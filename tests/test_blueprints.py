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
            self.assertTrue((output / "import_portfolio_snapshot.py").exists())
            self.assertTrue((output / "import_portfolio_transactions.py").exists())
            self.assertTrue((output / "import_portfolio_cash.py").exists())
            self.assertTrue((output / "import_conversation.py").exists())
            self.assertTrue((output / "extract_memory.py").exists())
            self.assertTrue((output / "report.py").exists())
            self.assertTrue((output / "verify.py").exists())
            self.assertTrue((output / "health.py").exists())
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
            self.assertIn("## Allocation Drift Alerts", report_text)
            self.assertIn("vs target", report_text)
            self.assertIn("## Concentration Alerts", report_text)
            self.assertIn("VOO is", report_text)
            self.assertIn("## Cash", report_text)
            self.assertIn("Cash value:", report_text)
            self.assertTrue((output / ".setup_os" / "notifications.jsonl").exists())
            self.assertIn("NOTIFY[info]:", report.stdout)
            self.assertIn("NOTIFY[warning]:", report.stdout)
            self.assertNotIn("NTFY[sent]", report.stdout)

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
