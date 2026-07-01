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
    "report.py",
    "health.py",
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
    "report.py",
    "verify.py",
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
- produce a Markdown daily report
- emit console-first recommendations
- keep broker credentials and trade execution out of scope
- preserve future changes as reviewable evolution proposals

## Commands

```bash
python report.py
python health.py
```

## Safety

{_bullet_list(spec.safety)}
""",
    )

    write_agent_metadata(spec, output_dir)

    _write(
        output_dir / "data" / "holdings.csv",
        """symbol,name,quantity,price,cost_basis
VOO,Vanguard S&P 500 ETF,10,500.00,4700.00
VXUS,Vanguard Total International Stock ETF,20,62.00,1180.00
BND,Vanguard Total Bond Market ETF,15,73.00,1110.00
""",
    )

    _write(
        output_dir / "report.py",
        """from __future__ import annotations

import csv
from datetime import date
from datetime import datetime, timezone
import json
from pathlib import Path


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "holdings.csv"
REPORT_PATH = ROOT / "reports" / "daily_report.md"
INBOX_PATH = ROOT / ".setup_os" / "notifications.jsonl"


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


def load_holdings() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def main() -> int:
    holdings = load_holdings()
    total_value = sum(float(row["quantity"]) * float(row["price"]) for row in holdings)

    lines = [
        "# Daily Portfolio Report",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        f"Total sample portfolio value: ${total_value:,.2f}",
        "",
        "## Holdings",
        "",
    ]

    for row in holdings:
        value = float(row["quantity"]) * float(row["price"])
        weight = value / total_value if total_value else 0
        lines.append(f"- {row['symbol']}: ${value:,.2f} ({weight:.1%})")

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
python report.py
python health.py
```

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
from pathlib import Path


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "health_notes.csv"
REPORT_PATH = ROOT / "reports" / "wellness_report.md"
INBOX_PATH = ROOT / ".setup_os" / "notifications.jsonl"


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
