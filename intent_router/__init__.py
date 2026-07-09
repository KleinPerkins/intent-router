"""intent-router — shared operator-intent -> verb-proposal capability.

Constitutional invariant (see CONSTITUTION.md / contracts/intent-constitution.v1.json):
the router PROPOSES; it never executes and never authorizes. The consumer's kernel makes
the real decision, and the kernel never reads a router artifact (kernel-first: safety holds
router-OFF). Nothing in this package may become a NEW safety dependency for a consumer.

Zero-link: this package is destined for the global `tools/intent-router` shelf and therefore
carries ZERO org/governed-repo literals. Any host/consumer-specific facts live in the consumer's
own catalog + a machine-local policy, never here.

P0 status: architecture + frozen contracts only. No L0-L5 routing logic exists yet; the CLI is a
thin "not-yet" stub. Stdlib only (no third-party deps).
"""

from __future__ import annotations

__all__ = ["__version__"]
__version__ = "0.1.0"
