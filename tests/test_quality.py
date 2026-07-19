from __future__ import annotations

import unittest

from setup_os.conversation import parse_conversation_file
from setup_os.quality import agent_dna, score_agent
from setup_os.spec import extract_agent_spec


class QualityTests(unittest.TestCase):
    def test_portfolio_agent_quality_score_and_dna(self) -> None:
        envelope = parse_conversation_file("examples/portfolio_conversation.md")
        spec = extract_agent_spec(envelope)
        score = score_agent(spec)
        dna = agent_dna(spec)

        self.assertGreaterEqual(score.overall, 90)
        self.assertEqual(dna["maturity_level"], "Level 2: Alerts")
        self.assertIn("optimize for deletion", dna["principles"])
        self.assertEqual(dna["quality_score"]["privacy"], 100)


if __name__ == "__main__":
    unittest.main()
