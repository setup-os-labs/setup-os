from __future__ import annotations

import subprocess
import sys
import unittest


class CliTests(unittest.TestCase):
    def test_help_runs(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "setup_os.cli", "--help"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("usage: setup-os", result.stdout)
        self.assertIn("create", result.stdout)
        self.assertIn("evolve", result.stdout)


if __name__ == "__main__":
    unittest.main()
