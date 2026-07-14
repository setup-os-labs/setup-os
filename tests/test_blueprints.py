from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class BlueprintTests(unittest.TestCase):
    def test_create_generates_portfolio_blueprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "setup_os.cli",
                    "create",
                    "examples/portfolio_conversation.md",
                    "--output",
                    tmpdir,
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            output = Path(tmpdir)
            self.assertEqual(result.returncode, 0)
            self.assertTrue((output / "README.md").exists())
            self.assertTrue((output / "config.json").exists())
            self.assertTrue((output / "agent_dna.json").exists())
            self.assertTrue((output / "data" / "holdings.csv").exists())
            self.assertTrue((output / "data" / "allocation_targets.csv").exists())
            self.assertTrue((output / "data" / "transactions.csv").exists())
            self.assertTrue((output / "data" / "cash.csv").exists())
            self.assertTrue((output / "data" / "watchlist.csv").exists())
            self.assertTrue((output / "data" / "market_data.csv").exists())
            self.assertTrue((output / "import_portfolio_snapshot.py").exists())
            self.assertTrue((output / "import_portfolio_transactions.py").exists())
            self.assertTrue((output / "import_portfolio_cash.py").exists())
            self.assertTrue((output / "import_portfolio_watchlist.py").exists())
            self.assertTrue((output / "import_portfolio_market_data.py").exists())
            self.assertTrue((output / "import_conversation.py").exists())
            self.assertTrue((output / "extract_memory.py").exists())
            self.assertTrue((output / "memory_update_report.py").exists())
            self.assertTrue((output / "functional_evolution_report.py").exists())
            self.assertTrue((output / "extraction_observability.py").exists())
            self.assertTrue((output / "extractor_versioning.py").exists())
            self.assertTrue((output / "weekly_review.py").exists())
            self.assertTrue((output / "review_packet.py").exists())
            self.assertTrue((output / "report.py").exists())
            self.assertTrue((output / "verify.py").exists())
            self.assertTrue((output / "health.py").exists())
            self.assertTrue((output / "runtime_node.py").exists())
            self.assertTrue((output / "handoff.py").exists())
            self.assertTrue((output / "memory" / "raw").is_dir())
            self.assertTrue((output / "evolution").is_dir())
            config = json.loads((output / "config.json").read_text(encoding="utf-8"))
            ntfy_config = config["notification_channels"]["ntfy"]
            self.assertFalse(ntfy_config["enabled"])
            self.assertEqual(ntfy_config["topic_env"], "SETUP_OS_NTFY_TOPIC")

            report = subprocess.run(
                [sys.executable, "report.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(report.returncode, 0)
            report_text = (output / "reports" / "daily_report.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("## Performance Summary", report_text)
            self.assertIn("Holdings cost basis:", report_text)
            self.assertIn("Unrealized gain/loss:", report_text)
            self.assertIn("## Allocation Drift Alerts", report_text)
            self.assertIn("vs target", report_text)
            self.assertIn("## Concentration Alerts", report_text)
            self.assertIn("VOO is", report_text)
            self.assertIn("## Cash", report_text)
            self.assertIn("Cash value:", report_text)
            self.assertIn("## Watchlist", report_text)
            self.assertIn("## Market Snapshot", report_text)
            self.assertTrue((output / ".setup_os" / "notifications.jsonl").exists())
            self.assertIn("NOTIFY[info]:", report.stdout)
            self.assertIn("NOTIFY[warning]:", report.stdout)
            self.assertNotIn("NTFY[sent]", report.stdout)

            runtime_node = subprocess.run(
                [sys.executable, "runtime_node.py", "--skip-report"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(runtime_node.returncode, 0)
            self.assertIn("Runtime node run complete.", runtime_node.stdout)
            self.assertIn("OK: health", runtime_node.stdout)
            runtime_log_path = output / ".setup_os" / "runtime_node.jsonl"
            self.assertTrue(runtime_log_path.exists())
            runtime_log = [
                json.loads(line)
                for line in runtime_log_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(runtime_log[0]["event"], "runtime_node_run_once")
            self.assertEqual(runtime_log[0]["mode"], "personal_runtime_node")

            handoff = subprocess.run(
                [sys.executable, "handoff.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(handoff.returncode, 0)
            handoff_text = (output / "handoff.md").read_text(encoding="utf-8")
            self.assertIn("# Local Utility Handoff", handoff_text)
            self.assertIn("Latest runtime node cycle passed", handoff_text)
            self.assertIn("Notifications:", handoff_text)

            import_snapshot = subprocess.run(
                [
                    sys.executable,
                    "import_portfolio_snapshot.py",
                    str(Path.cwd() / "examples" / "portfolio_snapshot.csv"),
                    "--source",
                    "robinhood-readonly-export",
                ],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(import_snapshot.returncode, 0)
            self.assertIn("No broker credentials were stored.", import_snapshot.stdout)

            import_manifest_path = output / "data" / "portfolio_import_manifest.jsonl"
            self.assertTrue(import_manifest_path.exists())
            import_manifest = [
                json.loads(line)
                for line in import_manifest_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(import_manifest[0]["source_type"], "robinhood-readonly-export")
            self.assertFalse(import_manifest[0]["credentials_stored"])
            self.assertEqual(import_manifest[0]["mode"], "read_only_snapshot")

            imported_report = subprocess.run(
                [sys.executable, "report.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            imported_report_text = (output / "reports" / "daily_report.md").read_text(
                encoding="utf-8"
            )
            self.assertEqual(imported_report.returncode, 0)
            self.assertIn("AAPL", imported_report_text)
            self.assertIn("## Recent Transactions", imported_report_text)

            import_transactions = subprocess.run(
                [
                    sys.executable,
                    "import_portfolio_transactions.py",
                    str(Path.cwd() / "examples" / "portfolio_transactions.csv"),
                    "--source",
                    "robinhood-readonly-export",
                ],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(import_transactions.returncode, 0)
            self.assertIn("No broker credentials were stored.", import_transactions.stdout)

            transaction_manifest_path = (
                output / "data" / "transaction_import_manifest.jsonl"
            )
            self.assertTrue(transaction_manifest_path.exists())
            transaction_manifest = [
                json.loads(line)
                for line in transaction_manifest_path.read_text(
                    encoding="utf-8"
                ).splitlines()
                if line.strip()
            ]
            self.assertEqual(
                transaction_manifest[0]["source_type"], "robinhood-readonly-export"
            )
            self.assertFalse(transaction_manifest[0]["credentials_stored"])
            self.assertEqual(
                transaction_manifest[0]["mode"], "read_only_transactions"
            )

            transaction_report = subprocess.run(
                [sys.executable, "report.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            transaction_report_text = (
                output / "reports" / "daily_report.md"
            ).read_text(encoding="utf-8")
            self.assertEqual(transaction_report.returncode, 0)
            self.assertIn("MSFT", transaction_report_text)
            self.assertIn("DIVIDEND", transaction_report_text)

            import_cash = subprocess.run(
                [
                    sys.executable,
                    "import_portfolio_cash.py",
                    str(Path.cwd() / "examples" / "portfolio_cash.csv"),
                    "--source",
                    "robinhood-readonly-export",
                ],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(import_cash.returncode, 0)
            self.assertIn("No broker credentials were stored.", import_cash.stdout)

            cash_manifest_path = output / "data" / "cash_import_manifest.jsonl"
            self.assertTrue(cash_manifest_path.exists())
            cash_manifest = [
                json.loads(line)
                for line in cash_manifest_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(cash_manifest[0]["source_type"], "robinhood-readonly-export")
            self.assertFalse(cash_manifest[0]["credentials_stored"])
            self.assertEqual(cash_manifest[0]["mode"], "read_only_cash")

            cash_report = subprocess.run(
                [sys.executable, "report.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            cash_report_text = (output / "reports" / "daily_report.md").read_text(
                encoding="utf-8"
            )
            self.assertEqual(cash_report.returncode, 0)
            self.assertIn("retirement: USD 1,250.00", cash_report_text)
            self.assertIn("Cash value: $2,000.00", cash_report_text)

            import_watchlist = subprocess.run(
                [
                    sys.executable,
                    "import_portfolio_watchlist.py",
                    str(Path.cwd() / "examples" / "portfolio_watchlist.csv"),
                    "--source",
                    "conversation-draft",
                ],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(import_watchlist.returncode, 0)
            self.assertIn("No broker credentials were stored.", import_watchlist.stdout)

            watchlist_manifest_path = output / "data" / "watchlist_import_manifest.jsonl"
            self.assertTrue(watchlist_manifest_path.exists())
            watchlist_manifest = [
                json.loads(line)
                for line in watchlist_manifest_path.read_text(
                    encoding="utf-8"
                ).splitlines()
                if line.strip()
            ]
            self.assertEqual(watchlist_manifest[0]["source_type"], "conversation-draft")
            self.assertFalse(watchlist_manifest[0]["credentials_stored"])
            self.assertEqual(watchlist_manifest[0]["mode"], "read_only_watchlist")

            watchlist_report = subprocess.run(
                [sys.executable, "report.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            watchlist_report_text = (
                output / "reports" / "daily_report.md"
            ).read_text(encoding="utf-8")
            self.assertEqual(watchlist_report.returncode, 0)
            self.assertIn("NVDA", watchlist_report_text)
            self.assertIn("Dividend quality candidate", watchlist_report_text)

            import_market_data = subprocess.run(
                [
                    sys.executable,
                    "import_portfolio_market_data.py",
                    str(Path.cwd() / "examples" / "portfolio_market_data.csv"),
                    "--source",
                    "openbb-export",
                ],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(import_market_data.returncode, 0)
            self.assertIn("No broker credentials were stored.", import_market_data.stdout)

            market_manifest_path = output / "data" / "market_data_import_manifest.jsonl"
            self.assertTrue(market_manifest_path.exists())
            market_manifest = [
                json.loads(line)
                for line in market_manifest_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(market_manifest[0]["source_type"], "openbb-export")
            self.assertFalse(market_manifest[0]["credentials_stored"])
            self.assertEqual(market_manifest[0]["mode"], "read_only_market_snapshot")

            market_report = subprocess.run(
                [sys.executable, "report.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            market_report_text = (output / "reports" / "daily_report.md").read_text(
                encoding="utf-8"
            )
            self.assertEqual(market_report.returncode, 0)
            self.assertIn("Cloud growth watch", market_report_text)
            self.assertIn("market snapshot price $210.00", market_report_text)
            self.assertIn("Unrealized gain/loss: $550.00", market_report_text)
            self.assertIn("unrealized $200.00", market_report_text)

            import_result = subprocess.run(
                [
                    sys.executable,
                    "import_conversation.py",
                    str(Path.cwd() / "examples" / "portfolio_update.md"),
                ],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(import_result.returncode, 0)
            self.assertIn("Imported raw conversation", import_result.stdout)

            manifest_path = output / "memory" / "raw" / "import_manifest.jsonl"
            self.assertTrue(manifest_path.exists())
            manifest = [
                json.loads(line)
                for line in manifest_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(manifest[0]["memory_layer"], "raw")
            self.assertEqual(manifest[0]["status"], "stored_raw_only")
            self.assertTrue((output / manifest[0]["stored_path"]).exists())

            extract_result = subprocess.run(
                [sys.executable, "extract_memory.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(extract_result.returncode, 0)
            self.assertIn("structured memory draft", extract_result.stdout)

            drafts_path = output / "memory" / "structured" / "extraction_drafts.jsonl"
            self.assertTrue(drafts_path.exists())
            drafts = [
                json.loads(line)
                for line in drafts_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(drafts[0]["memory_layer"], "structured")
            self.assertEqual(drafts[0]["status"], "draft_requires_review")
            self.assertIn("concentration", " ".join(drafts[0]["risk_rules"]).lower())
            self.assertIn("review", drafts[0]["next_step"].lower())

            memory_report_result = subprocess.run(
                [sys.executable, "memory_update_report.py", "--all"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(memory_report_result.returncode, 0)
            self.assertIn("review-only memory update report", memory_report_result.stdout)
            self.assertIn("No policy", memory_report_result.stdout)

            memory_report_path = (
                output / "memory" / "structured" / "memory_update_report.md"
            )
            self.assertTrue(memory_report_path.exists())
            memory_report = memory_report_path.read_text(encoding="utf-8")
            self.assertIn("# Memory Update Report", memory_report)
            self.assertIn("## Pipeline Observability", memory_report)
            self.assertIn("## Proposed Memory Updates", memory_report)
            self.assertIn("### Risk Rules", memory_report)
            self.assertIn("### Watchlist Changes", memory_report)
            self.assertIn("evidence: S1:L", memory_report)
            self.assertIn("sha256:", memory_report)
            self.assertIn("Policy mutations: 0", memory_report)
            self.assertIn("Strategy mutations: 0", memory_report)
            self.assertIn("Review these proposed memory updates", memory_report)

            functional_report_result = subprocess.run(
                [sys.executable, "functional_evolution_report.py", "--all"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(functional_report_result.returncode, 0)
            self.assertIn("functional evolution report", functional_report_result.stdout)
            self.assertIn("No extractor", functional_report_result.stdout)

            functional_report_path = output / "evolution" / "functional_evolution_report.md"
            self.assertTrue(functional_report_path.exists())
            functional_report = functional_report_path.read_text(encoding="utf-8")
            self.assertIn("# Functional Evolution Report", functional_report)
            self.assertIn("## Pipeline Observability", functional_report)
            self.assertIn("## Proposed Functional Upgrades", functional_report)
            self.assertIn("Add Intent-State Classifier", functional_report)
            self.assertIn("Require Evidence Anchors For Durable Memory", functional_report)
            self.assertIn("proposed_requires_approval", functional_report)
            self.assertIn("activation: not_active", functional_report)
            self.assertIn("rollback path", functional_report)
            self.assertIn("evidence:", functional_report)
            self.assertIn("sha256:", functional_report)
            self.assertIn("must not directly rewrite", functional_report)

            observability_result = subprocess.run(
                [sys.executable, "extraction_observability.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(observability_result.returncode, 0)
            self.assertIn("extraction observability report", observability_result.stdout)
            self.assertIn("No memory", observability_result.stdout)

            observability_path = (
                output / "memory" / "structured" / "extraction_observability.md"
            )
            self.assertTrue(observability_path.exists())
            observability = observability_path.read_text(encoding="utf-8")
            self.assertIn("# Extraction Observability Report", observability)
            self.assertIn("## Processing Summary", observability)
            self.assertIn("Raw imports processed: 1", observability)
            self.assertIn("Rejected or noisy lines:", observability)
            self.assertIn("Low-confidence drafts:", observability)
            self.assertIn("Conflict-signal lines:", observability)
            self.assertIn("Evidence anchors found:", observability)
            self.assertIn("## Source Checksums", observability)
            self.assertIn("sha256", observability)
            self.assertIn("## Evidence Locations", observability)
            self.assertIn("S1:L", observability)

            versioning_result = subprocess.run(
                [sys.executable, "extractor_versioning.py", "snapshot"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(versioning_result.returncode, 0)
            self.assertIn("extractor version snapshot", versioning_result.stdout)
            self.assertIn("extractor rollback plan", versioning_result.stdout)
            self.assertIn("No extractor", versioning_result.stdout)

            version_log_path = output / "evolution" / "extractor_versions.jsonl"
            rollback_plan_path = output / "evolution" / "extractor_rollback_plan.md"
            self.assertTrue(version_log_path.exists())
            self.assertTrue(rollback_plan_path.exists())
            version_log = [
                json.loads(line)
                for line in version_log_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(version_log[0]["event"], "extractor_version_snapshot")
            self.assertEqual(version_log[0]["activation"], "not_active")
            self.assertIn("extract_memory.py", {item["path"] for item in version_log[0]["files"]})
            rollback_plan = rollback_plan_path.read_text(encoding="utf-8")
            self.assertIn("# Extractor Rollback Plan", rollback_plan)
            self.assertIn("No extractor change is active", rollback_plan)

            weekly_result = subprocess.run(
                [sys.executable, "weekly_review.py", "--skip-report"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(weekly_result.returncode, 0)
            self.assertIn("weekly review log", weekly_result.stdout)
            weekly_log_path = output / ".setup_os" / "weekly_review.jsonl"
            self.assertTrue(weekly_log_path.exists())
            weekly_events = [
                json.loads(line)
                for line in weekly_log_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(weekly_events[-1]["event"], "weekly_review")
            self.assertEqual(weekly_events[-1]["status"], "success")
            self.assertFalse(weekly_events[-1]["mutated_policy_or_strategy"])

            packet_path = output / "evolution" / "review_packet.md"
            self.assertTrue(packet_path.exists())
            packet = packet_path.read_text(encoding="utf-8")
            self.assertIn("# Portfolio Evolution Review Packet", packet)
            self.assertIn("Memory Update Report", packet)
            self.assertIn("Functional Evolution Report", packet)
            self.assertIn("Extractor Rollback Plan", packet)
            self.assertIn("Weekly Review Log", packet)

            verify = subprocess.run(
                [sys.executable, "verify.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(verify.returncode, 0)
            self.assertIn("Verification passed.", verify.stdout)

            health = subprocess.run(
                [sys.executable, "health.py"],
                cwd=output,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(health.returncode, 0)
            self.assertIn("Runtime health check passed.", health.stdout)


if __name__ == "__main__":
    unittest.main()

