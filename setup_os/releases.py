"""Generated-agent release metadata helpers."""

from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any


def write_release_snapshot(
    output_dir: Path,
    version: str,
    title: str,
    artifacts: list[str],
    source: dict[str, Any],
) -> Path:
    release_dir = output_dir / ".setup_os" / "releases"
    release_dir.mkdir(parents=True, exist_ok=True)
    release_path = release_dir / f"{version}.json"

    snapshot = {
        "version": version,
        "title": title,
        "created_at": datetime.now(UTC).isoformat(),
        "artifacts": artifacts,
        "source": source,
    }
    release_path.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return release_path
