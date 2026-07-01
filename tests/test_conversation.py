from __future__ import annotations

import unittest
from pathlib import Path

from setup_os.conversation import parse_conversation_file, parse_markdown_or_text


class ConversationImportTests(unittest.TestCase):
    def test_parse_markdown_headings(self) -> None:
        messages = parse_markdown_or_text(
            """# Planning

## User
Build a local portfolio agent.

## Assistant
Start with CSV imports and reports.
"""
        )

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].role, "user")
        self.assertEqual(messages[0].content, "Build a local portfolio agent.")
        self.assertEqual(messages[1].role, "assistant")

    def test_parse_inline_role_prefixes(self) -> None:
        messages = parse_markdown_or_text(
            """User: Keep trades disabled.
Assistant: Require approval for external actions.
"""
        )

        self.assertEqual([message.role for message in messages], ["user", "assistant"])
        self.assertEqual(messages[0].content, "Keep trades disabled.")

    def test_parse_portfolio_example_into_envelope(self) -> None:
        envelope = parse_conversation_file(Path("examples/portfolio_conversation.md"))

        self.assertEqual(envelope.source["name"], "portfolio_conversation.md")
        self.assertEqual(envelope.provenance["message_count"], 4)
        self.assertEqual(envelope.messages[0].role, "user")
        self.assertIn("Portfolio Manager Agent", envelope.messages[0].content)


if __name__ == "__main__":
    unittest.main()
