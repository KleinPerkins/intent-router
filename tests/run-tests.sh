#!/usr/bin/env bash
# run-tests.sh — run the intent-router test suite (stdlib unittest; local-only, no network).
#
# Runs from the repo root so `intent_router` (the package) and `tests` (the suite) both import
# with PYTHONPATH=repo-root. No governed git repos are created, so there is no host-hook chaining.
set -uo pipefail

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"   # tests/
ROOT="$(cd "$SELF_DIR/.." && pwd)"                              # repo root

# Never inherit a parent repo's git env into any scratch fixture.
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES 2>/dev/null || true

cd "$ROOT"
PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}" \
  python3 -m unittest discover -s tests -t . -p 'test_*.py' "$@"
