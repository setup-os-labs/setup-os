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
    write_conversation_importer(output_dir)
    write_memory_extractor(output_dir)


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
    "report.py",
    "health.py",
    "runtime_node.py",
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
    "report.py",
    "verify.py",
    "runtime_node.py",
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
python report.py
python health.py
python runtime_node.py --skip-report
```

Raw conversation imports are stored in `memory/raw` and do not mutate strategy.
Structured memory drafts are written to `memory/structured` for review before promotion.
ntfy push is available but disabled by default in `config.json`.
Portfolio snapshots, transactions, cash balances, watchlists, and market data are local CSV imports only; no broker credentials are stored.

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
python report.py
python health.py
python runtime_node.py --skip-report
```

Raw conversation imports are stored in `memory/raw` and do not mutate behavior.
Structured memory drafts are written to `memory/structured` for review before promotion.
ntfy push is available but disabled by default in `config.json`.

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
