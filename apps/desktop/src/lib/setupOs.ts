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

export async function importPortfolioConversationExample(): Promise<string> {
  return invoke<string>("setup_os_import_portfolio_conversation_example");
}

export async function extractPortfolioMemory(): Promise<string> {
  return invoke<string>("setup_os_extract_portfolio_memory");
}
