"""Evolution timeline helpers."""

from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any


def append_timeline_event(output_dir: Path, event_type: str, title: str, details: dict[str, Any]) -> Path:
    timeline_dir = output_dir / ".setup_os"
    timeline_dir.mkdir(parents=True, exist_ok=True)
    timeline_path = timeline_dir / "timeline.jsonl"

    event = {
        "timestamp": datetime.now(UTC).isoformat(),
        "event_type": event_type,
        "title": title,
        "details": details,
    }
    with timeline_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, sort_keys=True) + "\n")

    return timeline_path
