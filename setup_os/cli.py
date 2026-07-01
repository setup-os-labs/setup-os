"""Command-line interface for Setup OS."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
import json
from pathlib import Path

from setup_os import __version__
from setup_os.architecture import write_architecture_proposal
from setup_os.audit import append_audit_event
from setup_os.blueprints import generate_portfolio_blueprint
from setup_os.completeness import missing_decisions
from setup_os.conversation import parse_conversation_file
from setup_os.evolution import create_evolution_proposal
from setup_os.spec import extract_agent_spec


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="setup-os",
        description="Turn finalized AI planning conversations into local systems.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"setup-os {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="command")

    create = subparsers.add_parser(
        "create",
        help="Create a local system from a planning conversation.",
    )
    create.add_argument(
        "conversation",
        help="Path to a Markdown, TXT, or JSON planning conversation.",
    )
    create.add_argument(
        "-o",
        "--output",
        default="generated/setup-os-agent",
        help="Directory for generated Setup OS files.",
    )
    create.set_defaults(handler=_create)

    evolve = subparsers.add_parser(
        "evolve",
        help="Create an evolution proposal from an update conversation.",
    )
    evolve.add_argument(
        "conversation",
        help="Path to a Markdown, TXT, or JSON update conversation.",
    )
    evolve.add_argument(
        "-o",
        "--output",
        default="generated/setup-os-agent",
        help="Directory where the evolution proposal should be written.",
    )
    evolve.set_defaults(handler=_evolve)

    return parser


def _create(args: argparse.Namespace) -> int:
    envelope = parse_conversation_file(args.conversation)
    spec = extract_agent_spec(envelope)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    spec_path = output_dir / "agent_spec.json"
    spec_path.write_text(
        json.dumps(spec.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    architecture_path = write_architecture_proposal(spec, output_dir)
    missing = missing_decisions(spec)
    if spec.slug == "portfolio-manager-agent":
        generate_portfolio_blueprint(spec, output_dir)
    append_audit_event(
        output_dir,
        "create",
        {
            "conversation": args.conversation,
            "spec": spec.slug,
            "artifact": str(spec_path),
            "architecture": str(architecture_path),
            "missing_decisions": [decision.key for decision in missing],
        },
    )

    print(f"Wrote {spec_path}")
    if missing:
        print("Missing decisions:")
        for decision in missing:
            print(f"- {decision.key}: {decision.prompt}")
    return 0


def _evolve(args: argparse.Namespace) -> int:
    envelope = parse_conversation_file(args.conversation)
    proposal = create_evolution_proposal(envelope)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    proposal_path = output_dir / "evolution_proposal.md"
    proposal_path.write_text(proposal.to_markdown(), encoding="utf-8")
    append_audit_event(
        output_dir,
        "evolve",
        {
            "conversation": args.conversation,
            "artifact": str(proposal_path),
            "approval_required": proposal.approval_required,
        },
    )

    print(f"Wrote {proposal_path}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "handler"):
        parser.print_help()
        return 0

    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
