#!/usr/bin/env bash
# bootstrap.sh — one-command "clone + install" for intent-router.
#
# Run from a checkout (it just installs), or standalone (it clones KleinPerkins/intent-router to a
# durable location first, then installs). Idempotent: an existing clone is fast-forwarded.
#
#   bash bootstrap.sh [install-args...]     # e.g. bash bootstrap.sh --repair
set -euo pipefail

REPO="${INTENT_ROUTER_REPO_URL:-git@github.com:KleinPerkins/intent-router.git}"
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"

# Running from a checkout — install in place.
if [ -f "$SELF_DIR/install.sh" ] && [ -d "$SELF_DIR/intent_router" ]; then
  exec "$SELF_DIR/install.sh" "$@"
fi

CLONE_DIR="${INTENT_ROUTER_CLONE_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/intent-router/checkout}"
if [ -d "$CLONE_DIR/.git" ]; then
  echo "bootstrap: updating existing clone at $CLONE_DIR"
  git -C "$CLONE_DIR" fetch --quiet origin || true
  git -C "$CLONE_DIR" pull --ff-only --quiet || echo "bootstrap: could not fast-forward; installing current checkout"
else
  echo "bootstrap: cloning $REPO -> $CLONE_DIR"
  mkdir -p "$(dirname "$CLONE_DIR")"
  git clone --quiet "$REPO" "$CLONE_DIR"
fi

exec "$CLONE_DIR/install.sh" "$@"
