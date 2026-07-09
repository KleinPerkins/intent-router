"""mcp_server — a READ-ONLY MCP mirror of the intent CLI. Stdlib-only, EXECUTIONLESS (CR1).

Mirrors exactly the four read-only CLI verbs as MCP tools — `intent_map`, `intent_explain`,
`intent_catalog_verify`, `intent_doctor` — and NOTHING else. There is no mutating tool path by
construction: the tool table below is the ENTIRE surface, every entry calls a pure engine/catalog/
doctor function, and none runs a consumer verb, spawns a process, or evaluates code.

Transport: newline-delimited JSON-RPC 2.0 over stdio (one compact JSON object per line, no
Content-Length framing). This is the minimal stdio framing an MCP client speaks; keeping it
stdlib-only means the router runtime pulls in no third-party dependency (locked: JSON/JSONL only,
no daemon). `handle_request` is a PURE function of one request object so the whole protocol is unit-
testable without a live client; `serve` is the thin stdin/stdout loop around it.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from . import __version__
from . import doctor as doctor_mod
from .catalog import verify_catalog_file
from .engine import explain as engine_explain
from .engine import propose as engine_propose

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "intent-router"

_DEFAULT_CONSUMER = "unknown"

# The COMPLETE tool surface (read-only). Each `handler` is a pure function taking the MCP `arguments`
# dict and returning a JSON-serializable result. Adding a mutating tool would require adding an entry
# here; there is intentionally no code path that could execute a consumer verb.
_STR = {"type": "string"}


def _load_catalog(path: str):
    """Read a catalog JSON into a dict (read-only). Returns (data, error)."""
    if not path:
        return None, "catalog_path is required"
    ok, errors = verify_catalog_file(path)
    if not ok:
        return None, "; ".join(errors)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh), None


def _consumer_of(catalog: Any, override: str | None) -> str:
    if override:
        return override
    c = catalog.get("consumer") if isinstance(catalog, dict) else None
    return c if isinstance(c, str) and c else _DEFAULT_CONSUMER


def _tool_map(args: dict) -> dict:
    catalog, err = _load_catalog(args.get("catalog_path", ""))
    if err:
        return {"error": f"catalog error: {err}"}
    return engine_propose(_consumer_of(catalog, args.get("consumer")),
                          args.get("utterance", ""), catalog)


def _tool_explain(args: dict) -> dict:
    catalog, err = _load_catalog(args.get("catalog_path", ""))
    if err:
        return {"error": f"catalog error: {err}"}
    top_n = args.get("top_n", 5)
    top_n = top_n if isinstance(top_n, int) and top_n > 0 else 5
    return engine_explain(_consumer_of(catalog, args.get("consumer")),
                          args.get("utterance", ""), catalog, top_n=top_n)


def _tool_catalog_verify(args: dict) -> dict:
    path = args.get("catalog_path", "")
    ok, errors = verify_catalog_file(path)
    return {"schema": "intent-catalog-verify/v1", "catalog": path, "ok": ok, "errors": errors}


def _tool_doctor(args: dict) -> dict:
    return doctor_mod.health_report(catalog_path=args.get("catalog_path"))


TOOLS = {
    "intent_map": {
        "handler": _tool_map,
        "description": "Propose a verb for an operator utterance (read-only, deterministic). "
                       "Returns an intent-proposal/v1 envelope; never executes anything.",
        "inputSchema": {
            "type": "object",
            "properties": {"utterance": _STR, "catalog_path": _STR, "consumer": _STR},
            "required": ["utterance", "catalog_path"],
        },
    },
    "intent_explain": {
        "handler": _tool_explain,
        "description": "Explain the ranked candidates and the resulting proposal (read-only).",
        "inputSchema": {
            "type": "object",
            "properties": {"utterance": _STR, "catalog_path": _STR, "consumer": _STR,
                           "top_n": {"type": "integer"}},
            "required": ["utterance", "catalog_path"],
        },
    },
    "intent_catalog_verify": {
        "handler": _tool_catalog_verify,
        "description": "Validate a consumer catalog against intent-catalog/v1 (read-only). Reports "
                       "bad safety_class / missing param_schema / unsafe tool_path / leaked host literals.",
        "inputSchema": {
            "type": "object",
            "properties": {"catalog_path": _STR},
            "required": ["catalog_path"],
        },
    },
    "intent_doctor": {
        "handler": _tool_doctor,
        "description": "Read-only health report (catalog/store/golden-set/drift).",
        "inputSchema": {
            "type": "object",
            "properties": {"catalog_path": _STR},
            "required": [],
        },
    },
}


def _result(req_id, result) -> dict:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def _error(req_id, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def _tools_list() -> dict:
    return {"tools": [
        {"name": name, "description": meta["description"], "inputSchema": meta["inputSchema"]}
        for name, meta in TOOLS.items()
    ]}


def _call_tool(params: dict):
    name = params.get("name")
    arguments = params.get("arguments") or {}
    meta = TOOLS.get(name)
    if meta is None:
        return None, f"unknown tool: {name!r}"
    result = meta["handler"](arguments)
    # MCP tool result: a content array. We return the structured JSON as a text block (clients parse
    # it) — plus `structuredContent` for clients that support it. Read-only: `isError` only reflects
    # a bad request (e.g. an unreadable catalog), never an execution failure (nothing executes).
    is_error = isinstance(result, dict) and "error" in result
    return {
        "content": [{"type": "text", "text": json.dumps(result, sort_keys=True)}],
        "structuredContent": result if isinstance(result, dict) else {"result": result},
        "isError": is_error,
    }, None


def handle_request(req: dict):
    """Handle ONE JSON-RPC request object. Returns a response dict, or None for a notification
    (no `id`) that needs no reply. Pure: depends only on `req` (+ read-only disk for catalogs)."""
    if not isinstance(req, dict) or req.get("jsonrpc") != "2.0":
        return _error(req.get("id") if isinstance(req, dict) else None, -32600, "invalid request")
    method = req.get("method")
    req_id = req.get("id")
    is_notification = "id" not in req

    if method == "initialize":
        return _result(req_id, {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SERVER_NAME, "version": __version__},
        })
    if method in ("notifications/initialized", "initialized"):
        return None  # notification — no reply
    if method == "tools/list":
        return _result(req_id, _tools_list())
    if method == "tools/call":
        result, err = _call_tool(req.get("params") or {})
        if err:
            return _error(req_id, -32602, err)
        return _result(req_id, result)
    if method == "ping":
        return _result(req_id, {})

    if is_notification:
        return None
    return _error(req_id, -32601, f"method not found: {method!r}")


def serve(stdin=None, stdout=None) -> int:
    """Thin stdio loop: read newline-delimited JSON-RPC requests, write newline-delimited responses.
    Read-only server: it only ever reads catalogs and serializes proposals/reports."""
    stdin = stdin if stdin is not None else sys.stdin
    stdout = stdout if stdout is not None else sys.stdout
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            stdout.write(json.dumps(_error(None, -32700, "parse error")) + "\n")
            stdout.flush()
            continue
        resp = handle_request(req)
        if resp is not None:
            stdout.write(json.dumps(resp) + "\n")
            stdout.flush()
    return 0


def main(argv=None) -> int:
    return serve()


if __name__ == "__main__":
    raise SystemExit(main())
