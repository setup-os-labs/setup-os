use std::fs;
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

#[tauri::command]
fn setup_os_run_portfolio_report() -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let agent_dir = repo_dir.join("generated").join("desktop-portfolio-os");
    ensure_generated_portfolio_file(&agent_dir, "report.py")?;

    let python = std::env::var("SETUP_OS_PYTHON").unwrap_or_else(|_| "python".to_string());
    let output = Command::new(python)
        .arg("report.py")
        .current_dir(&agent_dir)
        .output()
        .map_err(|error| format!("failed to run generated Portfolio report: {error}"))?;

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr).to_string();
        return Err(format!(
            "generated Portfolio report exited with {}: {stderr}",
            output.status
        ));
    }

    let report_path = agent_dir.join("reports").join("daily_report.md");
    let report = fs::read_to_string(&report_path)
        .map_err(|error| format!("failed to read {}: {error}", report_path.display()))?;
    Ok(report)
}

#[tauri::command]
fn setup_os_check_portfolio_health() -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let agent_dir = repo_dir.join("generated").join("desktop-portfolio-os");
    ensure_generated_portfolio_file(&agent_dir, "health.py")?;

    let python = std::env::var("SETUP_OS_PYTHON").unwrap_or_else(|_| "python".to_string());
    let output = Command::new(python)
        .arg("health.py")
        .current_dir(&agent_dir)
        .output()
        .map_err(|error| format!("failed to run generated Portfolio health check: {error}"))?;

    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr).to_string();
        Err(format!(
            "generated Portfolio health check exited with {}: {stderr}",
            output.status
        ))
    }
}

#[tauri::command]
fn setup_os_import_portfolio_conversation(conversation_path: String) -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let agent_dir = repo_dir.join("generated").join("desktop-portfolio-os");
    ensure_generated_portfolio_file(&agent_dir, "import_conversation.py")?;
    let trimmed_path = conversation_path.trim();
    if trimmed_path.is_empty() {
        return Err("conversation path is required".to_string());
    }

    let python = std::env::var("SETUP_OS_PYTHON").unwrap_or_else(|_| "python".to_string());
    let output = Command::new(python)
        .args(["import_conversation.py", trimmed_path])
        .current_dir(&agent_dir)
        .output()
        .map_err(|error| format!("failed to import Portfolio conversation: {error}"))?;

    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr).to_string();
        Err(format!(
            "Portfolio conversation import exited with {}: {stderr}",
            output.status
        ))
    }
}

#[tauri::command]
fn setup_os_extract_portfolio_memory() -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let agent_dir = repo_dir.join("generated").join("desktop-portfolio-os");
    ensure_generated_portfolio_file(&agent_dir, "extract_memory.py")?;

    let python = std::env::var("SETUP_OS_PYTHON").unwrap_or_else(|_| "python".to_string());
    let output = Command::new(python)
        .arg("extract_memory.py")
        .current_dir(&agent_dir)
        .output()
        .map_err(|error| format!("failed to extract Portfolio memory drafts: {error}"))?;

    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr).to_string();
        Err(format!(
            "Portfolio memory extraction exited with {}: {stderr}",
            output.status
        ))
    }
}

#[tauri::command]
fn setup_os_portfolio_status() -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let agent_dir = repo_dir.join("generated").join("desktop-portfolio-os");
    let checks = [
        ("Generated Portfolio OS", agent_dir.exists()),
        ("Report command", agent_dir.join("report.py").exists()),
        ("Health command", agent_dir.join("health.py").exists()),
        (
            "Raw conversation memory",
            agent_dir
                .join("memory")
                .join("raw")
                .join("import_manifest.jsonl")
                .exists(),
        ),
        (
            "Structured memory drafts",
            agent_dir
                .join("memory")
                .join("structured")
                .join("extraction_drafts.jsonl")
                .exists(),
        ),
        (
            "Latest daily report",
            agent_dir.join("reports").join("daily_report.md").exists(),
        ),
    ];

    let mut lines = vec!["Portfolio Management OS status".to_string()];
    for (label, exists) in checks {
        let marker = if exists { "OK" } else { "MISSING" };
        lines.push(format!("- {marker}: {label}"));
    }
    Ok(lines.join("\n"))
}

fn ensure_generated_portfolio_file(agent_dir: &PathBuf, file_name: &str) -> Result<(), String> {
    if agent_dir.join(file_name).exists() {
        return Ok(());
    }

    Err(format!(
        "generated/desktop-portfolio-os is missing {file_name}; create the Portfolio Management OS first"
    ))
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
            setup_os_create_portfolio_example,
            setup_os_run_portfolio_report,
            setup_os_check_portfolio_health,
            setup_os_import_portfolio_conversation,
            setup_os_extract_portfolio_memory,
            setup_os_portfolio_status
        ])
        .run(tauri::generate_context!())
        .expect("error while running Setup OS desktop app");
}
