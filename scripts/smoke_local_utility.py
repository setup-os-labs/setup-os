from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"command failed in {cwd}: {' '.join(command)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result.stdout


def require_file(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f"missing expected file: {path}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="setup-os-local-utility-") as temp_dir:
        output = Path(temp_dir) / "portfolio-os"

        run(
            [
                sys.executable,
                "-m",
                "setup_os.cli",
                "create",
                "examples/portfolio_conversation.md",
                "-o",
                str(output),
            ],
            ROOT,
        )

        for relative_path in [
            "README.md",
            "health.py",
            "report.py",
            "runtime_node.py",
            "handoff.py",
            "import_conversation.py",
            "extract_memory.py",
            "memory_update_report.py",
            "functional_evolution_report.py",
            "data/holdings.csv",
            "data/transactions.csv",
            "data/cash.csv",
            "data/watchlist.csv",
            "data/market_data.csv",
        ]:
            require_file(output / relative_path)

        run([sys.executable, "health.py"], output)
        run([sys.executable, "report.py"], output)
        run([sys.executable, "runtime_node.py", "--skip-report"], output)
        run(
            [
                sys.executable,
                "import_conversation.py",
                str(ROOT / "examples" / "portfolio_update.md"),
            ],
            output,
        )
        run([sys.executable, "extract_memory.py"], output)
        run([sys.executable, "memory_update_report.py", "--all"], output)
        run([sys.executable, "functional_evolution_report.py", "--all"], output)
        run([sys.executable, "handoff.py"], output)

        for relative_path in [
            "reports/daily_report.md",
            ".setup_os/runtime_node.jsonl",
            "memory/raw/import_manifest.jsonl",
            "memory/structured/extraction_drafts.jsonl",
            "memory/structured/memory_update_report.md",
            "evolution/functional_evolution_report.md",
            "handoff.md",
        ]:
            require_file(output / relative_path)

        report = (output / "reports" / "daily_report.md").read_text(encoding="utf-8")
        if "## Holdings" not in report or "## Market Snapshot" not in report:
            raise AssertionError("generated report is missing expected Portfolio sections")

        handoff = (output / "handoff.md").read_text(encoding="utf-8")
        if "Local Utility Handoff" not in handoff or "Runtime cycles:" not in handoff:
            raise AssertionError("local utility handoff is missing expected readiness details")

    print("Setup OS local utility smoke test OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
