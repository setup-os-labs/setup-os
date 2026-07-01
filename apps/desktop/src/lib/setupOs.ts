import { invoke } from "@tauri-apps/api/core";

export async function getSetupOsHelp(): Promise<string> {
  return invoke<string>("setup_os_help");
}

export async function createPortfolioExample(): Promise<string> {
  return invoke<string>("setup_os_create_portfolio_example");
}
