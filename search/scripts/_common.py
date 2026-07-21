"""Shared helpers for Phase 2 literature-search scripts."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
QUERIES_PATH = REPO_ROOT / "search" / "queries.yaml"
SEARCH_LOG_PATH = REPO_ROOT / "search" / "search-log.md"
RAW_ROOT = REPO_ROOT / "search" / "raw"


def load_queries(path: Path = QUERIES_PATH) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data or "blocks" not in data or "meta" not in data:
        raise ValueError(f"Invalid queries file: {path}")
    return data


def raw_path(source: str, block_id: str, query_index: int) -> Path:
    """Deterministic raw output path: <block_id>_<query_index>.json (1-based index)."""
    return RAW_ROOT / source / f"{block_id}_{query_index}.json"


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_marker(source: str, block_id: str, query_index: int) -> str:
    return f"### {source} — {block_id} — query {query_index}"


def already_logged(source: str, block_id: str, query_index: int, log_path: Path = SEARCH_LOG_PATH) -> bool:
    if not log_path.exists():
        return False
    marker = log_marker(source, block_id, query_index)
    return marker in log_path.read_text(encoding="utf-8")


def append_search_log(
    *,
    source: str,
    block_id: str,
    query_index: int,
    query: str,
    n_results: int,
    notes: str = "",
    log_path: Path = SEARCH_LOG_PATH,
) -> None:
    """Append or replace a log entry for this source/block/query."""
    marker = log_marker(source, block_id, query_index)
    entry_lines = [
        marker,
        f"- **Query:** {query}",
        f"- **Date run:** {utc_now_iso()}",
        f"- **Results returned:** {n_results}",
    ]
    if notes:
        entry_lines.append(f"- **Notes:** {notes}")
    entry_lines.append("")
    entry_text = "\n".join(entry_lines)

    text = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
    placeholder = "_Entries appended by search scripts after Phase 2 begins._"
    if placeholder in text:
        text = text.replace(placeholder, "")
    if "**Status:** No searches executed yet" in text:
        text = re.sub(
            r"\*\*Status:\*\* No searches executed yet[^\n]*",
            "**Status:** Automated search runs in progress / completed (see entries below).",
            text,
            count=1,
        )

    # Replace existing section for this marker if present
    pattern = re.compile(
        rf"^{re.escape(marker)}\n(?:.*\n)*?(?=^### |\Z)",
        re.MULTILINE,
    )
    if pattern.search(text):
        text = pattern.sub(entry_text + "\n", text, count=1)
        log_path.write_text(text.rstrip() + "\n", encoding="utf-8")
        return

    log_path.write_text(text.rstrip() + "\n\n" + entry_text, encoding="utf-8")


def iter_queries(data: dict[str, Any]):
    """Yield (block_id, block_name, query_index_1based, query_string)."""
    for block in data["blocks"]:
        block_id = block["id"]
        name = block.get("name", block_id)
        for i, query in enumerate(block["queries"], start=1):
            yield block_id, name, i, query
