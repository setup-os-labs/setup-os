import { invoke } from "@tauri-apps/api/core";

export async function getSetupOsHelp(): Promise<string> {
  return invoke<string>("setup_os_help");
}

export async function getPythonRuntimeStatus(): Promise<string> {
  return invoke<string>("setup_os_python_runtime_status");
}

export async function getDesktopReleaseReadiness(): Promise<string> {
  return invoke<string>("setup_os_desktop_release_readiness");
}

export async function runLocalUtilitySmokeTest(): Promise<string> {
  return invoke<string>("setup_os_run_local_utility_smoke_test");
}

export async function checkDesktopReadiness(agentDir: string, seedConversationPath: string): Promise<string> {
  return invoke<string>("setup_os_check_desktop_readiness", { agentDir, seedConversationPath });
}

export async function createPortfolioExample(agentDir: string, seedConversationPath: string): Promise<string> {
  return invoke<string>("setup_os_create_portfolio_example", { agentDir, seedConversationPath });
}

export async function resetPortfolioWorkspace(agentDir: string, seedConversationPath: string): Promise<string> {
  return invoke<string>("setup_os_reset_portfolio_workspace", { agentDir, seedConversationPath });
}

export async function previewPortfolioConversation(conversationPath: string): Promise<string> {
  return invoke<string>("setup_os_preview_portfolio_conversation", { conversationPath });
}

export async function runPortfolioReport(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_run_portfolio_report", { agentDir });
}

export async function reviewPortfolioReportSections(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_review_portfolio_report_sections", { agentDir });
}

export async function reviewPortfolioInsights(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_review_portfolio_insights", { agentDir });
}

export async function checkPortfolioHealth(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_check_portfolio_health", { agentDir });
}

export async function writePortfolioHandoff(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_write_portfolio_handoff", { agentDir });
}

export async function reviewPortfolioHandoffGuidance(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_review_portfolio_handoff_guidance", { agentDir });
}

export async function importPortfolioConversation(agentDir: string, conversationPath: string): Promise<string> {
  return invoke<string>("setup_os_import_portfolio_conversation", { agentDir, conversationPath });
}

export async function importPortfolioHoldings(agentDir: string, holdingsPath: string): Promise<string> {
  return invoke<string>("setup_os_import_portfolio_holdings", { agentDir, holdingsPath });
}

export async function importPortfolioTransactions(agentDir: string, transactionsPath: string): Promise<string> {
  return invoke<string>("setup_os_import_portfolio_transactions", { agentDir, transactionsPath });
}

export async function importPortfolioCash(agentDir: string, cashPath: string): Promise<string> {
  return invoke<string>("setup_os_import_portfolio_cash", { agentDir, cashPath });
}

export async function importPortfolioWatchlist(agentDir: string, watchlistPath: string): Promise<string> {
  return invoke<string>("setup_os_import_portfolio_watchlist", { agentDir, watchlistPath });
}

export async function importPortfolioMarketData(agentDir: string, marketDataPath: string): Promise<string> {
  return invoke<string>("setup_os_import_portfolio_market_data", { agentDir, marketDataPath });
}

export async function extractPortfolioMemory(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_extract_portfolio_memory", { agentDir });
}

export async function reviewPortfolioMemoryDrafts(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_review_portfolio_memory_drafts", { agentDir });
}

export async function reviewPortfolioMemoryUpdateReport(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_review_portfolio_memory_update_report", { agentDir });
}

export async function reviewPortfolioExtractionObservability(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_review_portfolio_extraction_observability", { agentDir });
}

export async function getPortfolioStatus(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_portfolio_status", { agentDir });
}

export async function getPortfolioSummary(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_portfolio_summary", { agentDir });
}

export async function readPortfolioNotifications(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_read_portfolio_notifications", { agentDir });
}

export async function readRuntimeNodeLog(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_read_runtime_node_log", { agentDir });
}

export async function runPortfolioDemoFlow(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_run_portfolio_demo_flow", { agentDir });
}
