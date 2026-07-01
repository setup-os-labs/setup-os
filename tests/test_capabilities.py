from __future__ import annotations

import unittest

from setup_os.capabilities import capabilities_for_slug


class CapabilityTests(unittest.TestCase):
    def test_portfolio_capabilities_include_dependencies_and_surfaces(self) -> None:
        capabilities = capabilities_for_slug("portfolio-manager-agent")

        names = [capability.name for capability in capabilities]
        self.assertIn("Daily portfolio report", names)
        self.assertIn("Evolution proposal", names)
        self.assertIn(".setup_os/timeline.jsonl", capabilities[2].surfaces)


if __name__ == "__main__":
    unittest.main()
