import { invoke } from "@tauri-apps/api/core";

export async function getSetupOsHelp(): Promise<string> {
  return invoke<string>("setup_os_help");
}
