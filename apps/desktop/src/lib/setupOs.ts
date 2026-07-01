import { invoke } from "@tauri-apps/api/core";

export async function getSetupOsHelp(): Promise<string> {
  return invoke<string>("setup_os_help");
}

export async function createPortfolioExample(): Promise<string> {
  return invoke<string>("setup_os_create_portfolio_example");
}

export async function runPortfolioReport(): Promise<string> {
  return invoke<string>("setup_os_run_portfolio_report");
}

export async function checkPortfolioHealth(): Promise<string> {
  return invoke<string>("setup_os_check_portfolio_health");
}

export async function importPortfolioConversation(conversationPath: string): Promise<string> {
  return invoke<string>("setup_os_import_portfolio_conversation", { conversationPath });
}

export async function importPortfolioHoldings(holdingsPath: string): Promise<string> {
  return invoke<string>("setup_os_import_portfolio_holdings", { holdingsPath });
}

export async function importPortfolioTransactions(transactionsPath: string): Promise<string> {
  return invoke<string>("setup_os_import_portfolio_transactions", { transactionsPath });
}

export async function importPortfolioCash(cashPath: string): Promise<string> {
  return invoke<string>("setup_os_import_portfolio_cash", { cashPath });
}

export async function importPortfolioWatchlist(watchlistPath: string): Promise<string> {
  return invoke<string>("setup_os_import_portfolio_watchlist", { watchlistPath });
}

export async function importPortfolioMarketData(marketDataPath: string): Promise<string> {
  return invoke<string>("setup_os_import_portfolio_market_data", { marketDataPath });
}

export async function extractPortfolioMemory(): Promise<string> {
  return invoke<string>("setup_os_extract_portfolio_memory");
}

export async function getPortfolioStatus(): Promise<string> {
  return invoke<string>("setup_os_portfolio_status");
}
