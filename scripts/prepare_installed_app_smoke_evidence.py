from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform as platform_module


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "docs" / "installed-app-smoke-evidence-template.md"
DEFAULT_OUTPUT_DIR = ROOT / "release-evidence"


def normalize_platform(value: str | None) -> str:
    raw = (value or platform_module.system()).strip().lower()
    if raw in {"darwin", "mac", "macos", "macos-latest"}:
        return "macos"
    if raw in {"win32", "windows", "windows-latest"}:
        return "windows"
    if raw in {"linux", "ubuntu", "ubuntu-latest"}:
        return "linux"
    raise ValueError(f"unsupported platform: {value}")


def load_manifest(path: Path) -> dict[str, object]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise FileNotFoundError(f"packaged smoke manifest not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"packaged smoke manifest is invalid JSON: {error}") from error


def artifact_names(manifest: dict[str, object]) -> str:
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        return "unknown"
    names = []
    for artifact in artifacts:
        if isinstance(artifact, dict):
            names.append(str(artifact.get("path", "unknown")))
    return ", ".join(names) if names else "unknown"


def build_evidence(
    manifest_path: Path,
    manifest: dict[str, object],
    platform_name: str,
    tester: str,
    commit: str,
) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    generated = datetime.now(timezone.utc).isoformat()
    artifact_name = artifact_names(manifest)
    install_mode = "unsigned downloaded artifact"
    replacements = {
        "- Tester:": f"- Tester: {tester}",
        "- Date:": f"- Date: {generated}",
        "- Platform:": f"- Platform: {platform_name}",
        "- Artifact source:": "- Artifact source: GitHub Actions desktop release artifact",
        "- Artifact name:": f"- Artifact name: {artifact_name}",
        "- Packaged smoke manifest:": f"- Packaged smoke manifest: {manifest_path}",
        "- Setup OS commit:": f"- Setup OS commit: {commit}",
        "- Install mode:": f"- Install mode: {install_mode}",
    }
    for needle, value in replacements.items():
        template = template.replace(needle, value)
    return template


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare a local installed-app smoke evidence Markdown file.",
    )
    parser.add_argument(
        "manifest",
        help="Path to packaged-smoke-manifest.json from the downloaded desktop artifact.",
    )
    parser.add_argument(
        "--platform",
        help="Target platform: windows, macos, or linux. Defaults to current OS.",
    )
    parser.add_argument("--tester", default="Karan", help="Tester name for the evidence file.")
    parser.add_argument("--commit", default="unknown", help="Setup OS commit under test.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where the local evidence file should be written.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest_path = Path(args.manifest)
    manifest = load_manifest(manifest_path)
    platform_name = normalize_platform(args.platform or str(manifest.get("platform", "")))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = output_dir / f"{timestamp}-{platform_name}-installed-app-smoke.md"
    output_path.write_text(
        build_evidence(manifest_path, manifest, platform_name, args.tester, args.commit),
        encoding="utf-8",
    )
    print(f"Wrote installed-app smoke evidence template to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
