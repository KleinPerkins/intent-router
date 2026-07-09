# intent-router — shared operator-intent → verb-proposal capability. Make targets: help-first, .PHONY.
# P0 scope: architecture + frozen contracts + durable artifacts + gates. NO routing logic yet.
.DEFAULT_GOAL := help
.PHONY: help install repair doctor check uninstall verify verify-install test version freeze status-verify

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
	@echo "  make verify          - test + freeze + status-verify + install --check (the repo gate)"
	@echo "  make verify-install  - full install lifecycle in a throwaway HOME (headless/CI-safe)"
	@echo "  make version         - print the package version"

install: ## Install intent-router (idempotent)
	@./install.sh

repair: ## Force re-copy the runtime
	@./install.sh --repair

doctor: ## Read-only health check of the install
	@./install.sh --doctor

check: ## CI-safe static preflight (no writes to HOME)
	@./install.sh --check

uninstall: ## Remove the install (KEEP_STATE=1 to preserve router state)
	@./install.sh --uninstall $(if $(KEEP_STATE),--keep-state,)

test: ## Run the test suite (unittest: contract-freeze, additive-proof, zero-link, status-verify, constitution, cli-stub)
	@bash tests/run-tests.sh

freeze: ## Contract-freeze checker (mirror of AWA's behavior-only freeze: strings + required-key floors)
	@bash checks/intent-contract-freeze.sh

status-verify: ## Recompute the status.yml ledger against disk/tests (the ledger cannot lie)
	@PYTHONPATH=. python3 -m intent_router.status_verify --strict

verify: ## Full local verification: test + freeze + status-verify + install --check
	@bash tests/run-tests.sh
	@bash checks/intent-contract-freeze.sh
	@PYTHONPATH=. python3 -m intent_router.status_verify --strict
	@./install.sh --check
	@echo "verify: OK"

verify-install: ## Exercise the full install lifecycle in a throwaway HOME (never touches real ~)
	@set -e; tmp=$$(mktemp -d); \
	  env HOME=$$tmp XDG_DATA_HOME=$$tmp/.local/share XDG_CONFIG_HOME=$$tmp/.config XDG_STATE_HOME=$$tmp/.local/state ./install.sh >/dev/null; \
	  env HOME=$$tmp XDG_DATA_HOME=$$tmp/.local/share XDG_CONFIG_HOME=$$tmp/.config XDG_STATE_HOME=$$tmp/.local/state ./install.sh >/dev/null; \
	  echo "  idempotent double-install OK"; \
	  env HOME=$$tmp XDG_DATA_HOME=$$tmp/.local/share XDG_CONFIG_HOME=$$tmp/.config XDG_STATE_HOME=$$tmp/.local/state ./install.sh --doctor; \
	  env HOME=$$tmp XDG_DATA_HOME=$$tmp/.local/share XDG_CONFIG_HOME=$$tmp/.config XDG_STATE_HOME=$$tmp/.local/state ./install.sh --uninstall >/dev/null; \
	  rm -rf $$tmp; \
	  echo "verify-install: OK"

version: ## Print the package version
	@PYTHONPATH=. python3 -c "import intent_router; print(intent_router.__version__)"
