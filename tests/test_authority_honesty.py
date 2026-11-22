"""G0-V-R authority tests for the canonical gate and hermetic install receipt.

The local noexec proof is intentionally narrower than later exact controller-image
qualification: repository scripts are treated as interpreter input and must not need execute
bits.  Install fixtures use only throwaway HOME/XDG roots and always attempt uninstall.
"""

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
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


_REPO_ROOT = Path(__file__).resolve().parent.parent
_INSTALLER = _REPO_ROOT / "install.sh"
_MAKEFILE = _REPO_ROOT / "Makefile"
_POINTER_KEYS = {
    "schema",
    "version",
    "source",
    "commit",
    "runtime",
    "installed_at",
}
_INTEGRITY_CATEGORIES = {
    "pointer-file-safety",
    "pointer-identity",
    "source-identity",
    "runtime-file-safety",
    "runtime-file-set",
    "runtime-cache-exclusion",
    "runtime-byte-integrity",
}
_COPY_IGNORES = (
    ".git",
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "build",
    "dist",
)


def _without_git_environment(environment: dict[str, str]) -> dict[str, str]:
    return {key: value for key, value in environment.items() if not key.startswith("GIT_")}


def _run(
    command: list[str],
    *,
    cwd: Path = _REPO_ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 120,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def _output(process: subprocess.CompletedProcess[str]) -> str:
    return (process.stdout or "") + (process.stderr or "")


def _source_head(source: Path = _REPO_ROOT) -> str:
    process = _run(
        ["git", "-C", str(source), "rev-parse", "HEAD^{commit}"],
        env=_without_git_environment(dict(os.environ)),
    )
    if process.returncode != 0:
        raise AssertionError(f"cannot resolve source HEAD:\n{_output(process)}")
    return process.stdout.strip()


def _source_version(source: Path = _REPO_ROOT) -> str:
    text = (source / "intent_router" / "__init__.py").read_text(encoding="utf-8")
    matches = []
    for node in ast.walk(ast.parse(text)):
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "__version__"
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            matches.append(node.value.value)
    if len(matches) != 1:
        raise AssertionError("intent_router.__version__ is not one literal string assignment")
    return matches[0]


def _copy_source(destination: Path, source: Path = _REPO_ROOT) -> Path:
    shutil.copytree(
        source,
        destination,
        symlinks=True,
        ignore=shutil.ignore_patterns(*_COPY_IGNORES),
    )
    return destination


def _init_repository(source: Path, *, commit: bool) -> str | None:
    environment = _without_git_environment(dict(os.environ))
    commands = [
        ["git", "init", "-q"],
        ["git", "config", "user.name", "Intent Router Tests"],
        ["git", "config", "user.email", "intent-router-tests@example.invalid"],
    ]
    for command in commands:
        process = _run(command, cwd=source, env=environment)
        if process.returncode != 0:
            raise AssertionError(f"{command!r} failed:\n{_output(process)}")
    if not commit:
        return None
    for command in (["git", "add", "-A"], ["git", "commit", "-qm", "fixture"]):
        process = _run(command, cwd=source, env=environment)
        if process.returncode != 0:
            raise AssertionError(f"{command!r} failed:\n{_output(process)}")
    return _source_head(source)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _append_text(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _monitored_files(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    package = root / "intent_router"
    if package.is_dir():
        for path in package.rglob("*.py"):
            if path.is_file() and not path.is_symlink():
                files[path.relative_to(root).as_posix()] = path
    contracts = root / "contracts"
    if contracts.is_dir():
        for path in contracts.glob("*.json"):
            if path.is_file() and not path.is_symlink():
                files[path.relative_to(root).as_posix()] = path
    checker = root / "checks" / "intent-contract-freeze.sh"
    if checker.is_file() and not checker.is_symlink():
        files[checker.relative_to(root).as_posix()] = checker
    return files


def _cache_artifacts(root: Path) -> list[Path]:
    package = root / "intent_router"
    if not package.exists():
        return []
    return sorted(
        path
        for path in package.rglob("*")
        if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}
    )


def _root_metadata(path: Path) -> tuple[object, ...]:
    """Snapshot only the product-root inode metadata; never enumerate or read its contents."""
    try:
        info = path.lstat()
    except FileNotFoundError:
        return ("absent",)
    return (
        "present",
        stat.S_IFMT(info.st_mode),
        stat.S_IMODE(info.st_mode),
        info.st_ino,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def _real_product_root_snapshot() -> dict[str, tuple[object, ...]]:
    home = Path.home()
    paths = {
        "data": Path(os.environ.get("XDG_DATA_HOME", home / ".local" / "share"))
        / "intent-router",
        "config": Path(os.environ.get("XDG_CONFIG_HOME", home / ".config"))
        / "intent-router",
        "state": Path(os.environ.get("XDG_STATE_HOME", home / ".local" / "state"))
        / "intent-router",
    }
    return {label: _root_metadata(path) for label, path in paths.items()}


def _target_block(makefile: str, target: str) -> str:
    lines = makefile.splitlines()
    start = next(
        index for index, line in enumerate(lines) if line.startswith(f"{target}:")
    )
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line[0].isspace() and re.match(r"^[A-Za-z0-9_.-]+:", line):
            end = index
            break
    return "\n".join(lines[start:end])


def _embedded_release_pointer_source() -> str:
    installer = _INSTALLER.read_text(encoding="utf-8")
    function_start = installer.index("_release_pointer_tool() {")
    heredoc_start = installer.index("python3 - <<'PY'\n", function_start)
    heredoc_end = installer.index("\nPY\n}", heredoc_start)
    return installer[heredoc_start + len("python3 - <<'PY'\n") : heredoc_end]


class _HermeticInstall:
    def __init__(
        self,
        case: unittest.TestCase,
        *,
        source: Path = _REPO_ROOT,
        environment: dict[str, str] | None = None,
    ) -> None:
        self.source = source.resolve()
        self._temporary = TemporaryDirectory(prefix="intent-router-authority-")
        self.root = Path(self._temporary.name).resolve()
        self.home = self.root / "home"
        self.data_home = self.root / "data"
        self.config_home = self.root / "config"
        self.state_home = self.root / "state"
        self.tmpdir = self.root / "tmp"
        for path in (
            self.home,
            self.data_home,
            self.config_home,
            self.state_home,
            self.tmpdir,
        ):
            path.mkdir(parents=True, exist_ok=True)
        self.env = dict(os.environ)
        self.env.update(
            {
                "HOME": str(self.home),
                "XDG_DATA_HOME": str(self.data_home),
                "XDG_CONFIG_HOME": str(self.config_home),
                "XDG_STATE_HOME": str(self.state_home),
                "TMPDIR": str(self.tmpdir),
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )
        if environment:
            self.env.update(environment)
        self._closed = False
        case.addCleanup(self.close)

    @property
    def runtime(self) -> Path:
        return self.data_home / "intent-router" / "current"

    @property
    def pointer(self) -> Path:
        return self.data_home / "intent-router" / "release-pointer.json"

    @property
    def env_file(self) -> Path:
        return self.config_home / "intent-router" / "env"

    @property
    def state_dir(self) -> Path:
        return self.state_home / "intent-router"

    def run_source(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return _run(
            ["bash", str(self.source / "install.sh"), *arguments],
            cwd=self.source,
            env=self.env,
        )

    def run_runtime(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return _run(
            ["bash", str(self.runtime / "install.sh"), *arguments],
            cwd=self.runtime,
            env=self.env,
        )

    def install(self) -> subprocess.CompletedProcess[str]:
        return self.run_source()

    def doctor(self, *, installed_copy: bool = True) -> subprocess.CompletedProcess[str]:
        if installed_copy:
            return self.run_runtime("--doctor")
        return self.run_source("--doctor")

    def reset(self) -> subprocess.CompletedProcess[str]:
        if self.pointer.is_symlink():
            self.pointer.unlink()
        return self.install()

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            if (self.source / "install.sh").is_file():
                self.run_source("--uninstall")
        except (OSError, subprocess.SubprocessError):
            pass
        finally:
            self._temporary.cleanup()


class _HermeticAssertions(unittest.TestCase):
    def _fresh_install(
        self,
        *,
        source: Path = _REPO_ROOT,
        environment: dict[str, str] | None = None,
    ) -> _HermeticInstall:
        fixture = _HermeticInstall(self, source=source, environment=environment)
        process = fixture.install()
        self.assertEqual(
            process.returncode,
            0,
            f"hermetic install failed:\n{_output(process)}",
        )
        return fixture

    def _assert_doctor_green(
        self, fixture: _HermeticInstall, *, installed_copy: bool = True
    ) -> str:
        process = fixture.doctor(installed_copy=installed_copy)
        output = _output(process)
        self.assertEqual(process.returncode, 0, f"doctor should pass:\n{output}")
        self.assertIn("intent-router doctor: OK", output)
        return output

    def _assert_tamper_protocol(
        self,
        *,
        mutate,
        expected_category: str,
        prepare=None,
        semantic_check=None,
    ) -> None:
        self.assertIn(expected_category, _INTEGRITY_CATEGORIES)
        fixture = self._fresh_install()
        try:
            if prepare is not None:
                prepare(fixture)
            self._assert_doctor_green(fixture)
            mutate(fixture)
            if semantic_check is not None:
                semantic_check(fixture)
            process = fixture.doctor()
            output = _output(process)
            self.assertNotEqual(
                process.returncode,
                0,
                f"doctor falsely accepted one controlled mutation:\n{output}",
            )
            self.assertIn(
                expected_category,
                output,
                f"doctor rejected for the wrong reason:\n{output}",
            )
            reset = fixture.reset()
            self.assertEqual(
                reset.returncode,
                0,
                f"reset install failed:\n{_output(reset)}",
            )
            self._assert_doctor_green(fixture)
        finally:
            fixture.close()

    def _assert_installed_freeze_still_passes(
        self, fixture: _HermeticInstall
    ) -> None:
        environment = dict(fixture.env)
        environment["INTENT_HOME"] = str(fixture.runtime)
        process = _run(
            ["bash", str(fixture.runtime / "checks" / "intent-contract-freeze.sh")],
            cwd=fixture.runtime,
            env=environment,
        )
        self.assertEqual(
            process.returncode,
            0,
            "semantic freeze check should still pass before the integrity bite:\n"
            + _output(process),
        )


class TestNoexecCompatibleGate(unittest.TestCase):
    def test_makefile_target_graph_is_interpreter_invoked_and_complete(self):
        makefile = _MAKEFILE.read_text(encoding="utf-8")
        verify_block = _target_block(makefile, "verify")
        lifecycle_block = _target_block(makefile, "verify-install")

        verify_dry = _run(["make", "-n", "verify"])
        lifecycle_dry = _run(["make", "-n", "verify-install"])
        self.assertEqual(verify_dry.returncode, 0, _output(verify_dry))
        self.assertEqual(lifecycle_dry.returncode, 0, _output(lifecycle_dry))
        verify_graph = _output(verify_dry)
        lifecycle_graph = _output(lifecycle_dry)

        direct_installer_recipes = []
        for line in makefile.splitlines():
            if not line.startswith("\t") or "install.sh" not in line:
                continue
            if not re.search(
                r"""\bbash\s+(?:"[^"]*install\.sh"|\./install\.sh)""",
                line,
            ):
                direct_installer_recipes.append(line.strip())
        self.assertEqual(
            direct_installer_recipes,
            [],
            "every Makefile installer call must pass the script to bash:\n"
            + "\n".join(direct_installer_recipes),
        )

        ordered = (
            "bash tests/run-tests.sh",
            "bash checks/intent-contract-freeze.sh",
            "python3 -m intent_router.status_verify --strict",
            "bash ./install.sh --check",
            "verify-install: OK",
            'echo "verify: OK"',
        )
        positions = []
        for item in ordered:
            self.assertIn(item, verify_graph, f"canonical graph missing {item!r}")
            positions.append(verify_graph.index(item))
        self.assertEqual(positions, sorted(positions), "canonical gate order drifted")
        self.assertIn("$(MAKE) --no-print-directory verify-install", verify_block)

        self.assertIn("cleanup()", lifecycle_block)
        self.assertRegex(
            lifecycle_block,
            r"(?s)on_exit\(\).*?rc=\$\$\?.*?trap - 0 HUP INT TERM"
            r".*?cleanup.*?exit \"\$\$rc\"",
        )
        for handler, status_code, signal_name in (
            ("on_hup", "129", "HUP"),
            ("on_int", "130", "INT"),
            ("on_term", "143", "TERM"),
        ):
            self.assertRegex(
                lifecycle_block,
                rf"(?s){handler}\(\).*?trap - 0 HUP INT TERM"
                rf".*?cleanup.*?exit {status_code}",
            )
            self.assertRegex(
                lifecycle_block,
                rf"trap ['\"]{handler}['\"] {signal_name}",
            )
        self.assertRegex(lifecycle_block, r"""trap ['"]on_exit['"] 0""")
        self.assertNotRegex(
            lifecycle_block,
            r"(?s)on_(?:hup|int|term)\(\).*?verify-install: OK.*?\}",
        )
        self.assertIn('inner="$$outer/tmp"', lifecycle_block)
        self.assertIn('mktemp -d "$${TMPDIR:-/tmp}/intent-router-verify.', lifecycle_block)
        self.assertGreaterEqual(
            lifecycle_graph.count('TMPDIR="$inner"'),
            4,
            "every install/doctor/uninstall call must share the trapped inner TMPDIR",
        )
        self.assertIn('bash "$XDG_DATA_HOME/intent-router/current/install.sh" --doctor', lifecycle_graph)
        self.assertIn('bash "$XDG_DATA_HOME/intent-router/current/install.sh" --uninstall', lifecycle_graph)
        for required_absence in ("$runtime", "$pointer", "$env_file", "$state_dir"):
            self.assertIn(
                f'test ! -e "{required_absence}"',
                lifecycle_graph,
                f"post-uninstall absence check missing for {required_absence}",
            )
        self.assertRegex(
            lifecycle_block,
            r'(?s)cleanup;.*?echo "verify-install: OK"',
        )

    def test_verify_install_passes_with_nonexecutable_source_scripts(self):
        temporary = TemporaryDirectory(prefix="intent-router-noexec-copy-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        source = _copy_source(root / "source")
        scripts = set(source.rglob("*.sh"))
        scripts.update({source / "bootstrap.sh", source / "bin" / "intent"})
        for script in scripts:
            if script.is_file() and not script.is_symlink():
                script.chmod(stat.S_IMODE(script.stat().st_mode) & ~0o111)

        copied_installer = source / "install.sh"
        self.assertEqual(stat.S_IMODE(copied_installer.stat().st_mode), 0o644)
        denied = False
        try:
            direct = subprocess.run(
                [str(copied_installer), "--help"],
                cwd=str(source),
                capture_output=True,
                text=True,
                timeout=30,
            )
            denied = direct.returncode != 0
        except PermissionError:
            denied = True
        self.assertTrue(denied, "the copied mode-0644 installer must reject direct execution")

        environment = dict(os.environ)
        environment.update(
            {
                "HOME": str(root / "unused-home"),
                "XDG_DATA_HOME": str(root / "unused-data"),
                "XDG_CONFIG_HOME": str(root / "unused-config"),
                "XDG_STATE_HOME": str(root / "unused-state"),
                "TMPDIR": str(root),
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )
        process = _run(
            ["make", "verify-install"],
            cwd=source,
            env=environment,
        )
        self.assertEqual(
            process.returncode,
            0,
            "interpreter-invoked lifecycle should not need source execute bits:\n"
            + _output(process),
        )
        self.assertIn("verify-install: OK", _output(process))

    def test_verify_install_cleans_throwaway_root_on_failure(self):
        temporary = TemporaryDirectory(prefix="intent-router-failure-copy-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        source = _copy_source(root / "source")
        controlled_tmp = root / "controlled-tmp"
        controlled_tmp.mkdir()
        count_file = root / "install-count"
        installer = source / "install.sh"
        text = installer.read_text(encoding="utf-8")
        marker = "set -euo pipefail\n"
        injection = r'''
if [ "${IR_TEST_FAIL_SECOND_INSTALL:-0}" = "1" ] &&
   [ "${1:-install}" = "install" ]; then
  ir_test_count=0
  if [ -f "${IR_TEST_COUNT_FILE}" ]; then
    IFS= read -r ir_test_count < "${IR_TEST_COUNT_FILE}"
  fi
  ir_test_count=$((ir_test_count + 1))
  printf '%s\n' "$ir_test_count" > "${IR_TEST_COUNT_FILE}"
  if [ "$ir_test_count" -eq 2 ]; then
    exit 73
  fi
fi
'''
        self.assertIn(marker, text)
        installer.write_text(text.replace(marker, marker + injection, 1), encoding="utf-8")
        makefile = source / "Makefile"
        make_text = makefile.read_text(encoding="utf-8")
        old_outer = "tmp=$$(mktemp -d);"
        if old_outer in make_text:
            # BSD mktemp ignores TMPDIR without a template. Keep this regression focused on
            # cleanup by placing only the old recipe's outer root beneath the controlled TMPDIR.
            makefile.write_text(
                make_text.replace(
                    old_outer,
                    'tmp=$$(mktemp -d "$$TMPDIR/intent-router-verify.XXXXXX");',
                    1,
                ),
                encoding="utf-8",
            )

        environment = dict(os.environ)
        environment.update(
            {
                "TMPDIR": str(controlled_tmp),
                "IR_TEST_FAIL_SECOND_INSTALL": "1",
                "IR_TEST_COUNT_FILE": str(count_file),
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )
        process = _run(
            ["make", "verify-install"],
            cwd=source,
            env=environment,
        )
        self.assertNotEqual(process.returncode, 0, "the induced second install must fail")
        self.assertEqual(count_file.read_text(encoding="utf-8").strip(), "2")
        leaked = sorted(path.name for path in controlled_tmp.iterdir())
        self.assertEqual(
            leaked,
            [],
            "ordinary failure leaked outer/inner/installer temporary paths: "
            + ", ".join(leaked),
        )


class TestHermeticReleasePointer(_HermeticAssertions):
    def test_schema_and_version_are_exact(self):
        fixture = self._fresh_install()
        pointer = json.loads(fixture.pointer.read_text(encoding="utf-8"))
        self.assertEqual(set(pointer), _POINTER_KEYS)
        self.assertEqual(pointer["schema"], "intent-release-pointer/v1")
        self.assertEqual(pointer["version"], _source_version())
        self.assertEqual(pointer["version"], "0.1.0")
        parsed = dt.datetime.strptime(pointer["installed_at"], "%Y-%m-%dT%H:%M:%SZ")
        self.assertEqual(parsed.tzinfo, None)
        self.assertRegex(pointer["installed_at"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        preserved_timestamp = "2000-01-01T00:00:00Z"
        pointer["installed_at"] = preserved_timestamp
        fixture.pointer.write_text(
            json.dumps(pointer, indent=2) + "\n",
            encoding="utf-8",
        )
        reinstall = fixture.install()
        self.assertEqual(reinstall.returncode, 0, _output(reinstall))
        reinstalled_pointer = json.loads(
            fixture.pointer.read_text(encoding="utf-8")
        )
        self.assertEqual(
            reinstalled_pointer["installed_at"],
            preserved_timestamp,
            "an identical reinstall must preserve the valid install timestamp",
        )
        self._assert_doctor_green(fixture)

    def test_source_commit_matches_source_head(self):
        fixture = self._fresh_install()
        pointer = json.loads(fixture.pointer.read_text(encoding="utf-8"))
        self.assertEqual(pointer["commit"], _source_head())
        self.assertRegex(pointer["commit"], r"^[0-9a-f]{40}$")
        self._assert_doctor_green(fixture)

    def test_source_and_runtime_are_exact_and_hermetic(self):
        fixture = self._fresh_install()
        pointer = json.loads(fixture.pointer.read_text(encoding="utf-8"))
        self.assertEqual(Path(pointer["source"]), _REPO_ROOT.resolve())
        self.assertEqual(Path(pointer["runtime"]), fixture.runtime.resolve())
        self.assertTrue(fixture.runtime.is_relative_to(fixture.root))
        self.assertTrue(fixture.pointer.is_relative_to(fixture.root))
        self._assert_doctor_green(fixture, installed_copy=False)
        self._assert_doctor_green(fixture, installed_copy=True)

    def test_runtime_reinstall_preserves_validated_source_provenance(self):
        fixture = self._fresh_install()
        original = json.loads(fixture.pointer.read_text(encoding="utf-8"))

        reinstall = fixture.run_runtime()
        self.assertEqual(
            reinstall.returncode,
            0,
            "installed-copy idempotent install must use the validated original source:\n"
            + _output(reinstall),
        )
        repair = fixture.run_runtime("--repair")
        self.assertEqual(
            repair.returncode,
            0,
            "installed-copy repair must use the validated original source:\n"
            + _output(repair),
        )
        repaired = json.loads(fixture.pointer.read_text(encoding="utf-8"))
        self.assertEqual(repaired["source"], original["source"])
        self.assertEqual(repaired["commit"], original["commit"])
        self.assertEqual(repaired["source"], str(_REPO_ROOT.resolve()))
        self.assertEqual(repaired["commit"], _source_head())
        self._assert_doctor_green(fixture, installed_copy=False)
        self._assert_doctor_green(fixture, installed_copy=True)

        repaired["schema"] = "intent-release-pointer/v999"
        fixture.pointer.write_text(
            json.dumps(repaired, indent=2) + "\n",
            encoding="utf-8",
        )
        tampered_bytes = fixture.pointer.read_bytes()
        rejected = fixture.run_runtime()
        self.assertNotEqual(
            rejected.returncode,
            0,
            "installed-copy reinstall must not trust a malformed existing pointer",
        )
        self.assertIn("pointer-identity", _output(rejected))
        self.assertEqual(
            fixture.pointer.read_bytes(),
            tampered_bytes,
            "failed provenance selection must not rewrite the invalid pointer",
        )

    def test_normal_installed_cli_does_not_create_runtime_bytecode(self):
        fixture = self._fresh_install()
        cli_environment = dict(fixture.env)
        cli_environment.pop("PYTHONDONTWRITEBYTECODE", None)
        cli_environment.pop("PYTHONPYCACHEPREFIX", None)
        cli = _run(
            ["bash", str(fixture.runtime / "bin" / "intent"), "--version"],
            cwd=fixture.home,
            env=cli_environment,
        )
        self.assertEqual(cli.returncode, 0, _output(cli))
        self.assertEqual(cli.stdout.strip(), _source_version())
        self.assertEqual(
            _cache_artifacts(fixture.runtime),
            [],
            "normal installed CLI use must not create executable bytecode in runtime",
        )
        self._assert_doctor_green(fixture, installed_copy=False)
        self._assert_doctor_green(fixture, installed_copy=True)

        repair = fixture.run_runtime("--repair")
        self.assertEqual(
            repair.returncode,
            0,
            "runtime repair must stay green after normal CLI use:\n" + _output(repair),
        )
        self._assert_doctor_green(fixture)

        cache = fixture.runtime / "intent_router" / "__pycache__"
        cache.mkdir()
        (cache / "injected.pyc").write_bytes(b"controlled cache artifact")
        rejected = fixture.doctor()
        self.assertNotEqual(
            rejected.returncode,
            0,
            "doctor must still reject deliberately injected runtime bytecode",
        )
        self.assertIn("runtime-cache-exclusion", _output(rejected))
        reset = fixture.install()
        self.assertEqual(reset.returncode, 0, _output(reset))
        self._assert_doctor_green(fixture)

    def test_release_pointer_helper_respects_python_39_floor(self):
        source = _embedded_release_pointer_source()
        tree = ast.parse(source)
        forbidden = []
        for node in ast.walk(tree):
            annotations = []
            annotation = getattr(node, "annotation", None)
            if annotation is not None:
                annotations.append(annotation)
            returns = getattr(node, "returns", None)
            if returns is not None:
                annotations.append(returns)
            for annotation_root in annotations:
                for child in ast.walk(annotation_root):
                    if isinstance(child, ast.BinOp) and isinstance(child.op, ast.BitOr):
                        forbidden.append((child.lineno, ast.unparse(child)))
        self.assertEqual(
            forbidden,
            [],
            "embedded helper uses PEP 604 annotation spelling outside the Python 3.9 floor",
        )

        fixture = self._fresh_install()
        self._assert_doctor_green(fixture, installed_copy=False)
        self._assert_doctor_green(fixture, installed_copy=True)

    def test_installed_package_contract_and_checker_bytes_match_source(self):
        temporary = TemporaryDirectory(prefix="intent-router-cache-source-")
        self.addCleanup(temporary.cleanup)
        source = _copy_source(Path(temporary.name) / "source")
        cache_dir = source / "intent_router" / "__pycache__"
        cache_dir.mkdir()
        (cache_dir / "seed.cpython-312.pyc").write_bytes(b"seed-cache")
        (source / "intent_router" / "seed.pyc").write_bytes(b"seed-pyc")
        (source / "intent_router" / "seed.pyo").write_bytes(b"seed-pyo")

        fixture = self._fresh_install(source=source)
        source_files = _monitored_files(source)
        runtime_files = _monitored_files(fixture.runtime)
        self.assertTrue(source_files, "monitored source set must be nonempty")
        self.assertEqual(set(runtime_files), set(source_files))
        for relative, source_path in source_files.items():
            with self.subTest(relative=relative):
                self.assertEqual(_sha256(runtime_files[relative]), _sha256(source_path))
        self.assertEqual(
            _cache_artifacts(fixture.runtime),
            [],
            "source Python cache artifacts must not be copied into the runtime",
        )
        self._assert_doctor_green(fixture)

    def test_real_home_and_xdg_roots_are_untouched(self):
        before = _real_product_root_snapshot()
        fixture = self._fresh_install()
        self._assert_doctor_green(fixture, installed_copy=False)
        self._assert_doctor_green(fixture, installed_copy=True)
        fixture.close()
        after = _real_product_root_snapshot()
        self.assertEqual(
            after,
            before,
            "hermetic lifecycle changed metadata on a real product root",
        )

    def test_wrong_schema_commit_source_or_runtime_is_rejected(self):
        wrong_values = {
            "schema": "intent-release-pointer/v999",
            "version": "999.0.0",
            "source": "/definitely/not/the/intent-router/source",
            "commit": "0" * 40,
            "runtime": "/definitely/not/the/intent-router/runtime",
            "installed_at": "not-a-utc-second",
        }
        expected = {
            "schema": "pointer-identity",
            "version": "pointer-identity",
            "source": "pointer-identity",
            "commit": "source-identity",
            "runtime": "pointer-identity",
            "installed_at": "pointer-identity",
        }
        for field, value in wrong_values.items():
            with self.subTest(kind="wrong-value", field=field):
                def mutate(fixture, field=field, value=value):
                    pointer = json.loads(fixture.pointer.read_text(encoding="utf-8"))
                    pointer[field] = value
                    fixture.pointer.write_text(
                        json.dumps(pointer, indent=2) + "\n",
                        encoding="utf-8",
                    )

                self._assert_tamper_protocol(
                    mutate=mutate,
                    expected_category=expected[field],
                )

        for field in sorted(_POINTER_KEYS):
            with self.subTest(kind="non-string", field=field):
                def mutate(fixture, field=field):
                    pointer = json.loads(fixture.pointer.read_text(encoding="utf-8"))
                    pointer[field] = 1
                    fixture.pointer.write_text(
                        json.dumps(pointer, indent=2) + "\n",
                        encoding="utf-8",
                    )

                self._assert_tamper_protocol(
                    mutate=mutate,
                    expected_category="pointer-identity",
                )

        symlink_target: dict[str, Path] = {}

        def prepare_symlink(fixture):
            target = fixture.root / "otherwise-valid-pointer.json"
            target.write_bytes(fixture.pointer.read_bytes())
            symlink_target["path"] = target

        def replace_with_symlink(fixture):
            fixture.pointer.unlink()
            fixture.pointer.symlink_to(symlink_target["path"])

        with self.subTest(kind="pointer-symlink"):
            self._assert_tamper_protocol(
                prepare=prepare_symlink,
                mutate=replace_with_symlink,
                expected_category="pointer-file-safety",
            )

    def test_mismatched_installed_bytes_are_rejected(self):
        def package_semantics(fixture):
            ast.parse(
                (
                    fixture.runtime / "intent_router" / "__init__.py"
                ).read_text(encoding="utf-8")
            )

        cases = [
            (
                "python-comment",
                lambda fixture: _append_text(
                    fixture.runtime / "intent_router" / "__init__.py",
                    "\n# integrity mutation\n",
                ),
                "runtime-byte-integrity",
                package_semantics,
            ),
            (
                "contract-whitespace",
                lambda fixture: _append_text(
                    fixture.runtime / "contracts" / "intent-catalog.v1.json",
                    "\n",
                ),
                "runtime-byte-integrity",
                self._assert_installed_freeze_still_passes,
            ),
            (
                "checker-comment",
                lambda fixture: _append_text(
                    fixture.runtime / "checks" / "intent-contract-freeze.sh",
                    "\n# integrity mutation\n",
                ),
                "runtime-byte-integrity",
                self._assert_installed_freeze_still_passes,
            ),
            (
                "runtime-file-symlink",
                self._replace_runtime_file_with_source_symlink,
                "runtime-file-safety",
                None,
            ),
            (
                "missing-runtime-file",
                lambda fixture: (
                    fixture.runtime / "intent_router" / "__init__.py"
                ).unlink(),
                "runtime-file-set",
                None,
            ),
            (
                "extra-runtime-file",
                lambda fixture: (
                    fixture.runtime / "intent_router" / "extra_integrity_probe.py"
                ).write_text("# extra monitored file\n", encoding="utf-8"),
                "runtime-file-set",
                None,
            ),
            (
                "runtime-cache",
                self._inject_runtime_cache,
                "runtime-cache-exclusion",
                None,
            ),
        ]
        for name, mutate, category, semantic_check in cases:
            with self.subTest(case=name):
                self._assert_tamper_protocol(
                    mutate=mutate,
                    expected_category=category,
                    semantic_check=semantic_check,
                )

    @staticmethod
    def _replace_runtime_file_with_source_symlink(fixture):
        runtime_file = fixture.runtime / "intent_router" / "__init__.py"
        runtime_file.unlink()
        runtime_file.symlink_to(fixture.source / "intent_router" / "__init__.py")

    @staticmethod
    def _inject_runtime_cache(fixture):
        cache = fixture.runtime / "intent_router" / "__pycache__"
        cache.mkdir(exist_ok=True)
        (cache / "injected.pyc").write_bytes(b"controlled cache artifact")

    def test_git_source_identity_ignores_all_inherited_git_environment(self):
        temporary = TemporaryDirectory(prefix="intent-router-git-env-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        injected_paths = {
            "GIT_DIR": root / "git-dir",
            "GIT_WORK_TREE": root / "work-tree",
            "GIT_COMMON_DIR": root / "common-dir",
            "GIT_OBJECT_DIRECTORY": root / "objects",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES": root / "alternate-objects",
            "GIT_CONFIG_GLOBAL": root / "global.gitconfig",
            "GIT_CONFIG_SYSTEM": root / "system.gitconfig",
            "GIT_TRACE": root / "git.trace",
            "GIT_TRACE_SETUP": root / "git-setup.trace",
        }
        environment = {key: str(value) for key, value in injected_paths.items()}
        environment["GIT_CONFIG_COUNT"] = "0"

        fixture = self._fresh_install(environment=environment)
        pointer = json.loads(fixture.pointer.read_text(encoding="utf-8"))
        self.assertEqual(pointer["source"], str(_REPO_ROOT.resolve()))
        self.assertEqual(pointer["commit"], _source_head())
        self._assert_doctor_green(fixture, installed_copy=False)
        self._assert_doctor_green(fixture, installed_copy=True)
        for name in (
            "GIT_CONFIG_GLOBAL",
            "GIT_CONFIG_SYSTEM",
            "GIT_TRACE",
            "GIT_TRACE_SETUP",
        ):
            self.assertFalse(
                injected_paths[name].exists(),
                f"filtered {name} target was unexpectedly written",
            )

    def test_nested_nonrepository_source_does_not_inherit_parent_git_identity(self):
        temporary = TemporaryDirectory(prefix="intent-router-parent-repo-")
        self.addCleanup(temporary.cleanup)
        parent = Path(temporary.name) / "parent"
        parent.mkdir()
        (parent / "parent.txt").write_text("parent\n", encoding="utf-8")
        parent_head = _init_repository(parent, commit=True)
        source = _copy_source(parent / "nested" / "source")

        fixture = self._fresh_install(source=source)
        pointer = json.loads(fixture.pointer.read_text(encoding="utf-8"))
        self.assertNotEqual(parent_head, "unknown")
        self.assertEqual(
            pointer["commit"],
            "unknown",
            "a nested nonrepository source must not inherit its parent repository HEAD",
        )
        self._assert_doctor_green(fixture, installed_copy=False)
        self._assert_doctor_green(fixture, installed_copy=True)

    def test_repository_backed_git_failure_is_rejected(self):
        with self.subTest(stage="writer"):
            temporary = TemporaryDirectory(prefix="intent-router-unborn-repo-")
            self.addCleanup(temporary.cleanup)
            source = _copy_source(Path(temporary.name) / "source")
            _init_repository(source, commit=False)
            fixture = _HermeticInstall(self, source=source)
            process = fixture.install()
            self.assertNotEqual(
                process.returncode,
                0,
                "repository-backed source with no HEAD must fail pointer writing",
            )
            self.assertIn("source-identity", _output(process))
            fixture.close()

        with self.subTest(stage="doctor"):
            temporary = TemporaryDirectory(prefix="intent-router-broken-head-")
            self.addCleanup(temporary.cleanup)
            source = _copy_source(Path(temporary.name) / "source")
            _init_repository(source, commit=True)
            fixture = self._fresh_install(source=source)
            self._assert_doctor_green(fixture)

            environment = _without_git_environment(dict(os.environ))
            symbolic = _run(
                ["git", "symbolic-ref", "HEAD"],
                cwd=source,
                env=environment,
            )
            self.assertEqual(symbolic.returncode, 0, _output(symbolic))
            ref_path = source / ".git" / symbolic.stdout.strip()
            original = ref_path.read_bytes()
            ref_path.write_text("0" * 40 + "\n", encoding="ascii")
            try:
                process = fixture.doctor()
                self.assertNotEqual(
                    process.returncode,
                    0,
                    "repository-backed source with broken HEAD must fail doctor",
                )
                self.assertIn("source-identity", _output(process))
            finally:
                ref_path.write_bytes(original)
            self._assert_doctor_green(fixture)
            fixture.close()


if __name__ == "__main__":
    unittest.main()
