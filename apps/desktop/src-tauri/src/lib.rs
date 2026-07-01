use std::path::PathBuf;
use std::process::Command;

#[tauri::command]
fn setup_os_help() -> Result<String, String> {
    run_setup_os(["-m", "setup_os.cli", "--help"])
}

#[tauri::command]
fn setup_os_create_portfolio_example() -> Result<String, String> {
    run_setup_os([
        "-m",
        "setup_os.cli",
        "create",
        "examples/portfolio_conversation.md",
        "--output",
        "generated/desktop-portfolio-os",
    ])
}

fn run_setup_os<const N: usize>(args: [&str; N]) -> Result<String, String> {
    let python = std::env::var("SETUP_OS_PYTHON").unwrap_or_else(|_| "python".to_string());
    let repo_dir = setup_os_repo_dir()?;
    let output = Command::new(python)
        .args(args)
        .current_dir(repo_dir)
        .output()
        .map_err(|error| format!("failed to start Setup OS Python engine: {error}"))?;

    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr).to_string();
        Err(format!("Setup OS Python engine exited with {}: {stderr}", output.status))
    }
}

fn setup_os_repo_dir() -> Result<PathBuf, String> {
    if let Ok(path) = std::env::var("SETUP_OS_REPO_DIR") {
        return Ok(PathBuf::from(path));
    }

    let current_dir =
        std::env::current_dir().map_err(|error| format!("failed to read current dir: {error}"))?;
    for candidate in [
        current_dir.clone(),
        current_dir.join(".."),
        current_dir.join("../.."),
        current_dir.join("../../.."),
    ] {
        if candidate.join("setup_os").join("cli.py").exists() {
            return Ok(candidate);
        }
    }

    Err("could not locate Setup OS repo root; set SETUP_OS_REPO_DIR".to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            setup_os_help,
            setup_os_create_portfolio_example
        ])
        .run(tauri::generate_context!())
        .expect("error while running Setup OS desktop app");
}
