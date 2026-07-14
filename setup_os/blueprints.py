"""Generated vertical blueprint helpers."""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

from setup_os.policy import policy_for_slug
from setup_os.quality import agent_dna
from setup_os.spec import AgentSpec


def create_agent_directories(output_dir: Path) -> None:
    for directory in [
        "agents",
        "memory/raw",
        "memory/structured",
        "memory/policy",
        "tools",
        "notifications",
        "scheduler",
        "config",
        "evolution",
        "audit",
        "deployment",
    ]:
        (output_dir / directory).mkdir(parents=True, exist_ok=True)


def write_agent_metadata(spec: AgentSpec, output_dir: Path) -> None:
    policy = policy_for_slug(spec.slug)
    _write(
        output_dir / "config.json",
        json.dumps(
            {
                "name": spec.name,
                "slug": spec.slug,
                "mode": "advisory",
                "storage": spec.storage,
                "notifications": spec.notifications,
                "notification_channels": {
                    "ntfy": {
                        "enabled": False,
                        "server": "https://ntfy.sh",
                        "topic_env": "SETUP_OS_NTFY_TOPIC",
                    }
                },
                "action_policy": policy.to_dict(),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
    )
    _write(
        output_dir / "agent_dna.json",
        json.dumps(agent_dna(spec), indent=2, sort_keys=True) + "\n",
    )
    write_verifier(output_dir)
    write_runtime_health(output_dir)
    write_runtime_node(output_dir)
    write_local_handoff(output_dir)
    write_conversation_importer(output_dir)
    write_memory_extractor(output_dir)
    write_memory_update_reporter(output_dir)
    write_functional_evolution_reporter(output_dir)
    write_extraction_observability_reporter(output_dir)


def write_verifier(output_dir: Path) -> None:
    _write(
        output_dir / "verify.py",
        """from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).parent
REQUIRED_PATHS = [
    "README.md",
    "agent_spec.json",
    "architecture.md",
    "docs/diagrams/overview_orchestration.html",
    "docs/diagrams/runtime_architecture.html",
    "docs/diagrams/evolution_safety_flow.html",
    "agent_dna.json",
    "config.json",
    "import_conversation.py",
    "extract_memory.py",
    "memory_update_report.py",
    "functional_evolution_report.py",
    "extraction_observability.py",
    "report.py",
    "health.py",
    "runtime_node.py",
    "handoff.py",
    ".setup_os",
    "memory/raw",
    "memory/structured",
    "memory/policy",
    "notifications",
    "evolution",
    "audit",
    "deployment",
]


def main() -> int:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    if missing:
        print("Verification failed. Missing:")
        for path in missing:
            print(f"- {path}")
        return 1

    print("Verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def write_runtime_health(output_dir: Path) -> None:
    _write(
        output_dir / "health.py",
        """from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent
REQUIRED_PATHS = [
    "README.md",
    "agent_spec.json",
    "architecture.md",
    "agent_dna.json",
    "config.json",
    "import_conversation.py",
    "extract_memory.py",
    "memory_update_report.py",
    "functional_evolution_report.py",
    "extraction_observability.py",
    "report.py",
    "verify.py",
    "runtime_node.py",
    "handoff.py",
    "memory/raw",
    "memory/structured",
    "memory/policy",
    "notifications",
    "scheduler",
    "reports",
    ".setup_os",
]


def check_required_paths() -> list[str]:
    return [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]


def check_config() -> list[str]:
    issues: list[str] = []
    config_path = ROOT / "config.json"
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except OSError as error:
        return [f"config.json is unreadable: {error}"]
    except json.JSONDecodeError as error:
        return [f"config.json is invalid JSON: {error}"]

    if not config.get("name"):
        issues.append("config.json is missing name")
    if not config.get("slug"):
        issues.append("config.json is missing slug")
    if not config.get("action_policy"):
        issues.append("config.json is missing action_policy")
    return issues


def check_notifications() -> list[str]:
    inbox_path = ROOT / ".setup_os" / "notifications.jsonl"
    if not inbox_path.exists():
        return []

    issues: list[str] = []
    try:
        lines = inbox_path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        return [f"notifications.jsonl is unreadable: {error}"]

    for index, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            issues.append(f"notifications.jsonl line {index} is invalid JSON: {error}")
            continue
        for key in ["timestamp", "source", "title", "severity", "status"]:
            if key not in event:
                issues.append(f"notifications.jsonl line {index} is missing {key}")
    return issues


def main() -> int:
    issues = []
    issues.extend(f"missing required path: {path}" for path in check_required_paths())
    issues.extend(check_config())
    issues.extend(check_notifications())

    if issues:
        print("Runtime health check failed.")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("Runtime health check passed.")
    print("- required files and folders exist")
    print("- config and action policy are readable")
    print("- scheduler folder is present")
    print("- notification inbox is readable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def write_runtime_node(output_dir: Path) -> None:
    _write(
        output_dir / "runtime_node.py",
        """from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).parent
RUNTIME_LOG_PATH = ROOT / ".setup_os" / "runtime_node.jsonl"
INBOX_PATH = ROOT / ".setup_os" / "notifications.jsonl"


def run_step(label: str, command: list[str]) -> dict[str, object]:
    started_at = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(
        [sys.executable, *command],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "label": label,
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "command": command,
        "exit_code": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def append_runtime_log(record: dict[str, object]) -> None:
    RUNTIME_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RUNTIME_LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, sort_keys=True) + "\\n")


def read_inbox_count() -> int:
    if not INBOX_PATH.exists():
        return 0
    return len([line for line in INBOX_PATH.read_text(encoding="utf-8").splitlines() if line.strip()])


def run_once(include_report: bool) -> int:
    steps = [run_step("health", ["health.py"])]
    if include_report:
        steps.append(run_step("report", ["report.py"]))

    record = {
        "event": "runtime_node_run_once",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "personal_runtime_node",
        "steps": steps,
        "notification_count": read_inbox_count(),
        "next_step": "Schedule this command on a personal runtime node after reviewing outputs.",
    }
    append_runtime_log(record)

    print("Runtime node run complete.")
    print(f"- log: {RUNTIME_LOG_PATH}")
    print(f"- notifications: {record['notification_count']}")
    for step in steps:
        marker = "OK" if step["exit_code"] == 0 else "FAILED"
        print(f"- {marker}: {step['label']} ({step['exit_code']})")
    return 0 if all(step["exit_code"] == 0 for step in steps) else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run generated-agent runtime checks once for a personal always-on node.",
    )
    parser.add_argument(
        "--skip-report",
        action="store_true",
        help="Only run health checks and inbox counting.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return run_once(include_report=not args.skip_report)


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def write_local_handoff(output_dir: Path) -> None:
    _write(
        output_dir / "handoff.py",
        """from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent
HANDOFF_PATH = ROOT / "handoff.md"


def exists_line(label: str, relative_path: str) -> str:
    marker = "OK" if (ROOT / relative_path).exists() else "MISSING"
    return f"- {marker}: {label} (`{relative_path}`)"


def count_jsonl(relative_path: str) -> int:
    path = ROOT / relative_path
    if not path.exists():
        return 0
    return len([line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()])


def latest_runtime_status() -> str:
    path = ROOT / ".setup_os" / "runtime_node.jsonl"
    if not path.exists():
        return "Runtime node has not run yet."
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return "Runtime node log is empty."
    try:
        latest = json.loads(lines[-1])
    except json.JSONDecodeError:
        return "Runtime node log has an unreadable latest entry."
    failed = [
        step.get("label", "unknown")
        for step in latest.get("steps", [])
        if step.get("exit_code") != 0
    ]
    if failed:
        return f"Latest runtime node cycle needs review: {', '.join(failed)} failed."
    return "Latest runtime node cycle passed health/report steps."


def build_handoff() -> str:
    lines = [
        "# Local Utility Handoff",
        "",
        "This file summarizes the generated system state for a personal laptop, Mac mini, or other always-on runtime node.",
        "",
        "## Readiness",
        "",
        exists_line("Config", "config.json"),
        exists_line("Health command", "health.py"),
        exists_line("Report command", "report.py"),
        exists_line("Runtime node command", "runtime_node.py"),
        exists_line("Daily report", "reports/daily_report.md"),
        exists_line("Notification inbox", ".setup_os/notifications.jsonl"),
        exists_line("Runtime node log", ".setup_os/runtime_node.jsonl"),
        exists_line("Raw memory import manifest", "memory/raw/import_manifest.jsonl"),
        exists_line("Structured memory drafts", "memory/structured/extraction_drafts.jsonl"),
        exists_line("Memory update report", "memory/structured/memory_update_report.md"),
        exists_line("Functional evolution report", "evolution/functional_evolution_report.md"),
        exists_line("Extraction observability report", "memory/structured/extraction_observability.md"),
        "",
        "## Current Counts",
        "",
        f"- Notifications: {count_jsonl('.setup_os/notifications.jsonl')}",
        f"- Runtime cycles: {count_jsonl('.setup_os/runtime_node.jsonl')}",
        f"- Raw conversation imports: {count_jsonl('memory/raw/import_manifest.jsonl')}",
        f"- Structured memory drafts: {count_jsonl('memory/structured/extraction_drafts.jsonl')}",
        "",
        "## Runtime Status",
        "",
        f"- {latest_runtime_status()}",
        "",
        "## Next Local Steps",
        "",
        "1. Run `python health.py` and fix any missing required files.",
        "2. Run `python report.py` and review the daily report.",
        "3. Import saved conversations with `python import_conversation.py path/to/export.md`.",
        "4. Run `python extract_memory.py` and review structured drafts before promotion.",
        "5. Run `python memory_update_report.py --all` and review evidence before promoting memory.",
        "6. Run `python functional_evolution_report.py --all` and review proposed extractor upgrades separately.",
        "7. Run `python extraction_observability.py` to inspect traceability and quality signals.",
        "8. Run `python runtime_node.py --skip-report` before scheduling on an always-on machine.",
        "9. Keep phone notifications approval-gated until alert volume feels useful.",
        "",
    ]
    return "\\n".join(lines)


def main() -> int:
    HANDOFF_PATH.write_text(build_handoff(), encoding="utf-8")
    print(f"Wrote {HANDOFF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def write_conversation_importer(output_dir: Path) -> None:
    _write(
        output_dir / "import_conversation.py",
        """from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).parent
RAW_MEMORY_DIR = ROOT / "memory" / "raw"
MANIFEST_PATH = RAW_MEMORY_DIR / "import_manifest.jsonl"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or "conversation"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def import_conversation(source: Path) -> Path:
    if not source.exists():
        raise FileNotFoundError(source)
    if not source.is_file():
        raise IsADirectoryError(source)

    RAW_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination = RAW_MEMORY_DIR / f"{timestamp}-{slugify(source.stem)}{source.suffix or '.txt'}"
    shutil.copy2(source, destination)

    record = {
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source_path": str(source),
        "stored_path": str(destination.relative_to(ROOT)),
        "source_name": source.name,
        "source_size_bytes": source.stat().st_size,
        "sha256": file_sha256(destination),
        "memory_layer": "raw",
        "status": "stored_raw_only",
        "next_step": "Run structured extraction separately before proposing strategy changes.",
    }
    with MANIFEST_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, sort_keys=True) + "\\n")

    return destination


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Import a saved conversation into raw local memory without mutating strategy.",
    )
    parser.add_argument("conversation", help="Path to a saved ChatGPT/AI conversation file.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    destination = import_conversation(Path(args.conversation))
    print(f"Imported raw conversation to {destination}")
    print(f"Updated {MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def write_memory_extractor(output_dir: Path) -> None:
    _write(
        output_dir / "extract_memory.py",
        """from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re


ROOT = Path(__file__).parent
RAW_MEMORY_DIR = ROOT / "memory" / "raw"
MANIFEST_PATH = RAW_MEMORY_DIR / "import_manifest.jsonl"
STRUCTURED_MEMORY_DIR = ROOT / "memory" / "structured"
DRAFTS_PATH = STRUCTURED_MEMORY_DIR / "extraction_drafts.jsonl"


RISK_TERMS = [
    "alert",
    "concentration",
    "drawdown",
    "loss",
    "rebalance",
    "risk",
    "sell",
    "threshold",
    "warn",
]
STRATEGY_TERMS = [
    "allocation",
    "buy",
    "diversify",
    "goal",
    "hold",
    "portfolio",
    "strategy",
    "watchlist",
]


def load_manifest() -> list[dict[str, object]]:
    if not MANIFEST_PATH.exists():
        return []
    records = []
    for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def matching_lines(text: str, terms: list[str]) -> list[str]:
    matches = []
    for line in text.splitlines():
        normalized = line.strip()
        if not normalized:
            continue
        lowered = normalized.lower()
        if any(term in lowered for term in terms):
            matches.append(normalized[:240])
    return matches[:12]


def extract_tickers(text: str) -> list[str]:
    tickers = sorted(set(re.findall(r"\\b[A-Z]{2,5}\\b", text)))
    ignored = {"AI", "API", "CSV", "JSON", "LLM", "MCP", "OS", "TXT"}
    return [ticker for ticker in tickers if ticker not in ignored][:25]


def build_draft(record: dict[str, object]) -> dict[str, object]:
    stored_path = ROOT / str(record["stored_path"])
    text = stored_path.read_text(encoding="utf-8", errors="replace")
    risk_rules = matching_lines(text, RISK_TERMS)
    strategy_notes = matching_lines(text, STRATEGY_TERMS)
    watchlist = extract_tickers(text)

    return {
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "source_name": record.get("source_name"),
        "source_path": record.get("stored_path"),
        "source_sha256": record.get("sha256"),
        "memory_layer": "structured",
        "status": "draft_requires_review",
        "confidence": 0.45,
        "holdings_context": [],
        "strategy_notes": strategy_notes,
        "risk_rules": risk_rules,
        "watchlist": watchlist,
        "next_step": "Review this draft before promoting anything into policy, strategy, alerts, or evolution proposals.",
    }


def write_drafts(drafts: list[dict[str, object]]) -> None:
    STRUCTURED_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    with DRAFTS_PATH.open("w", encoding="utf-8") as file:
        for draft in drafts:
            file.write(json.dumps(draft, sort_keys=True) + "\\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract review-only structured memory drafts from raw imported conversations.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Extract drafts for all raw imports in the manifest.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    records = load_manifest()
    if not records:
        print("No raw conversation imports found. Run import_conversation.py first.")
        return 1
    if not args.all:
        records = records[-1:]

    drafts = [build_draft(record) for record in records]
    write_drafts(drafts)
    print(f"Wrote {len(drafts)} structured memory draft(s) to {DRAFTS_PATH}")
    print("Drafts require review before strategy, policy, alert, or evolution changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def write_memory_update_reporter(output_dir: Path) -> None:
    _write(
        output_dir / "memory_update_report.py",
        """from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re


ROOT = Path(__file__).parent
RAW_MEMORY_DIR = ROOT / "memory" / "raw"
MANIFEST_PATH = RAW_MEMORY_DIR / "import_manifest.jsonl"
STRUCTURED_MEMORY_DIR = ROOT / "memory" / "structured"
REPORT_PATH = STRUCTURED_MEMORY_DIR / "memory_update_report.md"


CATEGORY_TERMS = {
    "New Facts": [
        "current",
        "cash",
        "holding",
        "portfolio",
        "tax",
        "income",
        "debt",
        "account",
    ],
    "Preferences": [
        "prefer",
        "preference",
        "style",
        "concise",
        "brutal",
        "tactical",
        "avoid",
        "like",
    ],
    "Open Loops": [
        "?",
        "should",
        "pending",
        "todo",
        "open loop",
        "decide",
        "decision",
        "compare",
    ],
    "Decisions Made": [
        "decided",
        "approved",
        "rejected",
        "will",
        "won't",
        "do not",
        "don't",
        "no ",
    ],
    "Risk Rules": [
        "risk",
        "loss",
        "drawdown",
        "speculative",
        "options",
        "trading",
        "threshold",
        "guardrail",
    ],
    "Tax Notes": [
        "tax",
        "after-tax",
        "state tax",
        "federal",
        "sgov",
        "t-bill",
        "hysa",
        "interest",
    ],
    "Watchlist Changes": [
        "watchlist",
        "track",
        "monitor",
        "stock",
        "etf",
        "btc",
        "nvda",
        "msft",
        "goog",
    ],
}


def load_manifest() -> list[dict[str, object]]:
    if not MANIFEST_PATH.exists():
        return []
    records = []
    for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def clean_line(line: str) -> str:
    return re.sub(r"\\s+", " ", line.strip())[:260]


def evidence_id(index: int, line_number: int) -> str:
    return f"S{index}:L{line_number}"


def collect_candidates(records: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    sections: dict[str, list[dict[str, object]]] = {
        category: [] for category in CATEGORY_TERMS
    }
    seen: set[tuple[str, str]] = set()

    for source_index, record in enumerate(records, start=1):
        stored_path = ROOT / str(record["stored_path"])
        text = stored_path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            normalized = clean_line(line)
            if not normalized:
                continue
            lowered = normalized.lower()
            for category, terms in CATEGORY_TERMS.items():
                if not any(term in lowered for term in terms):
                    continue
                key = (category, lowered)
                if key in seen:
                    continue
                seen.add(key)
                sections[category].append(
                    {
                        "text": normalized,
                        "evidence": evidence_id(source_index, line_number),
                        "source_name": record.get("source_name", "unknown"),
                        "source_path": record.get("stored_path", "unknown"),
                        "source_sha256": record.get("sha256", "unknown"),
                    }
                )
                break

    return {category: items[:10] for category, items in sections.items()}


def build_observability(records: list[dict[str, object]], sections: dict[str, list[dict[str, object]]]) -> list[str]:
    category_counts = Counter(
        {category: len(items) for category, items in sections.items()}
    )
    lines = [
        "## Pipeline Observability",
        "",
        f"- Raw imports reviewed: {len(records)}",
        f"- Proposed memory items: {sum(category_counts.values())}",
        "- Policy mutations: 0",
        "- Strategy mutations: 0",
        "- Status: review_only",
        "",
    ]
    for category in sections:
        lines.append(f"- {category}: {category_counts[category]}")
    return lines


def build_sources(records: list[dict[str, object]]) -> list[str]:
    lines = ["## Evidence Sources", ""]
    for source_index, record in enumerate(records, start=1):
        lines.extend(
            [
                f"### S{source_index}: {record.get('source_name', 'unknown')}",
                "",
                f"- stored path: `{record.get('stored_path', 'unknown')}`",
                f"- sha256: `{record.get('sha256', 'unknown')}`",
                f"- imported at: {record.get('imported_at', 'unknown')}",
                "",
            ]
        )
    return lines


def build_report(records: list[dict[str, object]]) -> str:
    sections = collect_candidates(records)
    lines = [
        "# Memory Update Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This report is review-only. It does not mutate policy, strategy, alerts, releases, or execution settings.",
        "",
    ]
    lines.extend(build_observability(records, sections))
    lines.extend(["", "## Proposed Memory Updates", ""])
    for category, items in sections.items():
        lines.extend([f"### {category}", ""])
        if not items:
            lines.extend(["- None detected.", ""])
            continue
        for item in items:
            lines.append(
                f"- {item['text']} "
                f"(evidence: {item['evidence']}, source: {item['source_name']}, sha256: {item['source_sha256']})"
            )
        lines.append("")
    lines.extend(build_sources(records))
    lines.extend(
        [
            "## Next Step",
            "",
            "Review these proposed memory updates before promoting anything into policy, strategy, alerts, or evolution proposals.",
            "",
        ]
    )
    return "\\n".join(lines)


def write_report(report: str) -> None:
    STRUCTURED_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a review-only memory update report from raw imported conversations.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Review all raw imports instead of only the latest import.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    records = load_manifest()
    if not records:
        print("No raw conversation imports found. Run import_conversation.py first.")
        return 1
    if not args.all:
        records = records[-1:]

    write_report(build_report(records))
    print(f"Wrote review-only memory update report to {REPORT_PATH}")
    print("No policy, strategy, alert, release, or execution settings were mutated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def write_functional_evolution_reporter(output_dir: Path) -> None:
    _write(
        output_dir / "functional_evolution_report.py",
        """from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re


ROOT = Path(__file__).parent
RAW_MEMORY_DIR = ROOT / "memory" / "raw"
MANIFEST_PATH = RAW_MEMORY_DIR / "import_manifest.jsonl"
EVOLUTION_DIR = ROOT / "evolution"
REPORT_PATH = EVOLUTION_DIR / "functional_evolution_report.md"


UPGRADE_RULES = [
    {
        "title": "Add Intent-State Classifier",
        "kind": "classifier",
        "terms": ["?", "should", "maybe", "thinking about", "curious", "explore"],
        "reason": "The input includes exploratory language that should not automatically become user intent.",
        "expected_benefit": "Separates curiosity, serious consideration, rejected ideas, approved strategy, and active behavior.",
        "risk": "May over-classify short notes unless evidence remains visible.",
    },
    {
        "title": "Add Cash Yield Optimization Extractor",
        "kind": "extractor",
        "terms": ["hysa", "sgov", "t-bill", "treasury", "interest", "state tax", "after-tax", "cash"],
        "reason": "The input discusses cash, yield, liquidity, or tax drag.",
        "expected_benefit": "Future reports can compare cash options using after-tax yield and liquidity assumptions.",
        "risk": "Could overfit to current interest rates unless the extractor records dates and assumptions.",
    },
    {
        "title": "Add Speculative Trading Risk Gate",
        "kind": "risk_gate",
        "terms": ["options", "trading", "agentic", "bot", "moonshot", "speculative", "max loss"],
        "reason": "The input includes high-risk trading or speculative allocation language.",
        "expected_benefit": "Keeps speculative ideas bounded by max loss, approved bucket size, backtesting, and tax review.",
        "risk": "Can become too restrictive if all exploration is treated as a live strategy.",
    },
    {
        "title": "Add AI Bottleneck Thesis Tracker",
        "kind": "schema",
        "terms": ["ai", "compute", "gpu", "nvda", "memory bandwidth", "networking", "power", "cooling", "photonics"],
        "reason": "The input mentions AI infrastructure or bottleneck investing themes.",
        "expected_benefit": "Tracks thesis dimensions separately from generic watchlist symbols.",
        "risk": "Theme extraction can become noisy without source evidence and confidence.",
    },
    {
        "title": "Add Contradiction Checker",
        "kind": "quality_check",
        "terms": ["but", "however", "instead", "changed my mind", "rejected", "avoid", "do not", "don't"],
        "reason": "The input includes reversal, rejection, or contrast language.",
        "expected_benefit": "Flags possible conflicts between prior rules, new statements, and current drafts.",
        "risk": "May flag ordinary nuance as conflict until reviewed by the user.",
    },
    {
        "title": "Require Evidence Anchors For Durable Memory",
        "kind": "evidence_requirement",
        "terms": ["preference", "rule", "decision", "watchlist", "risk", "tax", "portfolio"],
        "reason": "The input contains durable memory candidates.",
        "expected_benefit": "Prevents memory updates without source file, checksum, and line-level evidence.",
        "risk": "Adds review overhead, but keeps the system debuggable.",
    },
]


def load_manifest() -> list[dict[str, object]]:
    if not MANIFEST_PATH.exists():
        return []
    records = []
    for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def clean_line(line: str) -> str:
    return re.sub(r"\\s+", " ", line.strip())[:260]


def evidence_id(index: int, line_number: int) -> str:
    return f"S{index}:L{line_number}"


def matching_evidence(records: list[dict[str, object]], terms: list[str]) -> list[dict[str, object]]:
    matches = []
    seen: set[str] = set()
    for source_index, record in enumerate(records, start=1):
        stored_path = ROOT / str(record["stored_path"])
        text = stored_path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            normalized = clean_line(line)
            lowered = normalized.lower()
            if not normalized or not any(term in lowered for term in terms):
                continue
            key = f"{source_index}:{line_number}:{lowered}"
            if key in seen:
                continue
            seen.add(key)
            matches.append(
                {
                    "evidence": evidence_id(source_index, line_number),
                    "text": normalized,
                    "source_name": record.get("source_name", "unknown"),
                    "source_sha256": record.get("sha256", "unknown"),
                }
            )
            if len(matches) >= 5:
                return matches
    return matches


def build_recommendations(records: list[dict[str, object]]) -> list[dict[str, object]]:
    recommendations = []
    for rule in UPGRADE_RULES:
        evidence = matching_evidence(records, rule["terms"])
        if not evidence:
            continue
        recommendations.append(
            {
                **rule,
                "evidence": evidence,
                "status": "proposed_requires_approval",
                "activation": "not_active",
                "rollback_path": "Do not activate this upgrade until it is versioned; reject the proposal to keep current extraction behavior.",
            }
        )
    return recommendations


def build_report(records: list[dict[str, object]]) -> str:
    recommendations = build_recommendations(records)
    lines = [
        "# Functional Evolution Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This report is review-only. It recommends extractor, schema, classifier, scoring, or quality-check upgrades without activating them.",
        "",
        "## Pipeline Observability",
        "",
        f"- Raw imports reviewed: {len(records)}",
        f"- Functional upgrades proposed: {len(recommendations)}",
        "- Active extractor changes: 0",
        "- Policy mutations: 0",
        "- Strategy mutations: 0",
        "- Status: proposed_requires_approval",
        "",
        "## Proposed Functional Upgrades",
        "",
    ]
    if not recommendations:
        lines.extend(["- None detected.", ""])
    for index, recommendation in enumerate(recommendations, start=1):
        lines.extend(
            [
                f"### {index}. {recommendation['title']}",
                "",
                f"- kind: {recommendation['kind']}",
                f"- status: {recommendation['status']}",
                f"- activation: {recommendation['activation']}",
                f"- reason: {recommendation['reason']}",
                f"- expected benefit: {recommendation['expected_benefit']}",
                f"- risk: {recommendation['risk']}",
                f"- rollback path: {recommendation['rollback_path']}",
                "- evidence:",
            ]
        )
        for item in recommendation["evidence"]:
            lines.append(
                f"  - {item['evidence']} {item['text']} "
                f"(source: {item['source_name']}, sha256: {item['source_sha256']})"
            )
        lines.append("")
    lines.extend(
        [
            "## Approval Rule",
            "",
            "Approving this report should create a versioned extractor/schema proposal. It must not directly rewrite prompts, code, policy, or strategy.",
            "",
        ]
    )
    return "\\n".join(lines)


def write_report(report: str) -> None:
    EVOLUTION_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a review-only functional evolution report from raw imported conversations.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Review all raw imports instead of only the latest import.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    records = load_manifest()
    if not records:
        print("No raw conversation imports found. Run import_conversation.py first.")
        return 1
    if not args.all:
        records = records[-1:]

    write_report(build_report(records))
    print(f"Wrote review-only functional evolution report to {REPORT_PATH}")
    print("No extractor, schema, policy, strategy, alert, release, or execution settings were mutated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def write_extraction_observability_reporter(output_dir: Path) -> None:
    _write(
        output_dir / "extraction_observability.py",
        """from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re


ROOT = Path(__file__).parent
RAW_MANIFEST_PATH = ROOT / "memory" / "raw" / "import_manifest.jsonl"
DRAFTS_PATH = ROOT / "memory" / "structured" / "extraction_drafts.jsonl"
MEMORY_REPORT_PATH = ROOT / "memory" / "structured" / "memory_update_report.md"
FUNCTIONAL_REPORT_PATH = ROOT / "evolution" / "functional_evolution_report.md"
REPORT_PATH = ROOT / "memory" / "structured" / "extraction_observability.md"


CONFLICT_TERMS = ["but", "however", "rejected", "avoid", "do not", "don't", "changed my mind"]
EVIDENCE_PATTERN = re.compile(r"S\\d+:L\\d+")


def read_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def source_line_stats(records: list[dict[str, object]]) -> tuple[int, int, int]:
    total_lines = 0
    noisy_lines = 0
    conflict_lines = 0
    for record in records:
        path = ROOT / str(record.get("stored_path", ""))
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            normalized = line.strip()
            if not normalized:
                noisy_lines += 1
                continue
            total_lines += 1
            if len(normalized) < 12:
                noisy_lines += 1
            lowered = normalized.lower()
            if any(term in lowered for term in CONFLICT_TERMS):
                conflict_lines += 1
    return total_lines, noisy_lines, conflict_lines


def evidence_ids(*texts: str) -> list[str]:
    ids = []
    seen = set()
    for text in texts:
        for match in EVIDENCE_PATTERN.findall(text):
            if match not in seen:
                seen.add(match)
                ids.append(match)
    return ids


def build_report() -> str:
    raw_records = read_jsonl(RAW_MANIFEST_PATH)
    drafts = read_jsonl(DRAFTS_PATH)
    memory_report = read_text(MEMORY_REPORT_PATH)
    functional_report = read_text(FUNCTIONAL_REPORT_PATH)
    total_lines, noisy_lines, conflict_lines = source_line_stats(raw_records)
    low_confidence = [
        draft
        for draft in drafts
        if float(draft.get("confidence", 0) or 0) < 0.60
    ]
    ids = evidence_ids(memory_report, functional_report)

    lines = [
        "# Extraction Observability Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This report is review-only. It summarizes extraction quality, traceability, and source evidence without mutating memory or behavior.",
        "",
        "## Processing Summary",
        "",
        f"- Raw imports processed: {len(raw_records)}",
        f"- Source non-empty lines scanned: {total_lines}",
        f"- Rejected or noisy lines: {noisy_lines}",
        f"- Structured memory drafts: {len(drafts)}",
        f"- Low-confidence drafts: {len(low_confidence)}",
        f"- Conflict-signal lines: {conflict_lines}",
        f"- Evidence anchors found: {len(ids)}",
        "",
        "## Source Checksums",
        "",
    ]
    if not raw_records:
        lines.append("- None. Run `python import_conversation.py path/to/export.md` first.")
    for index, record in enumerate(raw_records, start=1):
        lines.append(
            f"- S{index}: `{record.get('source_name', 'unknown')}` "
            f"stored at `{record.get('stored_path', 'unknown')}`, sha256 `{record.get('sha256', 'unknown')}`"
        )

    lines.extend(["", "## Low-Confidence Items", ""])
    if not low_confidence:
        lines.append("- None.")
    for draft in low_confidence:
        lines.append(
            f"- {draft.get('source_name', 'unknown')}: confidence {float(draft.get('confidence', 0) or 0):.2f}, "
            f"status {draft.get('status', 'unknown')}, sha256 `{draft.get('source_sha256', 'unknown')}`"
        )

    lines.extend(["", "## Evidence Locations", ""])
    if ids:
        for evidence in ids[:50]:
            lines.append(f"- {evidence}")
    else:
        lines.append("- None found. Run memory and functional evolution reports first.")

    lines.extend(
        [
            "",
            "## Next Step",
            "",
            "Review noisy lines, low-confidence drafts, conflict signals, and evidence coverage before approving any memory or extractor evolution.",
            "",
        ]
    )
    return "\\n".join(lines)


def main() -> int:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report(), encoding="utf-8")
    print(f"Wrote extraction observability report to {REPORT_PATH}")
    print("No memory, policy, strategy, extractor, release, or execution settings were mutated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def generate_portfolio_blueprint(spec: AgentSpec, output_dir: Path) -> None:
    create_agent_directories(output_dir)
    (output_dir / "data").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    _write(
        output_dir / "README.md",
        f"""# {spec.name}

This is a local, alert-only Portfolio Manager Agent scaffold generated by Setup OS.

## v0 Scope

- read sample/local CSV holdings
- read sample/local CSV transactions
- read sample/local CSV cash balances
- read sample/local CSV watchlist entries
- read sample/local CSV market snapshots
- produce a Markdown daily report
- warn when any single holding is above 35% of the sample portfolio
- warn when an allocation differs from its target by more than 5 percentage points
- emit console-first recommendations
- keep broker credentials and trade execution out of scope
- preserve future changes as reviewable evolution proposals

## Commands

```bash
python import_portfolio_snapshot.py path/to/holdings.csv --source robinhood-readonly-export
python import_portfolio_transactions.py path/to/transactions.csv --source robinhood-readonly-export
python import_portfolio_cash.py path/to/cash.csv --source robinhood-readonly-export
python import_portfolio_watchlist.py path/to/watchlist.csv
python import_portfolio_market_data.py path/to/market_data.csv
python import_conversation.py path/to/chatgpt-finance-export.md
python extract_memory.py
python memory_update_report.py --all
python functional_evolution_report.py --all
python extraction_observability.py
python report.py
python health.py
python runtime_node.py --skip-report
python handoff.py
```

Raw conversation imports are stored in `memory/raw` and do not mutate strategy.
Structured memory drafts are written to `memory/structured` for review before promotion.
Memory update reports are written to `memory/structured/memory_update_report.md` with source evidence and no policy mutation.
Functional evolution reports are written to `evolution/functional_evolution_report.md` with proposed extractor upgrades that require approval.
Extraction observability reports are written to `memory/structured/extraction_observability.md` for traceability review.
ntfy push is available but disabled by default in `config.json`.
Portfolio snapshots, transactions, cash balances, watchlists, and market data are local CSV imports only; no broker credentials are stored.
`handoff.py` writes `handoff.md` as a local utility checklist for your laptop or always-on runtime node.

## Safety

{_bullet_list(spec.safety)}
""",
    )

    write_agent_metadata(spec, output_dir)
    write_portfolio_snapshot_importer(output_dir)
    write_portfolio_transaction_importer(output_dir)
    write_portfolio_cash_importer(output_dir)
    write_portfolio_watchlist_importer(output_dir)
    write_portfolio_market_data_importer(output_dir)

    _write(
        output_dir / "data" / "holdings.csv",
        """symbol,name,quantity,price,cost_basis
VOO,Vanguard S&P 500 ETF,10,500.00,4700.00
VXUS,Vanguard Total International Stock ETF,20,62.00,1180.00
BND,Vanguard Total Bond Market ETF,15,73.00,1110.00
""",
    )

    _write(
        output_dir / "data" / "allocation_targets.csv",
        """symbol,target_weight
VOO,0.60
VXUS,0.25
BND,0.15
""",
    )

    _write(
        output_dir / "data" / "transactions.csv",
        """date,symbol,action,quantity,price,fees
2026-06-15,VOO,buy,1,500.00,0.00
2026-06-20,VXUS,buy,2,62.00,0.00
2026-06-25,BND,buy,1,73.00,0.00
""",
    )

    _write(
        output_dir / "data" / "cash.csv",
        """account,currency,balance
brokerage,USD,250.00
""",
    )

    _write(
        output_dir / "data" / "watchlist.csv",
        """symbol,rationale,alert_note
AAPL,Quality compounder to review,Watch valuation before adding
MSFT,AI and cloud exposure,Review concentration if added
""",
    )

    _write(
        output_dir / "data" / "market_data.csv",
        """symbol,price,as_of,event_note
VOO,505.00,2026-06-30,Updated local price snapshot
VXUS,61.50,2026-06-30,International allocation review
BND,73.25,2026-06-30,Bond sleeve steady
""",
    )

    _write(
        output_dir / "report.py",
        """from __future__ import annotations

import csv
from datetime import date
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "holdings.csv"
TARGETS_PATH = ROOT / "data" / "allocation_targets.csv"
TRANSACTIONS_PATH = ROOT / "data" / "transactions.csv"
CASH_PATH = ROOT / "data" / "cash.csv"
WATCHLIST_PATH = ROOT / "data" / "watchlist.csv"
MARKET_DATA_PATH = ROOT / "data" / "market_data.csv"
REPORT_PATH = ROOT / "reports" / "daily_report.md"
INBOX_PATH = ROOT / ".setup_os" / "notifications.jsonl"
CONFIG_PATH = ROOT / "config.json"


def load_config() -> dict:
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def notify(title: str, body: str, severity: str = "info") -> None:
    print(f"NOTIFY[{severity}]: {title} - {body}")
    INBOX_PATH.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "portfolio-manager-agent",
        "title": title,
        "body": body,
        "severity": severity,
        "status": "new",
    }
    with INBOX_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, sort_keys=True) + "\\n")
    send_ntfy(title, body, severity)


def send_ntfy(title: str, body: str, severity: str) -> None:
    ntfy_config = load_config().get("notification_channels", {}).get("ntfy", {})
    if not ntfy_config.get("enabled", False):
        return

    topic = os.environ.get(ntfy_config.get("topic_env", "SETUP_OS_NTFY_TOPIC"), "")
    if not topic:
        print("NTFY[skipped]: topic environment variable is not set")
        return

    server = ntfy_config.get("server", "https://ntfy.sh").rstrip("/")
    request = Request(
        f"{server}/{quote(topic, safe='')}",
        data=body.encode("utf-8"),
        method="POST",
        headers={"Title": title, "Tags": severity},
    )
    try:
        with urlopen(request, timeout=5):
            pass
        print(f"NTFY[sent]: {title}")
    except URLError as error:
        print(f"NTFY[failed]: {error}")


def load_holdings() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_targets() -> dict[str, float]:
    if not TARGETS_PATH.exists():
        return {}
    with TARGETS_PATH.open(newline="", encoding="utf-8") as file:
        return {
            row["symbol"]: float(row["target_weight"])
            for row in csv.DictReader(file)
            if row.get("symbol") and row.get("target_weight")
        }


def load_transactions() -> list[dict[str, str]]:
    if not TRANSACTIONS_PATH.exists():
        return []
    with TRANSACTIONS_PATH.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_cash() -> list[dict[str, str]]:
    if not CASH_PATH.exists():
        return []
    with CASH_PATH.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_watchlist() -> list[dict[str, str]]:
    if not WATCHLIST_PATH.exists():
        return []
    with WATCHLIST_PATH.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_market_data() -> dict[str, dict[str, str]]:
    if not MARKET_DATA_PATH.exists():
        return {}
    with MARKET_DATA_PATH.open(newline="", encoding="utf-8") as file:
        return {
            row["symbol"]: row
            for row in csv.DictReader(file)
            if row.get("symbol") and row.get("price")
        }


def main() -> int:
    holdings = load_holdings()
    targets = load_targets()
    transactions = load_transactions()
    cash_balances = load_cash()
    watchlist = load_watchlist()
    market_data = load_market_data()
    holdings_value = sum(
        float(row["quantity"]) * float(market_data.get(row["symbol"], row)["price"])
        for row in holdings
    )
    holdings_cost_basis = sum(float(row["cost_basis"]) for row in holdings)
    unrealized_gain_loss = holdings_value - holdings_cost_basis
    unrealized_return = (
        unrealized_gain_loss / holdings_cost_basis if holdings_cost_basis else 0
    )
    cash_value = sum(float(row["balance"]) for row in cash_balances if row["currency"] == "USD")
    total_value = holdings_value + cash_value
    concentration_threshold = 0.35
    drift_threshold = 0.05
    concentration_alerts = []
    drift_alerts = []

    lines = [
        "# Daily Portfolio Report",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        f"Total sample portfolio value: ${total_value:,.2f}",
        f"Holdings value: ${holdings_value:,.2f}",
        f"Cash value: ${cash_value:,.2f}",
        "",
        "## Performance Summary",
        "",
        f"Holdings cost basis: ${holdings_cost_basis:,.2f}",
        f"Unrealized gain/loss: ${unrealized_gain_loss:,.2f} ({unrealized_return:+.1%})",
        "",
        "## Holdings",
        "",
    ]

    for row in holdings:
        market_row = market_data.get(row["symbol"], {})
        price = float(market_row.get("price", row["price"]))
        value = float(row["quantity"]) * price
        cost_basis = float(row["cost_basis"])
        gain_loss = value - cost_basis
        return_pct = gain_loss / cost_basis if cost_basis else 0
        weight = value / total_value if total_value else 0
        price_note = "market snapshot" if market_row else "holding file"
        lines.append(
            f"- {row['symbol']}: ${value:,.2f} ({weight:.1%}, {price_note} price ${price:,.2f}, "
            f"unrealized ${gain_loss:,.2f} / {return_pct:+.1%})"
        )
        if weight > concentration_threshold:
            concentration_alerts.append(
                f"{row['symbol']} is {weight:.1%} of the portfolio, above the 35.0% review threshold."
            )
        target_weight = targets.get(row["symbol"])
        if target_weight is not None and abs(weight - target_weight) > drift_threshold:
            drift_alerts.append(
                f"{row['symbol']} is {weight:.1%} vs target {target_weight:.1%}, a {weight - target_weight:+.1%} drift."
            )

    lines.extend(
        [
            "",
            "## Market Snapshot",
            "",
        ]
    )
    if market_data:
        for symbol, row in sorted(market_data.items()):
            note = row.get("event_note", "")
            lines.append(f"- {symbol}: ${float(row['price']):,.2f} as of {row.get('as_of', 'unknown')} - {note}")
    else:
        lines.append("- None imported.")

    lines.extend(
        [
            "",
            "## Cash",
            "",
        ]
    )
    if cash_balances:
        for row in cash_balances:
            lines.append(f"- {row['account']}: {row['currency']} {float(row['balance']):,.2f}")
    else:
        lines.append("- None imported.")

    lines.extend(
        [
            "",
            "## Watchlist",
            "",
        ]
    )
    if watchlist:
        for row in watchlist:
            lines.append(f"- {row['symbol']}: {row['rationale']} ({row['alert_note']})")
    else:
        lines.append("- None imported.")

    lines.extend(
        [
            "",
            "## Recent Transactions",
            "",
        ]
    )
    if transactions:
        for row in transactions[-5:]:
            amount = float(row["quantity"]) * float(row["price"]) + float(row.get("fees", 0) or 0)
            lines.append(
                f"- {row['date']} {row['action'].upper()} {row['quantity']} {row['symbol']} @ ${float(row['price']):,.2f} (${amount:,.2f})"
            )
    else:
        lines.append("- None imported.")

    lines.extend(
        [
            "",
            "## Allocation Drift Alerts",
            "",
        ]
    )
    if drift_alerts:
        for alert in drift_alerts:
            lines.append(f"- WARNING: {alert}")
    else:
        lines.append("- None. No target allocation is outside the 5.0 percentage point review band.")

    lines.extend(
        [
            "",
            "## Concentration Alerts",
            "",
        ]
    )
    if concentration_alerts:
        for alert in concentration_alerts:
            lines.append(f"- WARNING: {alert}")
    else:
        lines.append("- None. No single holding is above the 35.0% review threshold.")

    lines.extend(
        [
            "",
            "## Console Notification",
            "",
            "Portfolio report generated. Review allocation drift before taking action.",
        ]
    )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\\n".join(lines) + "\\n", encoding="utf-8")
    print(f"Wrote {REPORT_PATH}")
    notify(
        "Portfolio report generated",
        "Manual review required before trades.",
        "info",
    )
    for alert in concentration_alerts:
        notify(
            "Portfolio concentration review",
            alert,
            "warning",
        )
    for alert in drift_alerts:
        notify(
            "Portfolio allocation drift review",
            alert,
            "warning",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def write_portfolio_snapshot_importer(output_dir: Path) -> None:
    _write(
        output_dir / "import_portfolio_snapshot.py",
        """from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
HOLDINGS_PATH = DATA_DIR / "holdings.csv"
MANIFEST_PATH = DATA_DIR / "portfolio_import_manifest.jsonl"
REQUIRED_COLUMNS = ["symbol", "name", "quantity", "price", "cost_basis"]


def validate_holdings(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        rows = list(reader)

    if not rows:
        raise ValueError("holdings CSV must contain at least one row")

    for index, row in enumerate(rows, start=2):
        if not row["symbol"].strip():
            raise ValueError(f"row {index} is missing symbol")
        for column in ["quantity", "price", "cost_basis"]:
            try:
                float(row[column])
            except ValueError as error:
                raise ValueError(f"row {index} has invalid {column}: {row[column]}") from error
    return rows


def import_snapshot(source: Path, source_type: str) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    if not source.is_file():
        raise IsADirectoryError(source)

    rows = validate_holdings(source)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if HOLDINGS_PATH.exists():
        backup_path = DATA_DIR / "holdings.previous.csv"
        shutil.copy2(HOLDINGS_PATH, backup_path)
    shutil.copy2(source, HOLDINGS_PATH)

    total_value = sum(float(row["quantity"]) * float(row["price"]) for row in rows)
    record = {
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source_path": str(source),
        "source_type": source_type,
        "stored_path": str(HOLDINGS_PATH.relative_to(ROOT)),
        "row_count": len(rows),
        "total_value": round(total_value, 2),
        "mode": "read_only_snapshot",
        "credentials_stored": False,
        "next_step": "Run report.py to review advisory alerts before taking any action.",
    }
    with MANIFEST_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, sort_keys=True) + "\\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Import a read-only portfolio holdings CSV snapshot into local data.",
    )
    parser.add_argument("holdings_csv", help="Path to a holdings CSV export.")
    parser.add_argument(
        "--source",
        default="manual-export",
        help="Source label, for example manual-export or robinhood-readonly-export.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    import_snapshot(Path(args.holdings_csv), args.source)
    print(f"Imported portfolio snapshot to {HOLDINGS_PATH}")
    print(f"Updated {MANIFEST_PATH}")
    print("No broker credentials were stored.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def write_portfolio_transaction_importer(output_dir: Path) -> None:
    _write(
        output_dir / "import_portfolio_transactions.py",
        """from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
TRANSACTIONS_PATH = DATA_DIR / "transactions.csv"
MANIFEST_PATH = DATA_DIR / "transaction_import_manifest.jsonl"
REQUIRED_COLUMNS = ["date", "symbol", "action", "quantity", "price", "fees"]


def validate_transactions(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        rows = list(reader)

    if not rows:
        raise ValueError("transactions CSV must contain at least one row")

    for index, row in enumerate(rows, start=2):
        if not row["date"].strip():
            raise ValueError(f"row {index} is missing date")
        if not row["symbol"].strip():
            raise ValueError(f"row {index} is missing symbol")
        if row["action"].strip().lower() not in {"buy", "sell", "dividend", "deposit", "withdrawal", "fee"}:
            raise ValueError(f"row {index} has unsupported action: {row['action']}")
        for column in ["quantity", "price", "fees"]:
            try:
                float(row[column])
            except ValueError as error:
                raise ValueError(f"row {index} has invalid {column}: {row[column]}") from error
    return rows


def import_transactions(source: Path, source_type: str) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    if not source.is_file():
        raise IsADirectoryError(source)

    rows = validate_transactions(source)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if TRANSACTIONS_PATH.exists():
        backup_path = DATA_DIR / "transactions.previous.csv"
        shutil.copy2(TRANSACTIONS_PATH, backup_path)
    shutil.copy2(source, TRANSACTIONS_PATH)

    gross_value = sum(float(row["quantity"]) * float(row["price"]) for row in rows)
    record = {
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source_path": str(source),
        "source_type": source_type,
        "stored_path": str(TRANSACTIONS_PATH.relative_to(ROOT)),
        "row_count": len(rows),
        "gross_value": round(gross_value, 2),
        "mode": "read_only_transactions",
        "credentials_stored": False,
        "next_step": "Run report.py to review recent activity before taking any action.",
    }
    with MANIFEST_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, sort_keys=True) + "\\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Import a read-only portfolio transactions CSV snapshot into local data.",
    )
    parser.add_argument("transactions_csv", help="Path to a transactions CSV export.")
    parser.add_argument(
        "--source",
        default="manual-export",
        help="Source label, for example manual-export or robinhood-readonly-export.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    import_transactions(Path(args.transactions_csv), args.source)
    print(f"Imported portfolio transactions to {TRANSACTIONS_PATH}")
    print(f"Updated {MANIFEST_PATH}")
    print("No broker credentials were stored.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def write_portfolio_cash_importer(output_dir: Path) -> None:
    _write(
        output_dir / "import_portfolio_cash.py",
        """from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
CASH_PATH = DATA_DIR / "cash.csv"
MANIFEST_PATH = DATA_DIR / "cash_import_manifest.jsonl"
REQUIRED_COLUMNS = ["account", "currency", "balance"]


def validate_cash(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        rows = list(reader)

    if not rows:
        raise ValueError("cash CSV must contain at least one row")

    for index, row in enumerate(rows, start=2):
        if not row["account"].strip():
            raise ValueError(f"row {index} is missing account")
        if not row["currency"].strip():
            raise ValueError(f"row {index} is missing currency")
        try:
            float(row["balance"])
        except ValueError as error:
            raise ValueError(f"row {index} has invalid balance: {row['balance']}") from error
    return rows


def import_cash(source: Path, source_type: str) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    if not source.is_file():
        raise IsADirectoryError(source)

    rows = validate_cash(source)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if CASH_PATH.exists():
        backup_path = DATA_DIR / "cash.previous.csv"
        shutil.copy2(CASH_PATH, backup_path)
    shutil.copy2(source, CASH_PATH)

    total_balance = sum(float(row["balance"]) for row in rows)
    record = {
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source_path": str(source),
        "source_type": source_type,
        "stored_path": str(CASH_PATH.relative_to(ROOT)),
        "row_count": len(rows),
        "total_balance": round(total_balance, 2),
        "mode": "read_only_cash",
        "credentials_stored": False,
        "next_step": "Run report.py to review total portfolio value before taking any action.",
    }
    with MANIFEST_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, sort_keys=True) + "\\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Import a read-only cash balance CSV snapshot into local data.",
    )
    parser.add_argument("cash_csv", help="Path to a cash balance CSV export.")
    parser.add_argument(
        "--source",
        default="manual-export",
        help="Source label, for example manual-export or robinhood-readonly-export.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    import_cash(Path(args.cash_csv), args.source)
    print(f"Imported cash balances to {CASH_PATH}")
    print(f"Updated {MANIFEST_PATH}")
    print("No broker credentials were stored.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def write_portfolio_watchlist_importer(output_dir: Path) -> None:
    _write(
        output_dir / "import_portfolio_watchlist.py",
        """from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
WATCHLIST_PATH = DATA_DIR / "watchlist.csv"
MANIFEST_PATH = DATA_DIR / "watchlist_import_manifest.jsonl"
REQUIRED_COLUMNS = ["symbol", "rationale", "alert_note"]


def validate_watchlist(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        rows = list(reader)

    if not rows:
        raise ValueError("watchlist CSV must contain at least one row")

    for index, row in enumerate(rows, start=2):
        if not row["symbol"].strip():
            raise ValueError(f"row {index} is missing symbol")
        if not row["rationale"].strip():
            raise ValueError(f"row {index} is missing rationale")
    return rows


def import_watchlist(source: Path, source_type: str) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    if not source.is_file():
        raise IsADirectoryError(source)

    rows = validate_watchlist(source)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if WATCHLIST_PATH.exists():
        backup_path = DATA_DIR / "watchlist.previous.csv"
        shutil.copy2(WATCHLIST_PATH, backup_path)
    shutil.copy2(source, WATCHLIST_PATH)

    record = {
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source_path": str(source),
        "source_type": source_type,
        "stored_path": str(WATCHLIST_PATH.relative_to(ROOT)),
        "row_count": len(rows),
        "mode": "read_only_watchlist",
        "credentials_stored": False,
        "next_step": "Run report.py to review watchlist notes before adding enrichment.",
    }
    with MANIFEST_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, sort_keys=True) + "\\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Import a read-only watchlist CSV snapshot into local data.",
    )
    parser.add_argument("watchlist_csv", help="Path to a watchlist CSV export.")
    parser.add_argument(
        "--source",
        default="manual-export",
        help="Source label, for example manual-export or conversation-draft.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    import_watchlist(Path(args.watchlist_csv), args.source)
    print(f"Imported watchlist to {WATCHLIST_PATH}")
    print(f"Updated {MANIFEST_PATH}")
    print("No broker credentials were stored.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def write_portfolio_market_data_importer(output_dir: Path) -> None:
    _write(
        output_dir / "import_portfolio_market_data.py",
        """from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
MARKET_DATA_PATH = DATA_DIR / "market_data.csv"
MANIFEST_PATH = DATA_DIR / "market_data_import_manifest.jsonl"
REQUIRED_COLUMNS = ["symbol", "price", "as_of", "event_note"]


def validate_market_data(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        rows = list(reader)

    if not rows:
        raise ValueError("market data CSV must contain at least one row")

    for index, row in enumerate(rows, start=2):
        if not row["symbol"].strip():
            raise ValueError(f"row {index} is missing symbol")
        if not row["as_of"].strip():
            raise ValueError(f"row {index} is missing as_of")
        try:
            float(row["price"])
        except ValueError as error:
            raise ValueError(f"row {index} has invalid price: {row['price']}") from error
    return rows


def import_market_data(source: Path, source_type: str) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    if not source.is_file():
        raise IsADirectoryError(source)

    rows = validate_market_data(source)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if MARKET_DATA_PATH.exists():
        backup_path = DATA_DIR / "market_data.previous.csv"
        shutil.copy2(MARKET_DATA_PATH, backup_path)
    shutil.copy2(source, MARKET_DATA_PATH)

    record = {
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source_path": str(source),
        "source_type": source_type,
        "stored_path": str(MARKET_DATA_PATH.relative_to(ROOT)),
        "row_count": len(rows),
        "mode": "read_only_market_snapshot",
        "credentials_stored": False,
        "next_step": "Run report.py to review market snapshot effects before taking any action.",
    }
    with MANIFEST_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, sort_keys=True) + "\\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Import a read-only market data CSV snapshot into local data.",
    )
    parser.add_argument("market_data_csv", help="Path to a market data CSV export.")
    parser.add_argument(
        "--source",
        default="manual-export",
        help="Source label, for example manual-export or openbb-export.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    import_market_data(Path(args.market_data_csv), args.source)
    print(f"Imported market data to {MARKET_DATA_PATH}")
    print(f"Updated {MANIFEST_PATH}")
    print("No broker credentials were stored.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def generate_health_blueprint(spec: AgentSpec, output_dir: Path) -> None:
    create_agent_directories(output_dir)
    (output_dir / "data").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    _write(
        output_dir / "README.md",
        f"""# {spec.name}

This is a local, advisory Health OS scaffold generated by Setup OS.

## v0 Scope

- read sample/local health notes and habit logs
- produce a Markdown wellness report
- collect questions for clinician review
- avoid diagnosis, medication changes, or emergency handling
- preserve future changes as reviewable evolution proposals

## Commands

```bash
python import_conversation.py path/to/health-notes-export.md
python extract_memory.py
python memory_update_report.py --all
python functional_evolution_report.py --all
python extraction_observability.py
python report.py
python health.py
python runtime_node.py --skip-report
python handoff.py
```

Raw conversation imports are stored in `memory/raw` and do not mutate behavior.
Structured memory drafts are written to `memory/structured` for review before promotion.
Memory update reports are written to `memory/structured/memory_update_report.md` with source evidence and no behavior mutation.
Functional evolution reports are written to `evolution/functional_evolution_report.md` with proposed extractor upgrades that require approval.
Extraction observability reports are written to `memory/structured/extraction_observability.md` for traceability review.
ntfy push is available but disabled by default in `config.json`.
`handoff.py` writes `handoff.md` as a local utility checklist for your laptop or always-on runtime node.

## Safety

{_bullet_list(spec.safety)}
""",
    )

    write_agent_metadata(spec, output_dir)

    _write(
        output_dir / "data" / "health_notes.csv",
        """date,category,note
2026-06-30,sleep,Slept 7 hours and woke up once.
2026-06-30,exercise,Walked 30 minutes.
2026-06-30,question,Ask clinician about recurring shoulder tightness.
""",
    )

    _write(
        output_dir / "report.py",
        """from __future__ import annotations

import csv
from datetime import date
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "health_notes.csv"
REPORT_PATH = ROOT / "reports" / "wellness_report.md"
INBOX_PATH = ROOT / ".setup_os" / "notifications.jsonl"
CONFIG_PATH = ROOT / "config.json"


def load_config() -> dict:
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def notify(title: str, body: str, severity: str = "info") -> None:
    print(f"NOTIFY[{severity}]: {title} - {body}")
    INBOX_PATH.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "health-os-agent",
        "title": title,
        "body": body,
        "severity": severity,
        "status": "new",
    }
    with INBOX_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, sort_keys=True) + "\\n")
    send_ntfy(title, body, severity)


def send_ntfy(title: str, body: str, severity: str) -> None:
    ntfy_config = load_config().get("notification_channels", {}).get("ntfy", {})
    if not ntfy_config.get("enabled", False):
        return

    topic = os.environ.get(ntfy_config.get("topic_env", "SETUP_OS_NTFY_TOPIC"), "")
    if not topic:
        print("NTFY[skipped]: topic environment variable is not set")
        return

    server = ntfy_config.get("server", "https://ntfy.sh").rstrip("/")
    request = Request(
        f"{server}/{quote(topic, safe='')}",
        data=body.encode("utf-8"),
        method="POST",
        headers={"Title": title, "Tags": severity},
    )
    try:
        with urlopen(request, timeout=5):
            pass
        print(f"NTFY[sent]: {title}")
    except URLError as error:
        print(f"NTFY[failed]: {error}")


def load_notes() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def main() -> int:
    notes = load_notes()
    questions = [row for row in notes if row["category"] == "question"]

    lines = [
        "# Daily Wellness Report",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        "This report is advisory and is not medical advice.",
        "",
        "## Notes",
        "",
    ]

    for row in notes:
        lines.append(f"- {row['date']} [{row['category']}]: {row['note']}")

    lines.extend(["", "## Questions For Clinician", ""])
    if questions:
        for row in questions:
            lines.append(f"- {row['note']}")
    else:
        lines.append("- None recorded.")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\\n".join(lines) + "\\n", encoding="utf-8")
    print(f"Wrote {REPORT_PATH}")
    notify(
        "Wellness report generated",
        "Review notes and clinician questions. This is not medical advice.",
        "info",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
    )


def _write(path: Path, content: str) -> None:
    path.write_text(dedent(content).lstrip(), encoding="utf-8")


def _bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)
