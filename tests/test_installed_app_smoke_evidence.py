from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstalledAppSmokeEvidenceTests(unittest.TestCase):
    def test_prepare_installed_app_smoke_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir)
            manifest_path = temp_path / "packaged-smoke-manifest.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "status": "pass",
                        "platform": "windows",
                        "artifacts": [
                            {
                                "path": "msi/Setup OS_0.1.0_x64_en-US.msi",
                                "kind": "msi",
                                "size_bytes": 123,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            output_dir = temp_path / "evidence"

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/prepare_installed_app_smoke_evidence.py",
                    str(manifest_path),
                    "--platform",
                    "windows",
                    "--tester",
                    "Karan",
                    "--commit",
                    "abc123",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            evidence_files = list(output_dir.glob("*windows-installed-app-smoke.md"))
            self.assertEqual(len(evidence_files), 1)
            evidence = evidence_files[0].read_text(encoding="utf-8")
            self.assertIn("Tester: Karan", evidence)
            self.assertIn("Platform: windows", evidence)
            self.assertIn("Setup OS commit: abc123", evidence)
            self.assertIn("Setup OS_0.1.0_x64_en-US.msi", evidence)
            self.assertIn("Review Evolution Review Packet", evidence)


if __name__ == "__main__":
    unittest.main()
