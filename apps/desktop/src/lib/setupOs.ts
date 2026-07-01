import { invoke } from "@tauri-apps/api/core";

export async function getSetupOsHelp(): Promise<string> {
  return invoke<string>("setup_os_help");
}

export async function createPortfolioExample(agentDir: string, seedConversationPath: string): Promise<string> {
  return invoke<string>("setup_os_create_portfolio_example", { agentDir, seedConversationPath });
}

export async function runPortfolioReport(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_run_portfolio_report", { agentDir });
}

export async function checkPortfolioHealth(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_check_portfolio_health", { agentDir });
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

export async function getPortfolioStatus(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_portfolio_status", { agentDir });
}

export async function readPortfolioNotifications(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_read_portfolio_notifications", { agentDir });
}

export async function runPortfolioDemoFlow(agentDir: string): Promise<string> {
  return invoke<string>("setup_os_run_portfolio_demo_flow", { agentDir });
}
