from __future__ import annotations

import argparse
from dataclasses import asdict
from dataclasses import dataclass
import json
from pathlib import Path
import platform as platform_module


SUPPORTED_EXTENSIONS = {
    "linux": [".AppImage", ".deb", ".rpm"],
    "macos": [".dmg", ".app"],
    "windows": [".msi", ".exe"],
}


@dataclass
class Artifact:
    path: str
    size_bytes: int
    kind: str


def normalize_platform(value: str | None) -> str:
    raw = (value or platform_module.system()).strip().lower()
    if raw in {"darwin", "mac", "macos", "macos-latest"}:
        return "macos"
    if raw in {"win32", "windows", "windows-latest"}:
        return "windows"
    if raw in {"linux", "ubuntu", "ubuntu-latest"}:
        return "linux"
    raise ValueError(f"unsupported platform: {value}")


def artifact_kind(path: Path, platform_name: str) -> str | None:
    for extension in SUPPORTED_EXTENSIONS[platform_name]:
        if extension == ".app" and path.is_dir() and path.name.endswith(extension):
            return extension.removeprefix(".")
        if path.is_file() and path.name.endswith(extension):
            return extension.removeprefix(".")
    return None


def find_artifacts(bundle_dir: Path, platform_name: str) -> list[Artifact]:
    artifacts: list[Artifact] = []
    for path in bundle_dir.rglob("*"):
        kind = artifact_kind(path, platform_name)
        if kind is None:
            continue
        size = 0 if path.is_dir() else path.stat().st_size
        artifacts.append(
            Artifact(
                path=str(path.relative_to(bundle_dir)).replace("\\", "/"),
                size_bytes=size,
                kind=kind,
            )
        )
    return artifacts


def build_manifest(bundle_dir: Path, platform_name: str) -> dict[str, object]:
    if not bundle_dir.exists():
        raise FileNotFoundError(bundle_dir)
    if not bundle_dir.is_dir():
        raise NotADirectoryError(bundle_dir)

    artifacts = find_artifacts(bundle_dir, platform_name)
    if not artifacts:
        expected = ", ".join(SUPPORTED_EXTENSIONS[platform_name])
        raise AssertionError(
            f"no {platform_name} bundle artifacts found in {bundle_dir}; expected one of: {expected}"
        )

    return {
        "status": "pass",
        "platform": platform_name,
        "bundle_dir": str(bundle_dir),
        "artifacts": [asdict(artifact) for artifact in artifacts],
        "manual_next_steps": [
            "Download the artifact for your platform.",
            "Install or extract it on the target machine.",
            "Launch Setup OS without using repo dev commands.",
            "Run Check engine, Runtime details, Release readiness, Run demo flow, and Review handoff guidance.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Smoke-check unsigned Setup OS desktop bundle artifacts.",
    )
    parser.add_argument("bundle_dir", help="Path to a Tauri bundle output directory.")
    parser.add_argument(
        "--platform",
        help="Target platform: linux, macos, windows. Defaults to the current OS.",
    )
    parser.add_argument(
        "--output",
        help="Optional JSON manifest path to write.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    platform_name = normalize_platform(args.platform)
    manifest = build_manifest(Path(args.bundle_dir), platform_name)
    text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
