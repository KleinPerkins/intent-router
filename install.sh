#!/usr/bin/env bash
# install.sh — intent-router Standalone System Package (SSP) installer.
#
# Clone KleinPerkins/intent-router and run ./install.sh: it installs a self-contained runtime
# (frozen contracts + the intent_router package + the CLI shim + docs) into your XDG dirs with NO
# sibling-repo dependency. Idempotent, backup-before-write. P0 wires NO Cursor hooks and NO MCP
# server (hooks stay OFF until phase C1; the read-only MCP mirror lands with the runtime in R-core).
#
#   ./install.sh                 install/reconcile (idempotent)
#   ./install.sh --repair        force re-copy the runtime
#   ./install.sh --doctor        read-only health check of the install
#   ./install.sh --check         CI-safe static preflight (no writes to $HOME)
#   ./install.sh --uninstall [--keep-state]   remove the install (--keep-state preserves router state)
#
# Layout (all HOME/XDG-relative — honors a HOME override):
#   runtime  $XDG_DATA_HOME/intent-router/current/     contracts + package + checks + bin + docs
#   config   $XDG_CONFIG_HOME/intent-router/env        INTENT_ROUTER_HOME + PATH
#   state    $XDG_STATE_HOME/intent-router/            event-sourced JSONL + derived JSON (local disk)
#   pointer  $XDG_DATA_HOME/intent-router/release-pointer.json   self-describing release record
set -euo pipefail

SRC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd -P)"

_data_home() { echo "${XDG_DATA_HOME:-$HOME/.local/share}"; }
_config_home() { echo "${XDG_CONFIG_HOME:-$HOME/.config}"; }
_state_home() { echo "${XDG_STATE_HOME:-$HOME/.local/state}"; }

log()  { printf 'intent-router: %s\n' "$1"; }
warn() { printf 'intent-router: WARN %s\n' "$1" >&2; }
die()  { printf 'intent-router: ERROR %s\n' "$1" >&2; exit 1; }

RUNTIME="$(_data_home)/intent-router/current"
CONFIG_DIR="$(_config_home)/intent-router"
ENV_FILE="$CONFIG_DIR/env"
STATE_DIR="$(_state_home)/intent-router"
POINTER="$(_data_home)/intent-router/release-pointer.json"

COPY_TREES=(contracts checks intent_router bin tests)
COPY_FILES=(pyproject.toml Makefile install.sh bootstrap.sh ARCHITECTURE.md CONSTITUTION.md \
            RESUME.md ROLLBACK.md README.md SECURITY.md AGENTS.md LICENSE status.yml meta.yml)

_backup_write() {
  # _backup_write <dest> ; content on stdin. Backs up an existing dest (only if content differs).
  local dest="$1" tmp
  tmp="$(mktemp "${TMPDIR:-/tmp}/intent-router-install.XXXXXX")"
  cat > "$tmp"
  if [ -f "$dest" ] && cmp -s "$tmp" "$dest"; then rm -f "$tmp"; return 0; fi
  mkdir -p "$(dirname "$dest")"
  [ -f "$dest" ] && cp "$dest" "$dest.bak.$(date +%Y%m%d%H%M%S)" 2>/dev/null || true
  mv "$tmp" "$dest"
}

_sync_tree() {
  local src="$1" dest="$2"
  [ -d "$src" ] || return 0
  mkdir -p "$(dirname "$dest")"
  rm -rf "$dest"
  cp -R "$src" "$dest"
}

_remove_runtime_python_cache() {
  IR_RUNTIME="$RUNTIME" python3 - <<'PY'
import os
import shutil
from pathlib import Path

root = Path(os.environ["IR_RUNTIME"])
if not root.exists():
    raise SystemExit(0)
for current, directories, files in os.walk(root, topdown=False, followlinks=False):
    directory = Path(current)
    for name in files:
        path = directory / name
        if path.suffix in {".pyc", ".pyo"}:
            path.unlink()
    for name in directories:
        if name != "__pycache__":
            continue
        path = directory / name
        if path.is_symlink():
            path.unlink()
        else:
            shutil.rmtree(path)
PY
}

_release_pointer_tool() {
  local mode="$1"
  IR_MODE="$mode" IR_POINTER="$POINTER" IR_SOURCE="$SRC_ROOT" IR_RUNTIME="$RUNTIME" \
    IR_EXEC_ROOT="$SRC_ROOT" python3 - <<'PY'
from __future__ import annotations

import ast
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


POINTER_KEYS = {
    "schema",
    "version",
    "source",
    "commit",
    "runtime",
    "installed_at",
}
CACHE_SUFFIXES = {".pyc", ".pyo"}
UTC_SECOND = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class IntegrityError(Exception):
    def __init__(self, category: str, item: str) -> None:
        super().__init__(category, item)
        self.category = category
        self.item = item


class DuplicateKeyError(ValueError):
    pass


def fail(category: str, item: str) -> None:
    raise IntegrityError(category, item)


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def clean_git_environment() -> dict[str, str]:
    return {
        key: value
        for key, value in os.environ.items()
        if not key.startswith("GIT_")
    }


def own_git_metadata(source: Path) -> bool:
    metadata = source / ".git"
    try:
        mode = metadata.lstat().st_mode
    except FileNotFoundError:
        return False
    return not stat.S_ISLNK(mode) and (
        stat.S_ISREG(mode) or stat.S_ISDIR(mode)
    )


def git_source_commit(source: Path) -> str:
    environment = clean_git_environment()
    if shutil.which("git", path=environment.get("PATH")) is None:
        return "unknown"
    repository_backed = own_git_metadata(source)
    try:
        top_process = subprocess.run(
            ["git", "-C", str(source), "rev-parse", "--show-toplevel"],
            env=environment,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        fail("source-identity", "git-show-toplevel")
    if top_process.returncode != 0:
        if repository_backed:
            fail("source-identity", "git-show-toplevel")
        return "unknown"
    top_text = top_process.stdout.strip()
    if not top_text:
        fail("source-identity", "git-show-toplevel")
    try:
        top = Path(top_text).resolve(strict=True)
    except OSError:
        fail("source-identity", "git-show-toplevel")
    if top != source:
        if repository_backed:
            fail("source-identity", "git-top-level-mismatch")
        return "unknown"

    try:
        head_process = subprocess.run(
            ["git", "-C", str(source), "rev-parse", "--verify", "HEAD^{commit}"],
            env=environment,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        fail("source-identity", "git-head-commit")
    commit = head_process.stdout.strip()
    if head_process.returncode != 0 or not re.fullmatch(
        r"[0-9a-fA-F]{40,64}", commit
    ):
        fail("source-identity", "git-head-commit")
    return commit.lower()


def require_directory(path: Path, category: str, item: str) -> Path:
    try:
        mode = path.lstat().st_mode
    except OSError:
        fail(category, item)
    if (
        stat.S_ISLNK(mode)
        or not stat.S_ISDIR(mode)
        or not os.access(path, os.R_OK | os.X_OK)
    ):
        fail(category, item)
    try:
        return path.resolve(strict=True)
    except OSError:
        fail(category, item)


def require_regular(path: Path, category: str, item: str) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError:
        fail(category, item)
    if (
        stat.S_ISLNK(mode)
        or not stat.S_ISREG(mode)
        or not os.access(path, os.R_OK)
    ):
        fail(category, item)


def package_version(source: Path) -> str:
    version_path = source / "intent_router" / "__init__.py"
    require_regular(version_path, "source-identity", "intent_router/__init__.py")
    try:
        tree = ast.parse(version_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, SyntaxError):
        fail("source-identity", "intent_router/__init__.py")
    versions = []
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "__version__"
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            versions.append(node.value.value)
    if len(versions) != 1 or not versions[0]:
        fail("source-identity", "intent_router/__init__.py")
    return versions[0]


def valid_utc_second(value: str) -> bool:
    if not UTC_SECOND.fullmatch(value):
        return False
    try:
        dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return False
    return True


def read_pointer(pointer: Path) -> dict:
    require_regular(pointer, "pointer-file-safety", "release-pointer.json")
    try:
        value = json.loads(
            pointer.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError):
        fail("pointer-identity", "release-pointer.json")
    if (
        not isinstance(value, dict)
        or set(value) != POINTER_KEYS
        or any(not isinstance(value.get(key), str) for key in POINTER_KEYS)
    ):
        fail("pointer-identity", "release-pointer.json")
    return value


def safe_existing_pointer(pointer: Path) -> dict | None:
    try:
        mode = pointer.lstat().st_mode
    except FileNotFoundError:
        return None
    except OSError:
        fail("pointer-file-safety", "release-pointer.json")
    if (
        stat.S_ISLNK(mode)
        or not stat.S_ISREG(mode)
        or not os.access(pointer, os.R_OK)
    ):
        fail("pointer-file-safety", "release-pointer.json")
    try:
        value = json.loads(
            pointer.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError):
        return None
    return value if isinstance(value, dict) else None


def atomic_write_pointer(pointer: Path, value: dict) -> None:
    pointer.parent.mkdir(parents=True, exist_ok=True)
    temporary_name = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=pointer.parent,
            prefix=".release-pointer.",
            delete=False,
        ) as handle:
            temporary_name = handle.name
            json.dump(value, handle, indent=2)
            handle.write("\n")
        os.replace(temporary_name, pointer)
    except OSError:
        if temporary_name is not None:
            try:
                Path(temporary_name).unlink()
            except OSError:
                pass
        fail("pointer-file-safety", "release-pointer.json")


def write_pointer(pointer: Path, source_value: str, runtime_value: str) -> str:
    if not Path(source_value).is_absolute() or not Path(runtime_value).is_absolute():
        fail("pointer-identity", "writer-paths")
    source = require_directory(
        Path(source_value), "source-identity", "source-root"
    )
    runtime = require_directory(
        Path(runtime_value), "runtime-file-safety", "runtime-root"
    )
    version = package_version(source)
    commit = git_source_commit(source)
    identity = {
        "schema": "intent-release-pointer/v1",
        "version": version,
        "source": str(source),
        "commit": commit,
        "runtime": str(runtime),
    }
    installed_at = None
    existing = safe_existing_pointer(pointer)
    if existing is not None and all(
        existing.get(key) == value for key, value in identity.items()
    ):
        candidate = existing.get("installed_at")
        if isinstance(candidate, str) and valid_utc_second(candidate):
            installed_at = candidate
    if installed_at is None:
        installed_at = dt.datetime.now(dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
    value = dict(identity)
    value["installed_at"] = installed_at
    atomic_write_pointer(pointer, value)
    return version


def cache_artifact(runtime: Path) -> str | None:
    for current, directories, files in os.walk(
        runtime, topdown=True, followlinks=False
    ):
        root = Path(current)
        for name in directories:
            if name == "__pycache__":
                return (root / name).relative_to(runtime).as_posix()
        for name in files:
            if Path(name).suffix in CACHE_SUFFIXES:
                return (root / name).relative_to(runtime).as_posix()
    return None


def collect_monitored(root: Path, role: str) -> dict[str, Path]:
    category = "source-identity" if role == "source" else "runtime-file-safety"
    files: dict[str, Path] = {}

    package = root / "intent_router"
    package_present = package.exists() or package.is_symlink()
    if package_present:
        require_directory(package, category, "intent_router")
        for current, directories, names in os.walk(
            package, topdown=True, followlinks=False
        ):
            directory = Path(current)
            for name in list(directories):
                child = directory / name
                if child.is_symlink():
                    fail(
                        category,
                        child.relative_to(root).as_posix(),
                    )
            for name in names:
                if not name.endswith(".py"):
                    continue
                path = directory / name
                relative = path.relative_to(root).as_posix()
                require_regular(path, category, relative)
                files[relative] = path
    elif role == "source":
        fail("source-identity", "intent_router")

    contracts = root / "contracts"
    contracts_present = contracts.exists() or contracts.is_symlink()
    if contracts_present:
        require_directory(contracts, category, "contracts")
        try:
            contract_entries = list(contracts.iterdir())
        except OSError:
            fail(category, "contracts")
        for path in contract_entries:
            if not path.name.endswith(".json"):
                continue
            relative = path.relative_to(root).as_posix()
            require_regular(path, category, relative)
            files[relative] = path
    elif role == "source":
        fail("source-identity", "contracts")

    checker = root / "checks" / "intent-contract-freeze.sh"
    checker_present = checker.exists() or checker.is_symlink()
    if checker_present:
        relative = checker.relative_to(root).as_posix()
        require_regular(checker, category, relative)
        files[relative] = checker
    elif role == "source":
        fail("source-identity", "checks/intent-contract-freeze.sh")

    if role == "source" and not files:
        fail("source-identity", "monitored-file-set")
    return files


def file_sha256(path: Path, category: str, item: str) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    except OSError:
        fail(category, item)
    return digest.hexdigest()


def validate_pointer(
    pointer: Path, expected_runtime_value: str, executing_root_value: str
) -> None:
    value = read_pointer(pointer)
    if value["schema"] != "intent-release-pointer/v1":
        fail("pointer-identity", "schema")
    if not valid_utc_second(value["installed_at"]):
        fail("pointer-identity", "installed_at")
    if not Path(value["source"]).is_absolute():
        fail("pointer-identity", "source")
    if not Path(value["runtime"]).is_absolute():
        fail("pointer-identity", "runtime")

    try:
        expected_runtime = Path(expected_runtime_value).resolve(strict=True)
        executing_root = Path(executing_root_value).resolve(strict=True)
    except OSError:
        fail("pointer-identity", "execution-paths")
    source = require_directory(
        Path(value["source"]), "pointer-identity", "source"
    )
    runtime = require_directory(
        Path(value["runtime"]), "pointer-identity", "runtime"
    )
    if value["source"] != str(source):
        fail("pointer-identity", "source")
    if value["runtime"] != str(runtime) or runtime != expected_runtime:
        fail("pointer-identity", "runtime")
    if executing_root not in {source, runtime}:
        fail("pointer-identity", "executing-root")

    if value["version"] != package_version(source):
        fail("pointer-identity", "version")
    expected_commit = git_source_commit(source)
    if value["commit"] != expected_commit:
        fail("source-identity", "commit")

    cache = cache_artifact(runtime)
    if cache is not None:
        fail("runtime-cache-exclusion", cache)
    source_files = collect_monitored(source, "source")
    runtime_files = collect_monitored(runtime, "runtime")
    if not runtime_files:
        fail("runtime-file-set", "monitored-file-set")
    source_set = set(source_files)
    runtime_set = set(runtime_files)
    if source_set != runtime_set:
        difference = sorted(source_set ^ runtime_set)
        fail("runtime-file-set", difference[0] if difference else "monitored-file-set")
    for relative in sorted(source_set):
        source_digest = file_sha256(
            source_files[relative], "source-identity", relative
        )
        runtime_digest = file_sha256(
            runtime_files[relative], "runtime-file-safety", relative
        )
        if source_digest != runtime_digest:
            fail("runtime-byte-integrity", relative)


try:
    mode = os.environ["IR_MODE"]
    pointer = Path(os.environ["IR_POINTER"])
    if mode == "write":
        print(
            write_pointer(
                pointer,
                os.environ["IR_SOURCE"],
                os.environ["IR_RUNTIME"],
            )
        )
    elif mode == "validate":
        validate_pointer(
            pointer,
            os.environ["IR_RUNTIME"],
            os.environ["IR_EXEC_ROOT"],
        )
    else:
        fail("pointer-identity", "validator-mode")
except IntegrityError as error:
    print(
        f"intent-router: ERROR release-integrity "
        f"[{error.category}]: {error.item}",
        file=sys.stderr,
    )
    raise SystemExit(1)
except Exception:
    print(
        "intent-router: ERROR release-integrity "
        "[pointer-identity]: internal-validator-error",
        file=sys.stderr,
    )
    raise SystemExit(1)
PY
}

do_install() {
  local force="${1:-0}"
  log "installing runtime -> $RUNTIME"
  mkdir -p "$RUNTIME"
  for d in "${COPY_TREES[@]}"; do
    [ -d "$SRC_ROOT/$d" ] && _sync_tree "$SRC_ROOT/$d" "$RUNTIME/$d"
  done
  for f in "${COPY_FILES[@]}"; do
    [ -f "$SRC_ROOT/$f" ] && cp "$SRC_ROOT/$f" "$RUNTIME/$f"
  done
  _remove_runtime_python_cache
  chmod +x "$RUNTIME"/install.sh "$RUNTIME"/bootstrap.sh 2>/dev/null || true
  chmod +x "$RUNTIME"/checks/*.sh "$RUNTIME"/bin/* "$RUNTIME"/tests/*.sh 2>/dev/null || true

  # State dir (local disk, event-sourced). 700; the events.jsonl + per-consumer dirs are created at
  # runtime (R-core+), not by install.
  mkdir -p "$STATE_DIR/doctor"; chmod 700 "$STATE_DIR" 2>/dev/null || true

  # Config env — deterministic content (no timestamp) so a re-install is a true no-op.
  _backup_write "$ENV_FILE" <<EOF
# intent-router environment — generated by install.sh. Source this to put 'intent' on your PATH.
export INTENT_ROUTER_HOME="$RUNTIME"
export INTENT_ROUTER_STATE="\${INTENT_ROUTER_STATE:-$STATE_DIR}"
export PATH="$RUNTIME/bin:\$PATH"
EOF
  log "wrote config env -> $ENV_FILE"

  # Self-describing release pointer. installed_at is preserved across re-installs of identical
  # identity (version/commit/runtime/source) so a re-install is a no-op.
  local version
  version="$(_release_pointer_tool write)"
  log "wrote release pointer -> $POINTER (version $version)"
  [ "$force" = "1" ] && log "(--repair) forced re-copy complete."
  log "install OK. Source '$ENV_FILE' to put 'intent' on PATH."
  return 0
}

do_uninstall() {
  local keep_state=0
  [ "${1:-}" = "--keep-state" ] && keep_state=1
  log "uninstalling"
  rm -rf "$RUNTIME"
  rm -f "$ENV_FILE" "$POINTER"
  rmdir "$CONFIG_DIR" 2>/dev/null || true
  # Remove the now-empty data-home parent ($XDG_DATA_HOME/intent-router) too, if nothing else lives
  # there (e.g. no leftover .bak files). rmdir is a safe no-op when the dir is non-empty or absent.
  rmdir "$(_data_home)/intent-router" 2>/dev/null || true
  if [ "$keep_state" = "1" ]; then
    log "kept router state at $STATE_DIR (--keep-state)"
  elif [ -d "$STATE_DIR" ]; then
    warn "removing router state at $STATE_DIR — pass --keep-state to preserve it"
    rm -rf "$STATE_DIR"
  fi
  log "uninstall complete."
}

do_doctor() {
  local rc=0
  echo "== intent-router install doctor =="
  echo "   runtime=$RUNTIME"
  if [ -d "$RUNTIME" ]; then echo "  PASS  runtime present"; else echo "  FAIL  runtime missing (run ./install.sh)"; rc=1; fi
  if [ -f "$ENV_FILE" ]; then echo "  PASS  config env present"; else echo "  FAIL  config env missing"; rc=1; fi
  if [ -d "$STATE_DIR" ]; then echo "  PASS  state dir present"; else echo "  FAIL  state dir missing"; rc=1; fi
  if _release_pointer_tool validate; then
    echo "  PASS  release pointer present + valid identity/integrity"
  else echo "  FAIL  release pointer identity/integrity"; rc=1; fi
  if [ -d "$RUNTIME/contracts" ] && python3 -c 'import json,sys;json.load(open(sys.argv[1]))' "$RUNTIME/contracts/intent-catalog.v1.json" 2>/dev/null; then
    echo "  PASS  contracts present + valid"
  else echo "  FAIL  contracts missing/invalid"; rc=1; fi
  if INTENT_HOME="$RUNTIME" bash "$RUNTIME/checks/intent-contract-freeze.sh" >/dev/null 2>&1; then
    echo "  PASS  installed contracts satisfy the frozen behavior floor"
  else echo "  FAIL  installed contracts drifted from the freeze"; rc=1; fi
  if [ -x "$RUNTIME/bin/intent" ]; then echo "  PASS  intent CLI shim present"; else echo "  FAIL  intent CLI shim missing"; rc=1; fi
  [ "$rc" -eq 0 ] && echo "intent-router doctor: OK" || echo "intent-router doctor: FAILED"
  return "$rc"
}

# CI-safe static preflight — validates the SOURCE tree is install-ready. Writes NOTHING to $HOME.
do_check() {
  local rc=0
  echo "== intent-router install --check (static preflight, no writes) =="
  for f in contracts/intent-catalog.v1.json contracts/intent-map.v1.json \
           contracts/intent-proposal.v1.json contracts/intent-feedback.v1.json \
           contracts/intent-constitution.v1.json; do
    if python3 -c 'import json,sys;json.load(open(sys.argv[1]))' "$SRC_ROOT/$f" 2>/dev/null; then
      echo "  PASS  $f valid JSON"
    else echo "  FAIL  $f invalid/missing"; rc=1; fi
  done
  if INTENT_HOME="$SRC_ROOT" bash "$SRC_ROOT/checks/intent-contract-freeze.sh" >/dev/null 2>&1; then
    echo "  PASS  contracts satisfy the frozen behavior floor"
  else echo "  FAIL  contract freeze drift"; rc=1; fi
  if (cd "$SRC_ROOT" && PYTHONPATH=. python3 -c 'import intent_router; assert intent_router.__version__' ) 2>/dev/null; then
    echo "  PASS  intent_router package imports"
  else echo "  FAIL  package import failed"; rc=1; fi
  # meta.yml must classify kind: tool (NOT mcp).
  if grep -qE '^kind:[[:space:]]*tool[[:space:]]*$' "$SRC_ROOT/meta.yml"; then
    echo "  PASS  meta.yml kind: tool"
  else echo "  FAIL  meta.yml is not kind: tool"; rc=1; fi
  [ "$rc" -eq 0 ] && echo "intent-router --check: OK" || echo "intent-router --check: FAILED"
  return "$rc"
}

case "${1:-install}" in
  install|"")   do_install 0 ;;
  --repair)     do_install 1 ;;
  --doctor)     do_doctor ;;
  --check)      do_check ;;
  --uninstall)  shift; do_uninstall "${1:-}" ;;
  -h|--help)    sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//' ;;
  *) die "unknown argument: $1 (see --help)" ;;
esac
