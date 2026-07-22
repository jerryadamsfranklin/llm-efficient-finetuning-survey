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
RAW_V10_ROOT = REPO_ROOT / "search" / "raw_v1.0"


def load_local_env(path: Path | None = None) -> None:
    """Load KEY=VALUE pairs from local.env into os.environ (does not override)."""
    import os

    env_path = path or (REPO_ROOT / "local.env")
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_queries(path: Path = QUERIES_PATH) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data or "blocks" not in data or "meta" not in data:
        raise ValueError(f"Invalid queries file: {path}")
    return data


def raw_path(
    source: str,
    block_id: str,
    query_index: int,
    *,
    slice_id: str | None = None,
    root: Path = RAW_ROOT,
) -> Path:
    """Deterministic raw path: <block>_<n>.json or <block>_<n>__<slice>.json."""
    if slice_id:
        name = f"{block_id}_{query_index}__{slice_id}.json"
    else:
        name = f"{block_id}_{query_index}.json"
    return root / source / name


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_marker(
    source: str,
    block_id: str,
    query_index: int,
    *,
    slice_id: str | None = None,
) -> str:
    base = f"### {source} — {block_id} — query {query_index}"
    if slice_id:
        return f"{base} — slice {slice_id}"
    return base


def append_search_log(
    *,
    source: str,
    block_id: str,
    query_index: int,
    query: str,
    n_results: int,
    notes: str = "",
    slice_id: str | None = None,
    log_path: Path = SEARCH_LOG_PATH,
) -> None:
    """Append or replace a log entry for this source/block/query[/slice]."""
    marker = log_marker(source, block_id, query_index, slice_id=slice_id)
    entry_lines = [
        marker,
        f"- **Query:** {query}",
        f"- **Date run:** {utc_now_iso()}",
        f"- **Results returned:** {n_results}",
    ]
    if slice_id:
        entry_lines.append(f"- **Slice:** {slice_id}")
    if notes:
        entry_lines.append(f"- **Notes:** {notes}")
    entry_lines.append("")
    entry_text = "\n".join(entry_lines)

    text = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
    placeholder = "_Entries appended by search scripts after Phase 2 begins._"
    if placeholder in text:
        text = text.replace(placeholder, "")
    if (
        "awaiting owner confirmation" in text.lower()
        or "No searches executed yet" in text
        or "pending execution" in text.lower()
    ):
        text = re.sub(
            r"\*\*Status:\*\*[^\n]*",
            "**Status:** Protocol v1.2 search runs in progress / completed (see entries below).",
            text,
            count=1,
        )

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
    """Yield (block_id, block_name, query_index_1based, query_string) for boolean queries."""
    for block in data["blocks"]:
        block_id = block["id"]
        name = block.get("name", block_id)
        for i, query in enumerate(block["queries"], start=1):
            yield block_id, name, i, query


def iter_s2_queries(data: dict[str, Any]):
    """Yield S2 keyword variants (protocol v1.1). Falls back to boolean queries if missing."""
    for block in data["blocks"]:
        block_id = block["id"]
        name = block.get("name", block_id)
        s2 = block.get("s2_queries") or block.get("queries") or []
        for i, query in enumerate(s2, start=1):
            yield block_id, name, i, query
