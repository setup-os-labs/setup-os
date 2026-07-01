use std::fs;
use std::path::PathBuf;
use std::process::Command;

#[tauri::command]
fn setup_os_help() -> Result<String, String> {
    run_setup_os(["-m", "setup_os.cli", "--help"])
}

#[tauri::command]
fn setup_os_check_desktop_readiness(
    agent_dir: String,
    seed_conversation_path: String,
) -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let agent_dir = resolve_agent_dir(&agent_dir)?;
    let seed_path = resolve_user_path(&repo_dir, &seed_conversation_path)?;
    let python = std::env::var("SETUP_OS_PYTHON").unwrap_or_else(|_| "python".to_string());
    let python_check = Command::new(&python)
        .args(["-m", "setup_os.cli", "--help"])
        .current_dir(&repo_dir)
        .output();

    let mut lines = vec!["Setup OS desktop readiness".to_string()];
    lines.push(format!(
        "- {}: repo root ({})",
        marker(repo_dir.join("setup_os").join("cli.py").exists()),
        repo_dir.display()
    ));
    lines.push(format!(
        "- {}: Python engine ({})",
        marker(python_check.as_ref().map_or(false, |output| output.status.success())),
        python
    ));
    if let Ok(output) = &python_check {
        if !output.status.success() {
            let stderr = String::from_utf8_lossy(&output.stderr);
            lines.push(format!("  Next: fix Python engine startup. {stderr}"));
        }
    } else if let Err(error) = &python_check {
        lines.push(format!("  Next: set SETUP_OS_PYTHON or install Python. {error}"));
    }
    lines.push(format!(
        "- {}: seed conversation ({})",
        marker(seed_path.exists()),
        seed_path.display()
    ));
    if !seed_path.exists() {
        lines.push("  Next: choose an existing Markdown/TXT planning conversation before creating.".to_string());
    }
    lines.push(format!(
        "- {}: selected Portfolio workspace ({})",
        marker(agent_dir.exists()),
        agent_dir.display()
    ));
    if !agent_dir.exists() {
        lines.push("  Next: run Create Portfolio Management OS.".to_string());
    } else {
        for file_name in ["report.py", "health.py", "import_conversation.py"] {
            lines.push(format!(
                "- {}: generated {file_name}",
                marker(agent_dir.join(file_name).exists())
            ));
        }
    }

    Ok(lines.join("\n"))
}

#[tauri::command]
fn setup_os_create_portfolio_example(
    agent_dir: String,
    seed_conversation_path: String,
) -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let output_dir = normalize_required_path(&agent_dir, "agent output path is required")?;
    let seed_path = normalize_required_path(
        &resolve_user_path(&repo_dir, &seed_conversation_path)?.display().to_string(),
        "seed conversation path is required",
    )?;
    run_setup_os([
        "-m",
        "setup_os.cli",
        "create",
        seed_path.as_str(),
        "--output",
        output_dir.as_str(),
    ])
}

#[tauri::command]
fn setup_os_run_portfolio_report(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
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
fn setup_os_check_portfolio_health(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
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
fn setup_os_import_portfolio_conversation(
    agent_dir: String,
    conversation_path: String,
) -> Result<String, String> {
    run_generated_portfolio_script(
        &agent_dir,
        "import_conversation.py",
        &[conversation_path.as_str()],
        "conversation path is required",
        "failed to import Portfolio conversation",
        "Portfolio conversation import",
    )
}

#[tauri::command]
fn setup_os_import_portfolio_holdings(agent_dir: String, holdings_path: String) -> Result<String, String> {
    run_generated_portfolio_script(
        &agent_dir,
        "import_portfolio_snapshot.py",
        &[holdings_path.as_str(), "--source", "desktop-local-file"],
        "holdings path is required",
        "failed to import Portfolio holdings",
        "Portfolio holdings import",
    )
}

#[tauri::command]
fn setup_os_import_portfolio_transactions(
    agent_dir: String,
    transactions_path: String,
) -> Result<String, String> {
    run_generated_portfolio_script(
        &agent_dir,
        "import_portfolio_transactions.py",
        &[transactions_path.as_str(), "--source", "desktop-local-file"],
        "transactions path is required",
        "failed to import Portfolio transactions",
        "Portfolio transactions import",
    )
}

#[tauri::command]
fn setup_os_import_portfolio_cash(agent_dir: String, cash_path: String) -> Result<String, String> {
    run_generated_portfolio_script(
        &agent_dir,
        "import_portfolio_cash.py",
        &[cash_path.as_str(), "--source", "desktop-local-file"],
        "cash path is required",
        "failed to import Portfolio cash",
        "Portfolio cash import",
    )
}

#[tauri::command]
fn setup_os_import_portfolio_watchlist(agent_dir: String, watchlist_path: String) -> Result<String, String> {
    run_generated_portfolio_script(
        &agent_dir,
        "import_portfolio_watchlist.py",
        &[watchlist_path.as_str(), "--source", "desktop-local-file"],
        "watchlist path is required",
        "failed to import Portfolio watchlist",
        "Portfolio watchlist import",
    )
}

#[tauri::command]
fn setup_os_import_portfolio_market_data(
    agent_dir: String,
    market_data_path: String,
) -> Result<String, String> {
    run_generated_portfolio_script(
        &agent_dir,
        "import_portfolio_market_data.py",
        &[market_data_path.as_str(), "--source", "desktop-local-file"],
        "market data path is required",
        "failed to import Portfolio market data",
        "Portfolio market data import",
    )
}

#[tauri::command]
fn setup_os_extract_portfolio_memory(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
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
fn setup_os_review_portfolio_memory_drafts(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
    let drafts_path = agent_dir
        .join("memory")
        .join("structured")
        .join("extraction_drafts.jsonl");
    if !drafts_path.exists() {
        return Ok(format!(
            "No structured memory drafts yet.\nExpected drafts: {}\nNext: import a saved conversation, then run Extract drafts.",
            drafts_path.display()
        ));
    }

    let drafts = fs::read_to_string(&drafts_path)
        .map_err(|error| format!("failed to read {}: {error}", drafts_path.display()))?;
    if drafts.trim().is_empty() {
        return Ok(format!(
            "Structured memory draft file is empty.\nDrafts: {}\nNext: run Extract drafts again after importing a conversation.",
            drafts_path.display()
        ));
    }

    Ok(format!(
        "Structured memory drafts\n{}\n\n{}",
        drafts_path.display(),
        drafts
    ))
}

#[tauri::command]
fn setup_os_portfolio_status(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
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

#[tauri::command]
fn setup_os_portfolio_summary(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
    let report_path = agent_dir.join("reports").join("daily_report.md");
    let notifications_path = agent_dir.join(".setup_os").join("notifications.jsonl");
    let drafts_path = agent_dir
        .join("memory")
        .join("structured")
        .join("extraction_drafts.jsonl");

    let mut lines = vec![
        "Portfolio Management OS summary".to_string(),
        format!("Workspace: {}", agent_dir.display()),
        format!("- {}", existence_line("Health command", agent_dir.join("health.py").exists())),
        format!("- {}", existence_line("Latest report", report_path.exists())),
        format!("- {}", count_line("Notifications", &notifications_path)?),
        format!("- {}", count_line("Structured memory drafts", &drafts_path)?),
    ];

    if report_path.exists() {
        let report = fs::read_to_string(&report_path)
            .map_err(|error| format!("failed to read {}: {error}", report_path.display()))?;
        let preview = report
            .lines()
            .filter(|line| !line.trim().is_empty())
            .take(8)
            .collect::<Vec<_>>()
            .join("\n");
        lines.push("\nLatest report preview".to_string());
        lines.push(preview);
    } else {
        lines.push("\nNext: run the daily report to populate the summary preview.".to_string());
    }

    Ok(lines.join("\n"))
}

#[tauri::command]
fn setup_os_read_portfolio_notifications(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
    let inbox_path = agent_dir.join(".setup_os").join("notifications.jsonl");
    if !inbox_path.exists() {
        return Ok(format!(
            "No Portfolio notifications yet.\nExpected inbox: {}",
            inbox_path.display()
        ));
    }

    let inbox = fs::read_to_string(&inbox_path)
        .map_err(|error| format!("failed to read {}: {error}", inbox_path.display()))?;
    if inbox.trim().is_empty() {
        return Ok(format!(
            "Portfolio notification inbox is empty.\nInbox: {}",
            inbox_path.display()
        ));
    }

    Ok(format!(
        "Portfolio notification inbox\n{}\n\n{}",
        inbox_path.display(),
        inbox
    ))
}

#[tauri::command]
fn setup_os_run_portfolio_demo_flow(agent_dir: String) -> Result<String, String> {
    let mut transcript = Vec::new();

    append_demo_step(
        &mut transcript,
        "Create Portfolio Management OS",
        setup_os_create_portfolio_example(
            agent_dir.clone(),
            "examples/portfolio_conversation.md".to_string(),
        ),
    )?;
    append_demo_step(
        &mut transcript,
        "Import holdings",
        setup_os_import_portfolio_holdings(agent_dir.clone(), "examples/portfolio_snapshot.csv".to_string()),
    )?;
    append_demo_step(
        &mut transcript,
        "Import transactions",
        setup_os_import_portfolio_transactions(
            agent_dir.clone(),
            "examples/portfolio_transactions.csv".to_string(),
        ),
    )?;
    append_demo_step(
        &mut transcript,
        "Import cash",
        setup_os_import_portfolio_cash(agent_dir.clone(), "examples/portfolio_cash.csv".to_string()),
    )?;
    append_demo_step(
        &mut transcript,
        "Import watchlist",
        setup_os_import_portfolio_watchlist(agent_dir.clone(), "examples/portfolio_watchlist.csv".to_string()),
    )?;
    append_demo_step(
        &mut transcript,
        "Import market data",
        setup_os_import_portfolio_market_data(agent_dir.clone(), "examples/portfolio_market_data.csv".to_string()),
    )?;
    append_demo_step(
        &mut transcript,
        "Import saved conversation",
        setup_os_import_portfolio_conversation(agent_dir.clone(), "examples/portfolio_update.md".to_string()),
    )?;
    append_demo_step(
        &mut transcript,
        "Extract memory drafts",
        setup_os_extract_portfolio_memory(agent_dir.clone()),
    )?;
    append_demo_step(
        &mut transcript,
        "Run health check",
        setup_os_check_portfolio_health(agent_dir.clone()),
    )?;
    append_demo_step(
        &mut transcript,
        "Run daily report",
        setup_os_run_portfolio_report(agent_dir.clone()),
    )?;
    append_demo_step(
        &mut transcript,
        "Read notification inbox",
        setup_os_read_portfolio_notifications(agent_dir.clone()),
    )?;
    append_demo_step(&mut transcript, "Refresh status", setup_os_portfolio_status(agent_dir))?;

    Ok(transcript.join("\n\n"))
}

fn append_demo_step(
    transcript: &mut Vec<String>,
    label: &str,
    result: Result<String, String>,
) -> Result<(), String> {
    transcript.push(format!("## {label}"));
    match result {
        Ok(output) => {
            transcript.push(output.trim().to_string());
            Ok(())
        }
        Err(error) => {
            transcript.push(format!("FAILED: {error}"));
            Err(transcript.join("\n\n"))
        }
    }
}

fn ensure_generated_portfolio_file(agent_dir: &PathBuf, file_name: &str) -> Result<(), String> {
    if agent_dir.join(file_name).exists() {
        return Ok(());
    }

    Err(format!(
        "{} is missing {file_name}; create the Portfolio Management OS first",
        agent_dir.display()
    ))
}

fn run_generated_portfolio_script(
    agent_dir: &str,
    script_name: &str,
    args: &[&str],
    empty_path_error: &str,
    start_error: &str,
    label: &str,
) -> Result<String, String> {
    if args.first().map_or(true, |path| path.trim().is_empty()) {
        return Err(empty_path_error.to_string());
    }

    let repo_dir = setup_os_repo_dir()?;
    let agent_dir = resolve_agent_dir(agent_dir)?;
    ensure_generated_portfolio_file(&agent_dir, script_name)?;
    let mut resolved_args = Vec::new();
    for argument in args {
        let trimmed = argument.trim();
        if trimmed.starts_with("--") {
            resolved_args.push(trimmed.to_string());
        } else if resolved_args.last().map_or(false, |last| last == "--source") {
            resolved_args.push(trimmed.to_string());
        } else {
            resolved_args.push(resolve_user_path(&repo_dir, trimmed)?.display().to_string());
        }
    }

    let python = std::env::var("SETUP_OS_PYTHON").unwrap_or_else(|_| "python".to_string());
    let output = Command::new(python)
        .arg(script_name)
        .args(resolved_args)
        .current_dir(&agent_dir)
        .output()
        .map_err(|error| format!("{start_error}: {error}"))?;

    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr).to_string();
        Err(format!("{label} exited with {}: {stderr}", output.status))
    }
}

fn normalize_required_path(path: &str, empty_error: &str) -> Result<String, String> {
    let trimmed = path.trim();
    if trimmed.is_empty() {
        return Err(empty_error.to_string());
    }
    Ok(trimmed.replace('\\', "/"))
}

fn resolve_agent_dir(agent_dir: &str) -> Result<PathBuf, String> {
    let repo_dir = setup_os_repo_dir()?;
    let normalized = normalize_required_path(agent_dir, "agent output path is required")?;
    let path = PathBuf::from(&normalized);
    if path.is_absolute() {
        Ok(path)
    } else {
        Ok(repo_dir.join(path))
    }
}

fn resolve_user_path(repo_dir: &PathBuf, path: &str) -> Result<PathBuf, String> {
    let normalized = normalize_required_path(path, "input path is required")?;
    let path = PathBuf::from(&normalized);
    if path.is_absolute() {
        Ok(path)
    } else {
        Ok(repo_dir.join(path))
    }
}

fn marker(ok: bool) -> &'static str {
    if ok {
        "OK"
    } else {
        "MISSING"
    }
}

fn existence_line(label: &str, ok: bool) -> String {
    format!("{}: {label}", marker(ok))
}

fn count_line(label: &str, path: &PathBuf) -> Result<String, String> {
    if !path.exists() {
        return Ok(format!("MISSING: {label}"));
    }
    let content =
        fs::read_to_string(path).map_err(|error| format!("failed to read {}: {error}", path.display()))?;
    let count = content.lines().filter(|line| !line.trim().is_empty()).count();
    Ok(format!("OK: {label} ({count})"))
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
            setup_os_check_desktop_readiness,
            setup_os_create_portfolio_example,
            setup_os_run_portfolio_report,
            setup_os_check_portfolio_health,
            setup_os_import_portfolio_conversation,
            setup_os_import_portfolio_holdings,
            setup_os_import_portfolio_transactions,
            setup_os_import_portfolio_cash,
            setup_os_import_portfolio_watchlist,
            setup_os_import_portfolio_market_data,
            setup_os_extract_portfolio_memory,
            setup_os_review_portfolio_memory_drafts,
            setup_os_portfolio_status,
            setup_os_portfolio_summary,
            setup_os_read_portfolio_notifications,
            setup_os_run_portfolio_demo_flow
        ])
        .run(tauri::generate_context!())
        .expect("error while running Setup OS desktop app");
}
