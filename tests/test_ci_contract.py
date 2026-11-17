#!/usr/bin/env python3
"""Repository safety and source-owned successor CI contract (stdlib only)."""
from __future__ import annotations

import json
from pathlib import Path
import stat
import unittest

ROOT = Path(__file__).resolve().parents[1]
SHARDS = {'contract': ['tests/test_additive_compat.py', 'tests/test_catalog_contract_binding.py', 'tests/test_constitution.py', 'tests/test_contract_freeze.py', 'tests/test_deferred_spec.py', 'tests/test_no_execution.py', 'tests/test_status_verify.py', 'tests/test_zero_link.py'], 'routing': ['tests/test_candidates.py', 'tests/test_catalog.py', 'tests/test_engine.py', 'tests/test_golden.py', 'tests/test_normalize.py', 'tests/test_proposal.py', 'tests/test_verdict.py'], 'surfaces': ['tests/test_catalog_egress.py', 'tests/test_cli.py', 'tests/test_cli_stub.py', 'tests/test_doctor.py', 'tests/test_egress_terms.py', 'tests/test_honest_confidence.py', 'tests/test_mcp.py', 'tests/test_proposal_exercise.py', 'tests/test_proposal_fixture.py', 'tests/test_state.py'], 'ci-negative': ['tests/test_ci_contract.py', 'tests/test_ci.py'], 'local-review': ['tests/test_local_review.py', 'tests/test_create_review_pr.py'], 'app-gate': ['tests/test_reviewer_app.py']}
CHECKOUT = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
PR_ENV = {"CI_HEAD_SHA": "${{ github.event.pull_request.head.sha }}",
          "CI_BASE_SHA": "${{ github.event.pull_request.base.sha }}"}
CODE = {"scripts/verify.py", "scripts/local_review.py", "scripts/create_review_pr.py", "scripts/reviewer_app.py"}
OWNER_RULES = {"/.github/** @KleinPerkins", "/scripts/** @KleinPerkins", "/tests/** @KleinPerkins", "/docs/** @KleinPerkins", "/checks/** @KleinPerkins", "/intent_router/** @KleinPerkins", "/contracts/** @KleinPerkins", "/Makefile @KleinPerkins", "/install.sh @KleinPerkins", "/status.yml @KleinPerkins", "/AGENTS.md @KleinPerkins", "/README.md @KleinPerkins", "/SECURITY.md @KleinPerkins"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def regular(path: Path) -> None:
    require(path.is_file() and not path.is_symlink(), f"not a regular non-symlink file: {path.name}")


def load_json(path: Path) -> dict:
    regular(path)
    result = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(result, dict), f"{path.name} must contain an object")
    return result


def check_policy(root: Path) -> None:
    policy = load_json(root / ".github/ci-contract.json")
    require(set(policy) == {"schema", "repository", "successor", "shards", "protected_paths",
                            "integration_allowlist", "legacy", "coverage_mapping"}, "unexpected contract fields")
    require(policy["schema"] == "intent-router-ci-contract/v1", "wrong successor schema")
    require(policy["repository"] == {"owner":"KleinPerkins", "name":"intent-router",
                                    "id":1294651532, "default_branch":"main"}, "repository identity drift")
    require(policy["successor"] == {"actions_app_id":15368, "reviewer_app_id":4217367,
                                    "required_check":"ci-required", "workflow":".github/workflows/ci.yml",
                                    "workflow_name":"CI", "activation":"gated"}, "successor identity drift")
    require(policy["shards"] == SHARDS, "closed shard command set drift")
    expected = {".github", "scripts", "tests", "docs", "AGENTS.md", "README.md", "SECURITY.md", "CODEOWNERS", "_ops", "checks", "intent_router", "Makefile", "install.sh", "contracts", "status.yml"}
    require(set(policy["protected_paths"]) == expected, "protected surface drift")
    require(policy["legacy"]["mode"] == "historical-until-control-cutover", "legacy mode drift")
    require(set(policy["coverage_mapping"]) == {"contracts", "routing", "surfaces", "delivery", "installation", "safety"}, "old obligations unmapped")
    require(all(isinstance(v,str) and len(v)>30 for v in policy["coverage_mapping"].values()), "empty coverage mapping")
    for name in policy["legacy"]["files"]:
        regular(root / name)
    for name in (".github/CODEOWNERS", "README.md", "AGENTS.md", "scripts/verify.py", *CODE):
        regular(root / name)


def check_workflow(workflow: dict) -> None:
    require(set(workflow) == {"name", "on", "permissions", "concurrency", "jobs"}, "workflow fields drift")
    require(workflow["name"] == "CI", "wrong workflow name")
    require(workflow["on"] == {"pull_request":{"types":["opened", "reopened", "synchronize", "ready_for_review"]},
                                "push":{"branches":["main"]}}, "unsafe or incomplete triggers")
    require(workflow["permissions"] == {"contents":"read"}, "CI must have contents-read only")
    require(workflow["concurrency"] == {"group":"ci-${{ github.event.pull_request.number || github.ref }}",
                                         "cancel-in-progress":True}, "concurrency drift")
    jobs = workflow["jobs"]
    require(set(jobs) == {*SHARDS, "ci-required"}, "missing or extra CI jobs")
    checkout = {"uses":CHECKOUT, "with":{"ref":"${{ github.sha }}", "persist-credentials":False, "fetch-depth":0}}
    for name, job in jobs.items():
        require(job.get("runs-on") == "ubuntu-24.04", "only free standard hosted Ubuntu is allowed")
        require(job.get("timeout-minutes") == 10, "bounded timeout required")
        require(job.get("name") == name, "job/check name drift")
        require(job.get("steps", [None])[0] == checkout, "checkout must pin action and exact revision without credentials")
        if name in SHARDS:
            require(set(job) == {"name", "runs-on", "timeout-minutes", "outputs", "steps"}, "unsafe shard fields")
            require(job["outputs"] == {"receipt":"${{ steps.verify.outputs.receipt }}"}, "shard receipt not exported")
            require(job["steps"] == [checkout, {"name":"Run "+name, "id":"verify", "env":PR_ENV,
                                                "run":"python3 -I -B scripts/verify.py shard --shard "+name}],
                    "shard execution must run its closed nonempty suite")
        else:
            require(set(job) == {"name", "needs", "if", "runs-on", "timeout-minutes", "steps"}, "unsafe aggregate fields")
            require(job["needs"] == list(SHARDS), "aggregate needs every shard exactly once")
            require(job["if"] == "${{ always() }}", "aggregate must always run")
            require(job["steps"] == [checkout, {"name":"Require every exact-run shard",
                                                "env":dict(PR_ENV, CI_NEEDS="${{ toJSON(needs) }}"),
                                                "run":"python3 -I -B scripts/verify.py aggregate"}],
                    "aggregate must verify actual needs and run identity")


def check_ownership(root: Path) -> None:
    path = root / ".github/CODEOWNERS"
    regular(path)
    rules = {line.strip() for line in path.read_text().splitlines() if line.strip() and not line.startswith("#")}
    require(OWNER_RULES <= rules, f"missing protected ownership: {sorted(OWNER_RULES - rules)}")
    # A later rule can override an earlier match. Restrict every effective owner line.
    require(all(line.split()[1:] == ["@KleinPerkins"] for line in rules), "unexpected ownership override")


def check_surface(root: Path) -> None:
    for folder, allowed in ((".github/workflows", {"ci.yml", "reviewer-app.yml"}), ("scripts", {Path(p).name for p in CODE})):
        for path in (root/folder).rglob("*"):
            if "__pycache__" in path.parts:
                continue
            require(not path.is_symlink(), f"symlink delivery input: {path}")
            if not path.is_file():
                continue
            relative=path.relative_to(root/folder).as_posix()
            label="unexpected workflow" if folder.startswith(".github") else "unexpected delivery code"
            require(relative in allowed, label+": "+relative)
            require(not path.stat().st_mode & 0o111, "delivery source must not be executable")


def check_docs(root: Path) -> None:
    text=(root/"docs/ci-delivery.md").read_text()
    for term in ("1294651532", "15368", "4217367", "ci-required", "publication", "owner/admin", "independent", "OFF", "historical"):
        require(term in text, "missing delivery boundary: "+term)


class IntentRouterCIContract(unittest.TestCase):
    def test_policy_identity_and_regular_inputs(self):
        check_policy(ROOT)

    def test_complete_workflow_topology_and_permissions(self):
        check_workflow(load_json(ROOT / ".github/workflows/ci.yml"))

    def test_protected_ownership(self):
        check_ownership(ROOT)

    def test_delivery_surface(self):
        check_surface(ROOT)

    def test_all_test_modules_mapped_exactly_once(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location("intent_ci_verify",ROOT/"scripts/verify.py")
        ci=importlib.util.module_from_spec(spec);spec.loader.exec_module(ci)
        declared=[p for paths in SHARDS.values() for p in paths]
        actual={p.relative_to(ROOT).as_posix() for p in (ROOT/"tests").glob("test_*.py")}
        self.assertEqual(set(declared),actual)
        self.assertEqual(len(declared),len(set(declared)))
        self.assertTrue(all(SHARDS.values()))
        self.assertEqual(ci.SHARDS,SHARDS)

    def test_committed_credential_files_are_forbidden(self):
        import fnmatch
        import subprocess
        paths=subprocess.check_output(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],cwd=ROOT).decode().split("\0")
        patterns=(".env", ".env.*", "*.env", "*.pem", "*.key", "*.p12", "*.pfx", "*.jks", "*.keystore", "*.kdbx", "id_rsa*", "id_dsa*", "id_ed25519*", ".netrc", ".pgpass", "credentials", "credentials.*", "service-account*.json")
        exceptions={".env.example", ".env.sample", ".env.template"}
        offenders=[name for name in paths if name and Path(name).name not in exceptions
                   and any(fnmatch.fnmatch(Path(name).name,pattern) for pattern in patterns)]
        self.assertEqual(offenders,[],"committed credential file detected")

    def test_qualified_producer_policy_does_not_activate_writer(self):
        import hashlib
        import importlib.util
        policy = load_json(ROOT/".github/review-enrollments.json")
        self.assertEqual(policy["repository_id"], 1294651532)
        self.assertIs(policy["enabled"], True)
        spec = importlib.util.spec_from_file_location("source_review", ROOT/"scripts/local_review.py")
        review = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(review)
        self.assertEqual(len(policy["producers"]), 2)
        self.assertEqual(len({p["origin_account"] for p in policy["producers"]}), 2)
        for producer in policy["producers"]:
            self.assertIs(producer["enabled"], True)
            self.assertEqual(producer["github_user_id"], 49759187)
            self.assertEqual(producer["instructions_sha256"], review.digest(review.INSTRUCTIONS))
            for field, path in (("capture_adapter_sha256", "scripts/local_review.py"),
                                ("creation_adapter_sha256", "scripts/create_review_pr.py")):
                self.assertEqual(producer[field], hashlib.sha256((ROOT/path).read_bytes()).hexdigest())
        workflow = load_json(ROOT/".github/workflows/reviewer-app.yml")
        write = [s for s in workflow["jobs"]["admit"]["steps"] if s.get("run", "").endswith("--write")]
        self.assertEqual(len(write), 1)
        self.assertIn("vars.REVIEWER_APP_ENABLED == 'true'", write[0]["if"])

    def test_operator_description(self):
        check_docs(ROOT)


if __name__ == "__main__":
    unittest.main(verbosity=2)
