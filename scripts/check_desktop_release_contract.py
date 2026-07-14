from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require_file(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.exists():
        raise AssertionError(f"missing required file: {relative_path}")
    return path.read_text(encoding="utf-8")


def require_text(relative_path: str, expected: str) -> None:
    text = require_file(relative_path)
    if expected not in text:
        raise AssertionError(f"{relative_path} does not include expected text: {expected}")


def main() -> int:
    require_file("apps/desktop/src-tauri/sidecar/README.md")
    require_file("docs/python-sidecar-packaging.md")
    require_file("docs/desktop-signing-notarization.md")
    require_file("docs/desktop-release-testing.md")
    require_file("docs/packaged-app-smoke-tests.md")
    require_file("docs/installed-app-smoke-evidence-template.md")
    require_file("docs/personal-local-setup.md")
    require_file("docs/sidecar-release-workflow-scaffold.md")
    require_file("scripts/smoke_packaged_artifact.py")
    require_file("scripts/prepare_installed_app_smoke_evidence.py")
    require_file(".github/workflows/desktop-release.yml")

    require_text(
        "apps/desktop/src-tauri/src/lib.rs",
        "SETUP_OS_PYTHON -> bundled sidecar -> system python",
    )
    require_text("apps/desktop/src-tauri/src/lib.rs", "sidecar_python_candidates")
    require_text("docs/python-sidecar-packaging.md", "Release Gate")
    require_text("docs/desktop-signing-notarization.md", "Do not add real secrets to the repo")
    require_text("docs/packaged-app-smoke-tests.md", "Run **Release readiness**")
    require_text("docs/packaged-app-smoke-tests.md", "packaged-smoke-manifest.json")
    require_text("docs/packaged-app-smoke-tests.md", "prepare_installed_app_smoke_evidence.py")
    require_text("docs/installed-app-smoke-evidence-template.md", "Review Evolution Review Packet")
    require_text("docs/installed-app-smoke-evidence-template.md", "No broker credentials requested")
    require_text("docs/personal-local-setup.md", "Local smoke test")
    require_text("docs/personal-local-setup.md", "Preview conversation")
    require_text("docs/personal-local-setup.md", "Always-On Runtime Node")
    require_text("docs/sidecar-release-workflow-scaffold.md", "Do not commit large Python runtime binaries")
    require_text(".github/workflows/desktop-release.yml", "Build unsigned desktop bundle")
    require_text(".github/workflows/desktop-release.yml", "Smoke-check packaged artifacts")
    require_text(".github/workflows/desktop-release.yml", "packaged-smoke-manifest.json")

    print("Desktop release contract OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
