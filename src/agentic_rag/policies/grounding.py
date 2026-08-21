"""Grounding-verdict parsing and classification policy.

Kept separate from graph/nodes.py so the decision rule (what counts as a
valid verdict, how to fail safely on a malformed response) can be tested
and changed independently of the node's I/O/tracing responsibilities.
"""
from __future__ import annotations

import json

GROUNDING_VERDICTS = {"grounded", "insufficient_evidence", "unsupported"}


def parse_grounding_response(raw: str) -> tuple[str, list[str], bool]:
    """Parse the grounding verifier's JSON response defensively.

    Returns (verdict, unsupported_claims, parsed_successfully).

    Any parse failure or unrecognized verdict defaults to verdict='unsupported'
    with parsed_successfully=False - an unparseable response is not evidence
    the answer is fine, so we fail closed rather than fail open."""
    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            cleaned = cleaned.split("\n", 1)[-1] if "\n" in cleaned else cleaned
        payload = json.loads(cleaned)
        verdict = str(payload.get("verdict", "")).strip().lower()
        claims = payload.get("unsupported_claims") or []
        if verdict not in GROUNDING_VERDICTS:
            raise ValueError(f"unrecognized verdict: {verdict!r}")
        return verdict, [str(c) for c in claims], True
    except Exception:
        return "unsupported", [], False