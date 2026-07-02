# Desktop Python Sidecar

This directory reserves the desktop sidecar location for future release builds.

Development builds still use `SETUP_OS_PYTHON` or the system `python`. Release builds should eventually place a platform-specific Python runtime here and keep the Tauri command runner pointed at the same Python resolver.

Do not commit large runtime binaries directly until the release packaging workflow is ready to produce and store them as build artifacts.
