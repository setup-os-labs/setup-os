from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "smoke_packaged_artifact.py"


class PackagedArtifactSmokeTests(unittest.TestCase):
    def run_smoke(self, bundle_dir: Path, platform_name: str) -> dict[str, object]:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(bundle_dir),
                "--platform",
                platform_name,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_accepts_windows_bundle_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = Path(tmpdir)
            artifact = bundle_dir / "msi" / "Setup OS_0.0.0_x64_en-US.msi"
            artifact.parent.mkdir()
            artifact.write_bytes(b"fake-msi")

            manifest = self.run_smoke(bundle_dir, "windows")

            self.assertEqual(manifest["status"], "pass")
            self.assertEqual(manifest["platform"], "windows")
            self.assertEqual(manifest["artifacts"][0]["kind"], "msi")

    def test_accepts_macos_bundle_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = Path(tmpdir)
            artifact = bundle_dir / "dmg" / "Setup OS_0.0.0_aarch64.dmg"
            artifact.parent.mkdir()
            artifact.write_bytes(b"fake-dmg")

            manifest = self.run_smoke(bundle_dir, "macos")

            self.assertEqual(manifest["platform"], "macos")
            self.assertEqual(manifest["artifacts"][0]["kind"], "dmg")

    def test_accepts_linux_bundle_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_dir = Path(tmpdir)
            artifact = bundle_dir / "appimage" / "setup-os_0.0.0_amd64.AppImage"
            artifact.parent.mkdir()
            artifact.write_bytes(b"fake-appimage")

            manifest = self.run_smoke(bundle_dir, "linux")

            self.assertEqual(manifest["platform"], "linux")
            self.assertEqual(manifest["artifacts"][0]["kind"], "AppImage")

    def test_fails_when_no_expected_artifact_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, str(SCRIPT), tmpdir, "--platform", "windows"],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no windows bundle artifacts found", result.stderr)


if __name__ == "__main__":
    unittest.main()
