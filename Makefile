# intent-router — shared operator-intent → verb-proposal capability. Make targets: help-first, .PHONY.
# P0 scope: architecture + frozen contracts + durable artifacts + gates. NO routing logic yet.
.DEFAULT_GOAL := help
.PHONY: help install repair doctor check uninstall verify verify-install test version freeze status-verify fix-hooks

help: ## Show available targets
	@echo "intent-router — router proposes, kernel decides (kernel-first). P0 = architecture/contracts freeze."
	@echo "  make install         - install intent-router into your XDG dirs (idempotent)"
	@echo "  make repair          - force re-copy the runtime"
	@echo "  make doctor          - read-only health check of the install"
	@echo "  make check           - CI-safe static preflight (no writes to HOME)"
	@echo "  make uninstall       - remove the install (KEEP_STATE=1 preserves router state)"
	@echo "  make test            - test suite (unittest; local-only, no network)"
	@echo "  make freeze          - contract-freeze checker (freeze strings + required-key floors)"
	@echo "  make status-verify   - recompute the status.yml ledger against disk/tests (cannot lie)"
	@echo "  make verify          - canonical gate: tests + freeze + status + static/full install checks"
	@echo "  make verify-install  - full install lifecycle in a throwaway HOME (headless/CI-safe)"
	@echo "  make fix-hooks       - install KleinPerkins local commit guards if the host overlay is present (see SECURITY.md)"
	@echo "  make version         - print the package version"

install: ## Install intent-router (idempotent)
	@bash ./install.sh

repair: ## Force re-copy the runtime
	@bash ./install.sh --repair

doctor: ## Read-only health check of the install
	@bash ./install.sh --doctor

check: ## CI-safe static preflight (no writes to HOME)
	@bash ./install.sh --check

uninstall: ## Remove the install (KEEP_STATE=1 to preserve router state)
	@bash ./install.sh --uninstall $(if $(KEEP_STATE),--keep-state,)

test: ## Run the test suite (unittest: contract-freeze, additive-proof, zero-link, status-verify, constitution, cli-stub)
	@bash tests/run-tests.sh

freeze: ## Contract-freeze checker (mirror of AWA's behavior-only freeze: strings + required-key floors)
	@bash checks/intent-contract-freeze.sh

status-verify: ## Recompute the status.yml ledger against disk/tests (the ledger cannot lie)
	@PYTHONPATH=. python3 -m intent_router.status_verify --strict

verify: ## Canonical local gate: tests + freeze + status + static and full install checks
	@bash tests/run-tests.sh
	@bash checks/intent-contract-freeze.sh
	@PYTHONPATH=. python3 -m intent_router.status_verify --strict
	@bash ./install.sh --check
	@$(MAKE) --no-print-directory verify-install
	@echo "verify: OK"

verify-install: ## Exercise the full install lifecycle in a throwaway HOME (never touches real ~)
	@set -eu; \
	  outer=""; \
	  cleanup() { \
	    if [ -n "$${outer:-}" ]; then \
	      rm -rf "$$outer" || return $$?; \
	      outer=""; \
	    fi; \
	  }; \
	  on_exit() { rc=$$?; trap - 0 HUP INT TERM; set +e; cleanup; exit "$$rc"; }; \
	  on_hup() { trap - 0 HUP INT TERM; set +e; cleanup; exit 129; }; \
	  on_int() { trap - 0 HUP INT TERM; set +e; cleanup; exit 130; }; \
	  on_term() { trap - 0 HUP INT TERM; set +e; cleanup; exit 143; }; \
	  trap 'on_exit' 0; \
	  trap 'on_hup' HUP; \
	  trap 'on_int' INT; \
	  trap 'on_term' TERM; \
	  outer=$$(mktemp -d "$${TMPDIR:-/tmp}/intent-router-verify.XXXXXX"); \
	  inner="$$outer/tmp"; \
	  HOME="$$outer/home"; \
	  XDG_DATA_HOME="$$outer/data"; \
	  XDG_CONFIG_HOME="$$outer/config"; \
	  XDG_STATE_HOME="$$outer/state"; \
	  export HOME XDG_DATA_HOME XDG_CONFIG_HOME XDG_STATE_HOME; \
	  mkdir -p "$$HOME" "$$inner"; \
	  runtime="$$XDG_DATA_HOME/intent-router/current"; \
	  pointer="$$XDG_DATA_HOME/intent-router/release-pointer.json"; \
	  env_file="$$XDG_CONFIG_HOME/intent-router/env"; \
	  state_dir="$$XDG_STATE_HOME/intent-router"; \
	  env HOME="$$HOME" XDG_DATA_HOME="$$XDG_DATA_HOME" XDG_CONFIG_HOME="$$XDG_CONFIG_HOME" XDG_STATE_HOME="$$XDG_STATE_HOME" TMPDIR="$$inner" bash ./install.sh >/dev/null; \
	  env HOME="$$HOME" XDG_DATA_HOME="$$XDG_DATA_HOME" XDG_CONFIG_HOME="$$XDG_CONFIG_HOME" XDG_STATE_HOME="$$XDG_STATE_HOME" TMPDIR="$$inner" bash ./install.sh >/dev/null; \
	  echo "  idempotent double-install OK"; \
	  env HOME="$$HOME" XDG_DATA_HOME="$$XDG_DATA_HOME" XDG_CONFIG_HOME="$$XDG_CONFIG_HOME" XDG_STATE_HOME="$$XDG_STATE_HOME" TMPDIR="$$inner" bash "$$XDG_DATA_HOME/intent-router/current/install.sh" --doctor; \
	  env HOME="$$HOME" XDG_DATA_HOME="$$XDG_DATA_HOME" XDG_CONFIG_HOME="$$XDG_CONFIG_HOME" XDG_STATE_HOME="$$XDG_STATE_HOME" TMPDIR="$$inner" bash "$$XDG_DATA_HOME/intent-router/current/install.sh" --uninstall >/dev/null; \
	  test ! -e "$$runtime"; \
	  test ! -e "$$pointer"; \
	  test ! -e "$$env_file"; \
	  test ! -e "$$state_dir"; \
	  cleanup; \
	  echo "verify-install: OK"

version: ## Print the package version
	@PYTHONPATH=. python3 -c "import intent_router; print(intent_router.__version__)"

fix-hooks: ## Install KleinPerkins local commit guards (identity/data/session-lock) if the host overlay is present
	@guard="$$HOME/dev/_ops/bin/install-identity-guard.sh"; \
	  if [ -x "$$guard" ]; then \
	    "$$guard" "$$(pwd)" && echo "fix-hooks: OK — commit guards installed into .git/hooks"; \
	  else \
	    echo "fix-hooks: KleinPerkins host overlay not found ($$guard)."; \
	    echo "  Local commit guards are a MACHINE-LOCAL developer aid, not part of this standalone"; \
	    echo "  capability. Durable, reproducible commit safety for every clone is CI"; \
	    echo "  (.github/workflows/baseline.yml) + branch protection. See SECURITY.md."; \
	  fi
