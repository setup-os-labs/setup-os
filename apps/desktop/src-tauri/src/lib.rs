use std::fs;
use std::path::PathBuf;
use std::process::Command;
use std::time::{SystemTime, UNIX_EPOCH};

#[tauri::command]
fn setup_os_help() -> Result<String, String> {
    run_setup_os(["-m", "setup_os.cli", "--help"])
}

#[tauri::command]
fn setup_os_python_runtime_status() -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let python = resolve_python_command(&repo_dir);
    let runtime_probe = Command::new(&python)
        .args([
            "-c",
            "import sys; print(sys.executable); print(sys.version.split()[0])",
        ])
        .current_dir(&repo_dir)
        .output();
    let cli_probe = Command::new(&python)
        .args(["-m", "setup_os.cli", "--help"])
        .current_dir(&repo_dir)
        .output();

    let mut lines = vec![
        "Setup OS Python runtime".to_string(),
        format!("- Repo root: {}", repo_dir.display()),
        format!("- Python command: {python}"),
        format!(
            "- Resolver order: SETUP_OS_PYTHON -> bundled sidecar -> system python"
        ),
    ];

    match runtime_probe {
        Ok(output) if output.status.success() => {
            let stdout = String::from_utf8_lossy(&output.stdout);
            let mut details = stdout.lines();
            lines.push(format!(
                "- {}: Python executable ({})",
                marker(true),
                details.next().unwrap_or("unknown")
            ));
            lines.push(format!(
                "- {}: Python version ({})",
                marker(true),
                details.next().unwrap_or("unknown")
            ));
        }
        Ok(output) => {
            let stderr = String::from_utf8_lossy(&output.stderr);
            lines.push(format!(
                "- {}: Python runtime probe failed ({})",
                marker(false),
                output.status
            ));
            lines.push(format!("  Next: set SETUP_OS_PYTHON or install Python 3.12+. {stderr}"));
        }
        Err(error) => {
            lines.push(format!("- {}: Python executable could not start", marker(false)));
            lines.push(format!("  Next: set SETUP_OS_PYTHON or install Python 3.12+. {error}"));
        }
    }

    match cli_probe {
        Ok(output) if output.status.success() => {
            lines.push(format!("- {}: Setup OS CLI import", marker(true)));
        }
        Ok(output) => {
            let stderr = String::from_utf8_lossy(&output.stderr);
            lines.push(format!(
                "- {}: Setup OS CLI import failed ({})",
                marker(false),
                output.status
            ));
            lines.push(format!(
                "  Next: run from the Setup OS repo or set SETUP_OS_REPO_DIR. {stderr}"
            ));
        }
        Err(error) => {
            lines.push(format!("- {}: Setup OS CLI import could not start", marker(false)));
            lines.push(format!("  Next: check Python and repo configuration. {error}"));
        }
    }

    lines.push("Future release target: bundled Python sidecar so users do not install Python manually.".to_string());
    Ok(lines.join("\n"))
}

#[tauri::command]
fn setup_os_desktop_release_readiness() -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let desktop_dir = repo_dir.join("apps").join("desktop");
    let checks = [
        (
            "Desktop package manifest",
            desktop_dir.join("package.json").exists(),
        ),
        (
            "Desktop package lock",
            desktop_dir.join("package-lock.json").exists(),
        ),
        (
            "Tauri config",
            desktop_dir.join("src-tauri").join("tauri.conf.json").exists(),
        ),
        (
            "Tauri Cargo manifest",
            desktop_dir.join("src-tauri").join("Cargo.toml").exists(),
        ),
        (
            "Python sidecar placeholder",
            desktop_dir
                .join("src-tauri")
                .join("sidecar")
                .join("README.md")
                .exists(),
        ),
        (
            "Python sidecar packaging notes",
            repo_dir.join("docs").join("python-sidecar-packaging.md").exists(),
        ),
        (
            "Desktop icon PNG",
            desktop_dir
                .join("src-tauri")
                .join("icons")
                .join("icon.png")
                .exists(),
        ),
        (
            "Desktop icon ICO",
            desktop_dir
                .join("src-tauri")
                .join("icons")
                .join("icon.ico")
                .exists(),
        ),
        (
            "CI workflow",
            repo_dir.join(".github").join("workflows").join("ci.yml").exists(),
        ),
        (
            "Manual desktop release workflow",
            repo_dir
                .join(".github")
                .join("workflows")
                .join("desktop-release.yml")
                .exists(),
        ),
        (
            "Python CLI entrypoint",
            repo_dir.join("setup_os").join("cli.py").exists(),
        ),
        (
            "Release testing notes",
            repo_dir.join("docs").join("desktop-release-testing.md").exists(),
        ),
        (
            "Signing and notarization plan",
            repo_dir
                .join("docs")
                .join("desktop-signing-notarization.md")
                .exists(),
        ),
        (
            "Packaged app smoke tests",
            repo_dir.join("docs").join("packaged-app-smoke-tests.md").exists(),
        ),
        (
            "Sidecar release workflow scaffold",
            repo_dir
                .join("docs")
                .join("sidecar-release-workflow-scaffold.md")
                .exists(),
        ),
        (
            "Release contract CI check",
            repo_dir
                .join("scripts")
                .join("check_desktop_release_contract.py")
                .exists(),
        ),
    ];

    let ready_count = checks.iter().filter(|(_, exists)| *exists).count();
    let mut lines = vec![
        "Setup OS desktop release readiness".to_string(),
        format!("Repo root: {}", repo_dir.display()),
        format!("Ready checks: {ready_count}/{}", checks.len()),
    ];
    for (label, exists) in checks {
        lines.push(format!("- {}", existence_line(label, exists)));
    }
    lines.push(
        "\nStill required before public release: bundled Python sidecar, code signing, notarization, and updater policy.".to_string(),
    );
    Ok(lines.join("\n"))
}

#[tauri::command]
fn setup_os_run_local_utility_smoke_test() -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let script_path = repo_dir.join("scripts").join("smoke_local_utility.py");
    if !script_path.exists() {
        return Ok(format!(
            "Local utility smoke test is not available.\nExpected script: {}",
            script_path.display()
        ));
    }

    let python = resolve_python_command(&repo_dir);
    let output = Command::new(python)
        .arg(&script_path)
        .current_dir(&repo_dir)
        .output()
        .map_err(|error| format!("failed to start local utility smoke test: {error}"))?;

    if output.status.success() {
        Ok(format!(
            "Setup OS local utility smoke test\n{}\n\n{}",
            script_path.display(),
            String::from_utf8_lossy(&output.stdout)
        ))
    } else {
        let stdout = String::from_utf8_lossy(&output.stdout);
        let stderr = String::from_utf8_lossy(&output.stderr);
        Err(format!(
            "local utility smoke test exited with {}\nSTDOUT:\n{}\nSTDERR:\n{}",
            output.status, stdout, stderr
        ))
    }
}

#[tauri::command]
fn setup_os_check_desktop_readiness(
    agent_dir: String,
    seed_conversation_path: String,
) -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let agent_dir = resolve_agent_dir(&agent_dir)?;
    let seed_path = resolve_user_path(&repo_dir, &seed_conversation_path)?;
    let python = resolve_python_command(&repo_dir);
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
fn setup_os_reset_portfolio_workspace(
    agent_dir: String,
    seed_conversation_path: String,
) -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let agent_dir_path = resolve_agent_dir(&agent_dir)?;
    let seed_path = resolve_user_path(&repo_dir, &seed_conversation_path)?;
    if !seed_path.exists() {
        return Err(format!(
            "seed conversation does not exist: {}",
            seed_path.display()
        ));
    }

    let archive_note = if agent_dir_path.exists() {
        let parent = agent_dir_path
            .parent()
            .ok_or_else(|| format!("cannot archive {}", agent_dir_path.display()))?;
        let workspace_name = agent_dir_path
            .file_name()
            .and_then(|name| name.to_str())
            .unwrap_or("portfolio-workspace");
        let archive_dir = parent.join("_archives");
        fs::create_dir_all(&archive_dir).map_err(|error| {
            format!(
                "failed to create archive directory {}: {error}",
                archive_dir.display()
            )
        })?;
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map_err(|error| format!("failed to create archive timestamp: {error}"))?
            .as_secs();
        let archive_path = archive_dir.join(format!("{workspace_name}-{timestamp}"));
        fs::rename(&agent_dir_path, &archive_path).map_err(|error| {
            format!(
                "failed to archive {} to {}: {error}",
                agent_dir_path.display(),
                archive_path.display()
            )
        })?;
        format!("Archived previous workspace: {}", archive_path.display())
    } else {
        "No existing workspace found; creating a fresh one.".to_string()
    };

    let create_output =
        setup_os_create_portfolio_example(agent_dir, seed_path.display().to_string()).map_err(|error| {
            format!("{archive_note}\nReset could not recreate the workspace: {error}")
        })?;

    Ok(format!(
        "Portfolio workspace reset complete.\n{archive_note}\n\n{create_output}"
    ))
}

#[tauri::command]
fn setup_os_preview_portfolio_conversation(conversation_path: String) -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let conversation_path = resolve_user_path(&repo_dir, &conversation_path)?;
    if !conversation_path.exists() {
        return Ok(format!(
            "Portfolio conversation preview\n{}\n\n- MISSING: conversation file\nNext: choose an existing Markdown or TXT export before importing.",
            conversation_path.display()
        ));
    }
    if !conversation_path.is_file() {
        return Ok(format!(
            "Portfolio conversation preview\n{}\n\n- MISSING: regular file\nNext: choose a Markdown or TXT file, not a directory.",
            conversation_path.display()
        ));
    }

    let content = fs::read_to_string(&conversation_path)
        .map_err(|error| format!("failed to read {}: {error}", conversation_path.display()))?;
    let lowercase = content.to_lowercase();
    let line_count = content.lines().count();
    let word_count = content.split_whitespace().count();
    let portfolio_mentions = count_keyword(&lowercase, "portfolio");
    let risk_mentions = count_keyword(&lowercase, "risk");
    let watchlist_mentions = count_keyword(&lowercase, "watchlist");
    let strategy_mentions = count_keyword(&lowercase, "strategy");
    let ticker_like_mentions = content
        .split(|character: char| !character.is_ascii_alphanumeric())
        .filter(|token| token.len() >= 2 && token.len() <= 5 && token.chars().all(|character| character.is_ascii_uppercase()))
        .count();

    let mut lines = vec![
        "Portfolio conversation preview".to_string(),
        conversation_path.display().to_string(),
        "".to_string(),
        "- OK: readable file".to_string(),
        format!("- Size: {} bytes", content.len()),
        format!("- Lines: {line_count}"),
        format!("- Words: {word_count}"),
        format!("- Portfolio mentions: {portfolio_mentions}"),
        format!("- Risk mentions: {risk_mentions}"),
        format!("- Strategy mentions: {strategy_mentions}"),
        format!("- Watchlist mentions: {watchlist_mentions}"),
        format!("- Ticker-like tokens: {ticker_like_mentions}"),
        "- No files were imported or mutated.".to_string(),
    ];

    if word_count < 50 {
        lines.push("Next: this looks short; use a fuller saved conversation for better memory drafts.".to_string());
    } else if portfolio_mentions == 0 && risk_mentions == 0 && strategy_mentions == 0 {
        lines.push("Next: this is readable, but it may not be a Portfolio Management conversation.".to_string());
    } else {
        lines.push("Next: run Import, then Extract drafts, then Review drafts.".to_string());
    }

    Ok(lines.join("\n"))
}

#[tauri::command]
fn setup_os_run_portfolio_report(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
    ensure_generated_portfolio_file(&agent_dir, "report.py")?;

    let repo_dir = setup_os_repo_dir()?;
    let python = resolve_python_command(&repo_dir);
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
fn setup_os_review_portfolio_report_sections(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
    let report_path = agent_dir.join("reports").join("daily_report.md");
    if !report_path.exists() {
        return Ok(format!(
            "No Portfolio report yet.\nExpected report: {}\nNext: run the Portfolio report first.",
            report_path.display()
        ));
    }

    let report = fs::read_to_string(&report_path)
        .map_err(|error| format!("failed to read {}: {error}", report_path.display()))?;
    let sections = format_markdown_sections(&report);
    Ok(format!(
        "Portfolio report sections\n{}\n\n{}",
        report_path.display(),
        sections
    ))
}

#[tauri::command]
fn setup_os_review_portfolio_insights(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
    let report_path = agent_dir.join("reports").join("daily_report.md");
    if !report_path.exists() {
        return Ok(format!(
            "No Portfolio insights yet.\nExpected report: {}\nNext: run the Portfolio report first.",
            report_path.display()
        ));
    }

    let report = fs::read_to_string(&report_path)
        .map_err(|error| format!("failed to read {}: {error}", report_path.display()))?;
    let insights = format_portfolio_insights(&report);
    Ok(format!(
        "Portfolio dashboard insights\n{}\n\n{}",
        report_path.display(),
        insights
    ))
}

#[tauri::command]
fn setup_os_check_portfolio_health(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
    ensure_generated_portfolio_file(&agent_dir, "health.py")?;

    let repo_dir = setup_os_repo_dir()?;
    let python = resolve_python_command(&repo_dir);
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
fn setup_os_write_portfolio_handoff(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
    ensure_generated_portfolio_file(&agent_dir, "handoff.py")?;

    let repo_dir = setup_os_repo_dir()?;
    let python = resolve_python_command(&repo_dir);
    let output = Command::new(python)
        .arg("handoff.py")
        .current_dir(&agent_dir)
        .output()
        .map_err(|error| format!("failed to write Portfolio local utility handoff: {error}"))?;

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr).to_string();
        return Err(format!(
            "Portfolio handoff command exited with {}: {stderr}",
            output.status
        ));
    }

    let handoff_path = agent_dir.join("handoff.md");
    let handoff = fs::read_to_string(&handoff_path)
        .map_err(|error| format!("failed to read {}: {error}", handoff_path.display()))?;
    Ok(format!(
        "Portfolio local utility handoff\n{}\n\n{}",
        handoff_path.display(),
        handoff
    ))
}

#[tauri::command]
fn setup_os_review_portfolio_handoff_guidance(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
    let handoff_path = agent_dir.join("handoff.md");
    if !handoff_path.exists() {
        return Ok(format!(
            "No local utility handoff yet.\nExpected handoff: {}\nNext: run Write handoff or Run demo flow.",
            handoff_path.display()
        ));
    }

    let handoff = fs::read_to_string(&handoff_path)
        .map_err(|error| format!("failed to read {}: {error}", handoff_path.display()))?;
    Ok(format!(
        "Portfolio handoff guidance\n{}\n\n{}",
        handoff_path.display(),
        format_handoff_guidance(&handoff)
    ))
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

    let repo_dir = setup_os_repo_dir()?;
    let python = resolve_python_command(&repo_dir);
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

    let readable_drafts = drafts
        .lines()
        .filter(|line| !line.trim().is_empty())
        .enumerate()
        .map(|(index, line)| format_memory_draft(index + 1, line))
        .collect::<Vec<_>>()
        .join("\n\n");

    Ok(format!(
        "Structured memory drafts\n{}\n\n{}",
        drafts_path.display(),
        readable_drafts
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
        (
            "Local utility handoff",
            agent_dir.join("handoff.md").exists(),
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
    let handoff_path = agent_dir.join("handoff.md");
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
        format!("- {}", existence_line("Local utility handoff", handoff_path.exists())),
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
fn setup_os_read_runtime_node_log(agent_dir: String) -> Result<String, String> {
    let agent_dir = resolve_agent_dir(&agent_dir)?;
    let log_path = agent_dir.join(".setup_os").join("runtime_node.jsonl");
    if !log_path.exists() {
        return Ok(format!(
            "No runtime node log yet.\nExpected log: {}\nNext: run python runtime_node.py from the generated agent directory.",
            log_path.display()
        ));
    }

    let log = fs::read_to_string(&log_path)
        .map_err(|error| format!("failed to read {}: {error}", log_path.display()))?;
    if log.trim().is_empty() {
        return Ok(format!(
            "Runtime node log is empty.\nLog: {}\nNext: run python runtime_node.py from the generated agent directory.",
            log_path.display()
        ));
    }

    let recent_entries = log
        .lines()
        .filter(|line| !line.trim().is_empty())
        .rev()
        .take(5)
        .collect::<Vec<_>>()
        .into_iter()
        .rev()
        .collect::<Vec<_>>()
        .join("\n");

    Ok(format!(
        "Runtime node log\n{}\n\nRecent cycles\n{}",
        log_path.display(),
        recent_entries
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
    append_demo_step(
        &mut transcript,
        "Write local utility handoff",
        setup_os_write_portfolio_handoff(agent_dir.clone()),
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

fn format_handoff_guidance(handoff: &str) -> String {
    let readiness = extract_markdown_section(handoff, "Readiness");
    let counts = extract_markdown_section(handoff, "Current Counts");
    let runtime = extract_markdown_section(handoff, "Runtime Status");
    let next_steps = extract_markdown_section(handoff, "Next Local Steps");
    let missing = readiness
        .lines()
        .filter(|line| line.contains("MISSING"))
        .collect::<Vec<_>>();

    let mut lines = vec!["## Immediate Guidance".to_string()];
    if missing.is_empty() {
        lines.push("- Core handoff readiness items are present.".to_string());
    } else {
        lines.push("- Fix missing readiness items first:".to_string());
        lines.extend(missing.iter().map(|line| format!("  {line}")));
    }

    if !runtime.trim().is_empty() {
        lines.push("\n## Runtime Status".to_string());
        lines.push(runtime.trim().to_string());
    }

    if !counts.trim().is_empty() {
        lines.push("\n## Counts".to_string());
        lines.push(counts.trim().to_string());
    }

    if !next_steps.trim().is_empty() {
        lines.push("\n## Next Local Steps".to_string());
        lines.push(next_steps.trim().to_string());
    }

    lines.join("\n")
}

fn extract_markdown_section(markdown: &str, heading: &str) -> String {
    let heading_line = format!("## {heading}");
    let mut lines = Vec::new();
    let mut inside = false;
    for line in markdown.lines() {
        if line.trim() == heading_line {
            inside = true;
            continue;
        }
        if inside && line.starts_with("## ") {
            break;
        }
        if inside {
            lines.push(line);
        }
    }
    lines.join("\n").trim().to_string()
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

    let python = resolve_python_command(&repo_dir);
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

fn format_memory_draft(index: usize, json_line: &str) -> String {
    let source = json_string_value(json_line, "source_name").unwrap_or_else(|| "unknown source".to_string());
    let status = json_string_value(json_line, "status").unwrap_or_else(|| "unknown".to_string());
    let confidence = json_number_value(json_line, "confidence").unwrap_or_else(|| "unknown".to_string());
    let strategy_notes = json_array_values(json_line, "strategy_notes");
    let risk_rules = json_array_values(json_line, "risk_rules");
    let watchlist = json_array_values(json_line, "watchlist");

    [
        format!("Draft {index}"),
        format!("- Source: {source}"),
        format!("- Status: {status}"),
        format!("- Confidence: {confidence}"),
        format!("- Strategy notes: {}", list_or_none(&strategy_notes)),
        format!("- Risk rules: {}", list_or_none(&risk_rules)),
        format!("- Watchlist: {}", list_or_none(&watchlist)),
        "- Next: review these drafts before changing strategy, policy, or alerts.".to_string(),
    ]
    .join("\n")
}

fn json_string_value(json_line: &str, key: &str) -> Option<String> {
    let needle = format!("\"{key}\":");
    let start = json_line.find(&needle)? + needle.len();
    let after_key = json_line[start..].trim_start();
    if after_key.starts_with("null") {
        return None;
    }
    let value_start = after_key.find('"')? + 1;
    let remainder = &after_key[value_start..];
    let value_end = remainder.find('"')?;
    Some(remainder[..value_end].to_string())
}

fn json_number_value(json_line: &str, key: &str) -> Option<String> {
    let needle = format!("\"{key}\":");
    let start = json_line.find(&needle)? + needle.len();
    let after_key = json_line[start..].trim_start();
    let value = after_key
        .chars()
        .take_while(|character| character.is_ascii_digit() || *character == '.')
        .collect::<String>();
    if value.is_empty() {
        None
    } else {
        Some(value)
    }
}

fn json_array_values(json_line: &str, key: &str) -> Vec<String> {
    let needle = format!("\"{key}\":");
    let Some(start) = json_line.find(&needle) else {
        return Vec::new();
    };
    let after_key = &json_line[start + needle.len()..];
    let Some(open) = after_key.find('[') else {
        return Vec::new();
    };
    let Some(close) = after_key[open..].find(']') else {
        return Vec::new();
    };
    let array_body = &after_key[open + 1..open + close];
    array_body
        .split('"')
        .enumerate()
        .filter_map(|(index, segment)| {
            if index % 2 == 1 && !segment.trim().is_empty() {
                Some(segment.to_string())
            } else {
                None
            }
        })
        .collect()
}

fn list_or_none(values: &[String]) -> String {
    if values.is_empty() {
        "none found".to_string()
    } else {
        values.join("; ")
    }
}

fn count_keyword(text: &str, keyword: &str) -> usize {
    text.matches(keyword).count()
}

fn format_markdown_sections(markdown: &str) -> String {
    let mut sections: Vec<(String, Vec<String>)> = Vec::new();
    let mut current_title = "Overview".to_string();
    let mut current_lines: Vec<String> = Vec::new();

    for line in markdown.lines() {
        let trimmed = line.trim();
        if let Some(title) = trimmed.strip_prefix("# ") {
            if !current_lines.is_empty() || !sections.is_empty() {
                sections.push((current_title, current_lines));
                current_lines = Vec::new();
            }
            current_title = title.to_string();
        } else if let Some(title) = trimmed.strip_prefix("## ") {
            sections.push((current_title, current_lines));
            current_title = title.to_string();
            current_lines = Vec::new();
        } else if !trimmed.is_empty() {
            current_lines.push(trimmed.to_string());
        }
    }

    sections.push((current_title, current_lines));
    sections
        .into_iter()
        .filter(|(_, lines)| !lines.is_empty())
        .map(|(title, lines)| {
            let preview = lines.into_iter().take(8).collect::<Vec<_>>().join("\n");
            format!("## {title}\n{preview}")
        })
        .collect::<Vec<_>>()
        .join("\n\n")
}

fn format_portfolio_insights(markdown: &str) -> String {
    let selected_titles = [
        "Holdings",
        "Alerts",
        "Recent Transactions",
        "Cash",
        "Watchlist",
        "Market Snapshot",
        "Performance",
    ];
    let mut sections: Vec<(String, Vec<String>)> = Vec::new();
    let mut current_title = "Overview".to_string();
    let mut current_lines: Vec<String> = Vec::new();

    for line in markdown.lines() {
        let trimmed = line.trim();
        if let Some(title) = trimmed.strip_prefix("# ") {
            if selected_titles.contains(&current_title.as_str()) {
                sections.push((current_title, current_lines));
            }
            current_title = title.to_string();
            current_lines = Vec::new();
        } else if let Some(title) = trimmed.strip_prefix("## ") {
            if selected_titles.contains(&current_title.as_str()) {
                sections.push((current_title, current_lines));
            }
            current_title = title.to_string();
            current_lines = Vec::new();
        } else if !trimmed.is_empty() {
            current_lines.push(trimmed.to_string());
        }
    }

    if selected_titles.contains(&current_title.as_str()) {
        sections.push((current_title, current_lines));
    }

    let formatted = sections
        .into_iter()
        .filter(|(_, lines)| !lines.is_empty())
        .map(|(title, lines)| {
            let preview = lines.into_iter().take(6).collect::<Vec<_>>().join("\n");
            format!("## {title}\n{preview}")
        })
        .collect::<Vec<_>>();

    if formatted.is_empty() {
        "No dashboard insight sections found yet. Run the generated report after importing local Portfolio data.".to_string()
    } else {
        formatted.join("\n\n")
    }
}

fn run_setup_os<const N: usize>(args: [&str; N]) -> Result<String, String> {
    let repo_dir = setup_os_repo_dir()?;
    let python = resolve_python_command(&repo_dir);
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

fn resolve_python_command(repo_dir: &PathBuf) -> String {
    if let Ok(python) = std::env::var("SETUP_OS_PYTHON") {
        if !python.trim().is_empty() {
            return python;
        }
    }

    for candidate in sidecar_python_candidates(repo_dir) {
        if candidate.exists() {
            return candidate.display().to_string();
        }
    }

    "python".to_string()
}

fn sidecar_python_candidates(repo_dir: &PathBuf) -> Vec<PathBuf> {
    let sidecar_dir = repo_dir
        .join("apps")
        .join("desktop")
        .join("src-tauri")
        .join("sidecar")
        .join("python");

    vec![
        sidecar_dir.join("python.exe"),
        sidecar_dir.join("python"),
        sidecar_dir.join("bin").join("python"),
        sidecar_dir.join("bin").join("python3"),
    ]
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
            setup_os_python_runtime_status,
            setup_os_desktop_release_readiness,
            setup_os_run_local_utility_smoke_test,
            setup_os_check_desktop_readiness,
            setup_os_create_portfolio_example,
            setup_os_reset_portfolio_workspace,
            setup_os_preview_portfolio_conversation,
            setup_os_run_portfolio_report,
            setup_os_review_portfolio_report_sections,
            setup_os_review_portfolio_insights,
            setup_os_check_portfolio_health,
            setup_os_write_portfolio_handoff,
            setup_os_review_portfolio_handoff_guidance,
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
            setup_os_read_runtime_node_log,
            setup_os_run_portfolio_demo_flow
        ])
        .run(tauri::generate_context!())
        .expect("error while running Setup OS desktop app");
}
