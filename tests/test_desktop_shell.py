from __future__ import annotations

import json
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
            "src-tauri/tauri.conf.json",
            "src-tauri/src/lib.rs",
        ]

        for relative_path in expected:
            self.assertTrue((DESKTOP / relative_path).exists(), relative_path)

    def test_tauri_config_is_valid_json(self) -> None:
        config = json.loads((DESKTOP / "src-tauri" / "tauri.conf.json").read_text(encoding="utf-8"))

        self.assertEqual(config["productName"], "Setup OS")
        self.assertEqual(config["app"]["windows"][0]["title"], "Setup OS")

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
        self.assertIn("setup_os_repo_dir", lib_rs)
        self.assertIn("SETUP_OS_REPO_DIR", lib_rs)
        self.assertIn('"setup_os.cli"', lib_rs)
        self.assertIn('"--help"', lib_rs)

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
