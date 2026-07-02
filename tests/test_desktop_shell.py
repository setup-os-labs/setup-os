from __future__ import annotations

import json
import struct
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESKTOP = ROOT / "apps" / "desktop"


class DesktopShellTests(unittest.TestCase):
    def test_desktop_project_files_exist(self) -> None:
        expected = [
            "package.json",
            "index.html",
            "src/App.tsx",
            "src/lib/setupOs.ts",
            "src-tauri/Cargo.toml",
            "src-tauri/icons/icon.png",
            "src-tauri/icons/icon.ico",
            "src-tauri/sidecar/README.md",
            "src-tauri/tauri.conf.json",
            "src-tauri/src/lib.rs",
        ]

        for relative_path in expected:
            self.assertTrue((DESKTOP / relative_path).exists(), relative_path)

    def test_tauri_config_is_valid_json(self) -> None:
        config = json.loads((DESKTOP / "src-tauri" / "tauri.conf.json").read_text(encoding="utf-8"))

        self.assertEqual(config["productName"], "Setup OS")
        self.assertEqual(config["app"]["windows"][0]["title"], "Setup OS")
        self.assertEqual(
            config["bundle"]["icon"],
            ["icons/icon.png", "icons/icon.ico"],
        )

    def test_ico_directory_matches_embedded_png_dimensions(self) -> None:
        icon = (DESKTOP / "src-tauri" / "icons" / "icon.ico").read_bytes()

        self.assertEqual(icon[:6], b"\x00\x00\x01\x00\x01\x00")
        directory_width = 256 if icon[6] == 0 else icon[6]
        directory_height = 256 if icon[7] == 0 else icon[7]
        image_size = struct.unpack("<I", icon[14:18])[0]
        image_offset = struct.unpack("<I", icon[18:22])[0]
        png = icon[image_offset : image_offset + image_size]
        png_width, png_height = struct.unpack(">II", png[16:24])

        self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual((directory_width, directory_height), (png_width, png_height))

    def test_package_declares_desktop_stack(self) -> None:
        package = json.loads((DESKTOP / "package.json").read_text(encoding="utf-8"))

        self.assertEqual(package["name"], "@setup-os/desktop")
        self.assertIn("@tauri-apps/api", package["dependencies"])
        self.assertIn("react", package["dependencies"])
        self.assertIn("lucide-react", package["dependencies"])
        self.assertIn("@tauri-apps/cli", package["devDependencies"])
        self.assertIn("@vitejs/plugin-react-swc", package["devDependencies"])

    def test_desktop_invokes_setup_os_help_contract(self) -> None:
        lib_rs = (DESKTOP / "src-tauri" / "src" / "lib.rs").read_text(encoding="utf-8")

        self.assertIn("setup_os_help", lib_rs)
        self.assertIn("setup_os_python_runtime_status", lib_rs)
        self.assertIn("setup_os_desktop_release_readiness", lib_rs)
        self.assertIn("setup_os_check_desktop_readiness", lib_rs)
        self.assertIn("setup_os_create_portfolio_example", lib_rs)
        self.assertIn("setup_os_reset_portfolio_workspace", lib_rs)
        self.assertIn("setup_os_run_portfolio_report", lib_rs)
        self.assertIn("setup_os_review_portfolio_report_sections", lib_rs)
        self.assertIn("setup_os_review_portfolio_insights", lib_rs)
        self.assertIn("setup_os_check_portfolio_health", lib_rs)
        self.assertIn("setup_os_import_portfolio_conversation", lib_rs)
        self.assertIn("setup_os_import_portfolio_holdings", lib_rs)
        self.assertIn("setup_os_import_portfolio_transactions", lib_rs)
        self.assertIn("setup_os_import_portfolio_cash", lib_rs)
        self.assertIn("setup_os_import_portfolio_watchlist", lib_rs)
        self.assertIn("setup_os_import_portfolio_market_data", lib_rs)
        self.assertIn("setup_os_extract_portfolio_memory", lib_rs)
        self.assertIn("setup_os_review_portfolio_memory_drafts", lib_rs)
        self.assertIn("setup_os_portfolio_status", lib_rs)
        self.assertIn("setup_os_portfolio_summary", lib_rs)
        self.assertIn("setup_os_read_portfolio_notifications", lib_rs)
        self.assertIn("setup_os_read_runtime_node_log", lib_rs)
        self.assertIn("setup_os_run_portfolio_demo_flow", lib_rs)
        self.assertIn("Archived previous workspace", lib_rs)
        self.assertIn("_archives", lib_rs)
        self.assertIn("agent_dir: String", lib_rs)
        self.assertIn("seed_conversation_path: String", lib_rs)
        self.assertIn("resolve_agent_dir", lib_rs)
        self.assertIn("resolve_user_path", lib_rs)
        self.assertIn("agent output path is required", lib_rs)
        self.assertIn("seed conversation path is required", lib_rs)
        self.assertIn("Setup OS desktop readiness", lib_rs)
        self.assertIn("Next: run Create Portfolio Management OS.", lib_rs)
        self.assertIn("setup_os_repo_dir", lib_rs)
        self.assertIn("SETUP_OS_REPO_DIR", lib_rs)
        self.assertIn("Setup OS Python runtime", lib_rs)
        self.assertIn("SETUP_OS_PYTHON", lib_rs)
        self.assertIn("resolve_python_command", lib_rs)
        self.assertIn("sidecar_python_candidates", lib_rs)
        self.assertIn("bundled sidecar", lib_rs)
        self.assertIn('"python.exe"', lib_rs)
        self.assertIn('"bin"', lib_rs)
        self.assertIn("Future release target: bundled Python sidecar", lib_rs)
        self.assertIn("Setup OS desktop release readiness", lib_rs)
        self.assertIn("Manual desktop release workflow", lib_rs)
        self.assertIn("Python sidecar placeholder", lib_rs)
        self.assertIn("Python sidecar packaging notes", lib_rs)
        self.assertIn("Signing and notarization plan", lib_rs)
        self.assertIn("Packaged app smoke tests", lib_rs)
        self.assertIn("Sidecar release workflow scaffold", lib_rs)
        self.assertIn("Release contract CI check", lib_rs)
        self.assertIn("Still required before public release", lib_rs)
        self.assertIn('"setup_os.cli"', lib_rs)
        self.assertIn('"--help"', lib_rs)
        self.assertIn('"create"', lib_rs)
        self.assertIn('"examples/portfolio_conversation.md"', lib_rs)
        self.assertIn('"report.py"', lib_rs)
        self.assertIn('"health.py"', lib_rs)
        self.assertIn('"import_conversation.py"', lib_rs)
        self.assertIn('"import_portfolio_snapshot.py"', lib_rs)
        self.assertIn('"import_portfolio_transactions.py"', lib_rs)
        self.assertIn('"import_portfolio_cash.py"', lib_rs)
        self.assertIn('"import_portfolio_watchlist.py"', lib_rs)
        self.assertIn('"import_portfolio_market_data.py"', lib_rs)
        self.assertIn('"extract_memory.py"', lib_rs)
        self.assertIn('"extraction_drafts.jsonl"', lib_rs)
        self.assertIn("Structured memory drafts", lib_rs)
        self.assertIn("format_memory_draft", lib_rs)
        self.assertIn("Strategy notes", lib_rs)
        self.assertIn("Risk rules", lib_rs)
        self.assertIn("Next: review these drafts before changing strategy", lib_rs)
        self.assertIn("conversation path is required", lib_rs)
        self.assertIn('"reports"', lib_rs)
        self.assertIn('"daily_report.md"', lib_rs)
        self.assertIn("Portfolio report sections", lib_rs)
        self.assertIn("format_markdown_sections", lib_rs)
        self.assertIn("Portfolio dashboard insights", lib_rs)
        self.assertIn("format_portfolio_insights", lib_rs)
        self.assertIn('"Recent Transactions"', lib_rs)
        self.assertIn('"Market Snapshot"', lib_rs)
        self.assertIn('"notifications.jsonl"', lib_rs)
        self.assertIn("Portfolio notification inbox", lib_rs)
        self.assertIn('"runtime_node.jsonl"', lib_rs)
        self.assertIn("Runtime node log", lib_rs)
        self.assertIn("Recent cycles", lib_rs)
        self.assertIn("Portfolio Management OS summary", lib_rs)
        self.assertIn("Latest report preview", lib_rs)
        self.assertIn("Portfolio Management OS status", lib_rs)
        self.assertIn("Create Portfolio Management OS", lib_rs)
        self.assertIn("Run daily report", lib_rs)

    def test_desktop_ui_accepts_portfolio_output_path(self) -> None:
        app = (DESKTOP / "src" / "App.tsx").read_text(encoding="utf-8")
        setup_os = (DESKTOP / "src" / "lib" / "setupOs.ts").read_text(encoding="utf-8")

        self.assertIn("portfolioOutputPath", app)
        self.assertIn("requirePath", app)
        self.assertIn("is required before running this action.", app)
        self.assertIn("Seed conversation path", app)
        self.assertIn("Conversation path", app)
        self.assertIn("window.localStorage", app)
        self.assertIn("setup-os:portfolio-output-path", app)
        self.assertIn("setup-os:portfolio-seed-conversation-path", app)
        self.assertIn("setup-os:portfolio-conversation-path", app)
        self.assertIn("setup-os:portfolio-data-import-paths", app)
        self.assertIn("getPythonRuntimeStatus", app)
        self.assertIn("Runtime details", app)
        self.assertIn("getDesktopReleaseReadiness", app)
        self.assertIn("Release readiness", app)
        self.assertIn("Portfolio dashboard", app)
        self.assertIn("parsePortfolioDashboard", app)
        self.assertIn("DashboardCard", app)
        self.assertIn("Update dashboard", app)
        self.assertIn("Memory drafts", app)
        self.assertIn('aria-label="Portfolio output path"', app)
        self.assertIn('aria-label="Seed conversation path"', app)
        self.assertIn('"generated/desktop-portfolio-os"', app)
        self.assertIn('"examples/portfolio_conversation.md"', app)
        self.assertIn('"examples/portfolio_update.md"', app)
        self.assertIn('"examples/portfolio_snapshot.csv"', app)
        self.assertIn("createPortfolioExample(portfolioOutputPath, seedConversationPath)", app)
        self.assertIn("resetPortfolioWorkspace(portfolioOutputPath, seedConversationPath)", app)
        self.assertIn("Reset workspace", app)
        self.assertIn("window.confirm", app)
        self.assertIn("runPortfolioDemoFlow(portfolioOutputPath)", app)
        self.assertIn("reviewPortfolioReportSections(portfolioOutputPath)", app)
        self.assertIn("Review report", app)
        self.assertIn("reviewPortfolioInsights(portfolioOutputPath)", app)
        self.assertIn("Review insights", app)
        self.assertIn("readPortfolioNotifications(portfolioOutputPath)", app)
        self.assertIn("Read inbox", app)
        self.assertIn("readRuntimeNodeLog(portfolioOutputPath)", app)
        self.assertIn("Read runtime log", app)
        self.assertIn("checkDesktopReadiness(portfolioOutputPath, seedConversationPath)", app)
        self.assertIn("Check readiness", app)
        self.assertIn("reviewPortfolioMemoryDrafts(portfolioOutputPath)", app)
        self.assertIn("Review drafts", app)
        self.assertIn("getPortfolioSummary(portfolioOutputPath)", app)
        self.assertIn("Load summary", app)
        self.assertIn("agentDir: string", setup_os)
        self.assertIn("seedConversationPath: string", setup_os)
        self.assertIn("getPythonRuntimeStatus", setup_os)
        self.assertIn('"setup_os_python_runtime_status"', setup_os)
        self.assertIn("getDesktopReleaseReadiness", setup_os)
        self.assertIn('"setup_os_desktop_release_readiness"', setup_os)
        self.assertIn("checkDesktopReadiness", setup_os)
        self.assertIn("resetPortfolioWorkspace", setup_os)
        self.assertIn("reviewPortfolioReportSections", setup_os)
        self.assertIn("reviewPortfolioInsights", setup_os)
        self.assertIn("reviewPortfolioMemoryDrafts", setup_os)
        self.assertIn("getPortfolioSummary", setup_os)
        self.assertIn('"setup_os_create_portfolio_example", { agentDir, seedConversationPath }', setup_os)
        self.assertIn('"setup_os_reset_portfolio_workspace", { agentDir, seedConversationPath }', setup_os)
        self.assertIn('"setup_os_review_portfolio_insights", { agentDir }', setup_os)
        self.assertIn('"setup_os_read_portfolio_notifications", { agentDir }', setup_os)
        self.assertIn('"setup_os_read_runtime_node_log", { agentDir }', setup_os)

        styles = (DESKTOP / "src" / "styles.css").read_text(encoding="utf-8")
        self.assertIn(".dashboard-grid", styles)
        self.assertIn(".dashboard-card", styles)

        sidecar_notes = (ROOT / "docs" / "python-sidecar-packaging.md").read_text(encoding="utf-8")
        self.assertIn("Resolver Order", sidecar_notes)
        self.assertIn("SETUP_OS_PYTHON", sidecar_notes)
        self.assertIn("Bundled sidecar Python", sidecar_notes)

        signing_notes = (ROOT / "docs" / "desktop-signing-notarization.md").read_text(encoding="utf-8")
        self.assertIn("Windows Release Requirements", signing_notes)
        self.assertIn("macOS Release Requirements", signing_notes)
        self.assertIn("Do not add real secrets to the repo", signing_notes)

        smoke_tests = (ROOT / "docs" / "packaged-app-smoke-tests.md").read_text(encoding="utf-8")
        self.assertIn("Windows", smoke_tests)
        self.assertIn("macOS", smoke_tests)
        self.assertIn("Run **Release readiness**", smoke_tests)

        release_contract = (ROOT / "scripts" / "check_desktop_release_contract.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("Desktop release contract OK", release_contract)

        result = subprocess.run(
            [sys.executable, "-m", "setup_os.cli", "--help"],
            check=False,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Turn finalized AI planning conversations into local systems.", result.stdout)


if __name__ == "__main__":
    unittest.main()
