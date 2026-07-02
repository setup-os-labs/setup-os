import {
  Bell,
  Bot,
  CheckCircle2,
  FileText,
  FolderInput,
  Play,
  RefreshCcw,
  Stethoscope,
  ShieldCheck,
} from "lucide-react";
import type { ReactNode } from "react";
import { useEffect, useState } from "react";
import {
  checkDesktopReadiness,
  checkPortfolioHealth,
  createPortfolioExample,
  extractPortfolioMemory,
  getDesktopReleaseReadiness,
  getPythonRuntimeStatus,
  getSetupOsHelp,
  getPortfolioSummary,
  getPortfolioStatus,
  importPortfolioCash,
  importPortfolioConversation as importPortfolioConversationFile,
  importPortfolioHoldings,
  importPortfolioMarketData,
  importPortfolioTransactions,
  importPortfolioWatchlist,
  readPortfolioNotifications,
  readRuntimeNodeLog,
  resetPortfolioWorkspace,
  reviewPortfolioMemoryDrafts,
  reviewPortfolioInsights,
  reviewPortfolioReportSections,
  runLocalUtilitySmokeTest,
  runPortfolioDemoFlow,
  runPortfolioReport,
} from "./lib/setupOs";
import "./styles.css";

const agents = [
  {
    name: "Portfolio Management OS",
    status: "Design locked",
    detail: "Raw-first conversation memory, read-only Robinhood path, reports and alerts first.",
    badge: "Next vertical",
  },
  {
    name: "Health OS",
    status: "Blueprint ready",
    detail: "Local reports and medical-action safety boundaries.",
    badge: "Scaffold",
  },
];

const activity = [
  "Portfolio stack research merged",
  "Desktop packaging decision accepted",
  "Notification inbox schema available",
  "Evolution proposals require approval",
];

type DataImportPaths = {
  holdings: string;
  transactions: string;
  cash: string;
  watchlist: string;
  marketData: string;
};

type PortfolioDashboard = {
  workspace: string;
  health: string;
  report: string;
  notifications: string;
  drafts: string;
};

const defaultDataImportPaths: DataImportPaths = {
  holdings: "examples/portfolio_snapshot.csv",
  transactions: "examples/portfolio_transactions.csv",
  cash: "examples/portfolio_cash.csv",
  watchlist: "examples/portfolio_watchlist.csv",
  marketData: "examples/portfolio_market_data.csv",
};

function readStoredValue(key: string, fallback: string) {
  return window.localStorage.getItem(key) || fallback;
}

function readStoredDataImportPaths(): DataImportPaths {
  const stored = window.localStorage.getItem("setup-os:portfolio-data-import-paths");
  if (!stored) {
    return defaultDataImportPaths;
  }

  try {
    return { ...defaultDataImportPaths, ...JSON.parse(stored) } as DataImportPaths;
  } catch {
    return defaultDataImportPaths;
  }
}

function parsePortfolioDashboard(output: string): PortfolioDashboard {
  const valueAfter = (prefix: string, fallback: string) =>
    output
      .split("\n")
      .find((line) => line.startsWith(prefix))
      ?.slice(prefix.length)
      .trim() || fallback;

  return {
    workspace: valueAfter("Workspace:", "Not loaded"),
    health: valueAfter("- OK: Health command", valueAfter("- MISSING: Health command", "Unknown")),
    report: valueAfter("- OK: Latest report", valueAfter("- MISSING: Latest report", "Unknown")),
    notifications: valueAfter("- OK: Notifications", valueAfter("- MISSING: Notifications", "Unknown")),
    drafts: valueAfter("- OK: Structured memory drafts", valueAfter("- MISSING: Structured memory drafts", "Unknown")),
  };
}

export function App() {
  const [cliStatus, setCliStatus] = useState("Not checked");
  const [cliOutput, setCliOutput] = useState("");
  const [actionStatus, setActionStatus] = useState("Ready");
  const [portfolioOutputPath, setPortfolioOutputPath] = useState(() =>
    readStoredValue("setup-os:portfolio-output-path", "generated/desktop-portfolio-os"),
  );
  const [seedConversationPath, setSeedConversationPath] = useState(() =>
    readStoredValue("setup-os:portfolio-seed-conversation-path", "examples/portfolio_conversation.md"),
  );
  const [conversationPath, setConversationPath] = useState(() =>
    readStoredValue("setup-os:portfolio-conversation-path", "examples/portfolio_update.md"),
  );
  const [dataImportPaths, setDataImportPaths] = useState<DataImportPaths>(readStoredDataImportPaths);
  const [portfolioDashboard, setPortfolioDashboard] = useState<PortfolioDashboard>({
    workspace: "Not loaded",
    health: "Unknown",
    report: "Unknown",
    notifications: "Unknown",
    drafts: "Unknown",
  });

  useEffect(() => {
    window.localStorage.setItem("setup-os:portfolio-output-path", portfolioOutputPath);
  }, [portfolioOutputPath]);

  useEffect(() => {
    window.localStorage.setItem("setup-os:portfolio-seed-conversation-path", seedConversationPath);
  }, [seedConversationPath]);

  useEffect(() => {
    window.localStorage.setItem("setup-os:portfolio-conversation-path", conversationPath);
  }, [conversationPath]);

  useEffect(() => {
    window.localStorage.setItem("setup-os:portfolio-data-import-paths", JSON.stringify(dataImportPaths));
  }, [dataImportPaths]);

  function requirePath(label: string, value: string) {
    if (value.trim()) {
      return true;
    }

    setActionStatus("Needs attention");
    setCliOutput(`${label} is required before running this action.`);
    return false;
  }

  function requirePortfolioOutput() {
    return requirePath("Portfolio output path", portfolioOutputPath);
  }

  async function checkCli() {
    setCliStatus("Checking");
    try {
      const output = await getSetupOsHelp();
      setCliOutput(output);
      setCliStatus("Ready");
    } catch (error) {
      setCliStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function checkPythonRuntime() {
    setCliStatus("Checking");
    setActionStatus("Checking runtime");
    try {
      const output = await getPythonRuntimeStatus();
      setCliOutput(output);
      setCliStatus(output.includes("MISSING") || output.includes("failed") ? "Needs attention" : "Ready");
      setActionStatus("Runtime checked");
    } catch (error) {
      setCliStatus("Needs attention");
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function checkReadiness() {
    if (!requirePortfolioOutput() || !requirePath("Seed conversation path", seedConversationPath)) {
      return;
    }

    setCliStatus("Checking");
    setActionStatus("Checking readiness");
    try {
      const output = await checkDesktopReadiness(portfolioOutputPath, seedConversationPath);
      setCliOutput(output);
      setCliStatus(output.includes("MISSING") ? "Needs attention" : "Ready");
      setActionStatus("Readiness checked");
    } catch (error) {
      setCliStatus("Needs attention");
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function checkReleaseReadiness() {
    setActionStatus("Checking release readiness");
    try {
      const output = await getDesktopReleaseReadiness();
      setCliOutput(output);
      setActionStatus("Release readiness checked");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function runLocalSmokeTest() {
    setActionStatus("Running local smoke test");
    setCliOutput("Running the local Setup OS utility smoke test...");
    try {
      const output = await runLocalUtilitySmokeTest();
      setCliOutput(output);
      setActionStatus("Smoke test passed");
      setCliStatus("Ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function createPortfolioAgent() {
    if (!requirePortfolioOutput() || !requirePath("Seed conversation path", seedConversationPath)) {
      return;
    }

    setActionStatus("Generating");
    setCliOutput(`Creating Portfolio Management OS in ${portfolioOutputPath} from ${seedConversationPath}...`);
    try {
      const output = await createPortfolioExample(portfolioOutputPath, seedConversationPath);
      setCliOutput(output);
      setActionStatus("Generated");
      setCliStatus("Ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function resetPortfolioAgent() {
    if (!requirePortfolioOutput() || !requirePath("Seed conversation path", seedConversationPath)) {
      return;
    }

    const confirmed = window.confirm(
      `Archive and recreate the Portfolio workspace at ${portfolioOutputPath}?`,
    );
    if (!confirmed) {
      setActionStatus("Reset cancelled");
      return;
    }

    setActionStatus("Resetting workspace");
    setCliOutput(`Archiving and recreating ${portfolioOutputPath} from ${seedConversationPath}...`);
    try {
      const output = await resetPortfolioWorkspace(portfolioOutputPath, seedConversationPath);
      setCliOutput(output);
      setActionStatus("Workspace reset");
      setCliStatus("Ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function runPortfolioAgentReport() {
    if (!requirePortfolioOutput()) {
      return;
    }

    setActionStatus("Running report");
    setCliOutput("Running generated Portfolio Management OS report...");
    try {
      const output = await runPortfolioReport(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Report ready");
      setCliStatus("Ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function reviewPortfolioReport() {
    if (!requirePortfolioOutput()) {
      return;
    }

    setActionStatus("Reviewing report");
    try {
      const output = await reviewPortfolioReportSections(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Report sections loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function checkPortfolioAgentHealth() {
    if (!requirePortfolioOutput()) {
      return;
    }

    setActionStatus("Checking health");
    setCliOutput("Running generated Portfolio Management OS health check...");
    try {
      const output = await checkPortfolioHealth(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Healthy");
      setCliStatus("Ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function reviewPortfolioDashboardInsights() {
    if (!requirePortfolioOutput()) {
      return;
    }

    setActionStatus("Reviewing insights");
    try {
      const output = await reviewPortfolioInsights(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Insights loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function importPortfolioConversationFromPath() {
    if (!requirePortfolioOutput() || !requirePath("Conversation path", conversationPath)) {
      return;
    }

    setActionStatus("Importing conversation");
    setCliOutput(`Importing ${conversationPath} into raw Portfolio memory...`);
    try {
      const output = await importPortfolioConversationFile(portfolioOutputPath, conversationPath);
      setCliOutput(output);
      setActionStatus("Conversation imported");
      setCliStatus("Ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function importPortfolioData(kind: keyof DataImportPaths) {
    const path = dataImportPaths[kind];
    const labels = {
      holdings: "holdings",
      transactions: "transactions",
      cash: "cash",
      watchlist: "watchlist",
      marketData: "market data",
    };
    const actions = {
      holdings: importPortfolioHoldings,
      transactions: importPortfolioTransactions,
      cash: importPortfolioCash,
      watchlist: importPortfolioWatchlist,
      marketData: importPortfolioMarketData,
    };

    if (!requirePortfolioOutput() || !requirePath(`${labels[kind]} path`, path)) {
      return;
    }

    setActionStatus(`Importing ${labels[kind]}`);
    setCliOutput(`Importing ${path} into Portfolio ${labels[kind]}...`);
    try {
      const output = await actions[kind](portfolioOutputPath, path);
      setCliOutput(output);
      setActionStatus(`${labels[kind]} imported`);
      setCliStatus("Ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  function updateDataImportPath(kind: keyof DataImportPaths, value: string) {
    setDataImportPaths((current) => ({ ...current, [kind]: value }));
  }

  async function extractPortfolioMemoryDrafts() {
    if (!requirePortfolioOutput()) {
      return;
    }

    setActionStatus("Extracting memory");
    setCliOutput("Extracting review-only Portfolio memory drafts...");
    try {
      const output = await extractPortfolioMemory(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Memory drafts ready");
      setCliStatus("Ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function reviewPortfolioDrafts() {
    if (!requirePortfolioOutput()) {
      return;
    }

    setActionStatus("Reviewing drafts");
    try {
      const output = await reviewPortfolioMemoryDrafts(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Drafts loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function refreshPortfolioStatus() {
    if (!requirePortfolioOutput()) {
      return;
    }

    setActionStatus("Refreshing status");
    try {
      const output = await getPortfolioStatus(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Status refreshed");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function loadPortfolioSummary() {
    if (!requirePortfolioOutput()) {
      return;
    }

    setActionStatus("Loading summary");
    try {
      const output = await getPortfolioSummary(portfolioOutputPath);
      setCliOutput(output);
      setPortfolioDashboard(parsePortfolioDashboard(output));
      setActionStatus("Summary loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function readPortfolioInbox() {
    if (!requirePortfolioOutput()) {
      return;
    }

    setActionStatus("Reading inbox");
    try {
      const output = await readPortfolioNotifications(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Inbox loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function readRuntimeLog() {
    if (!requirePortfolioOutput()) {
      return;
    }

    setActionStatus("Reading runtime log");
    try {
      const output = await readRuntimeNodeLog(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Runtime log loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function runFullPortfolioFlow() {
    if (!requirePortfolioOutput()) {
      return;
    }

    setActionStatus("Running full flow");
    setCliOutput("Running the full local Portfolio Management OS flow...");
    try {
      const output = await runPortfolioDemoFlow(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Full flow complete");
      setCliStatus("Ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">SO</div>
          <div>
            <h1>Setup OS</h1>
            <p>Local vertical agent launcher</p>
          </div>
        </div>
        <nav aria-label="Primary">
          <a className="active" href="#agents">
            <Bot size={18} /> Agents
          </a>
          <a href="#import">
            <FolderInput size={18} /> Imports
          </a>
          <a href="#proposals">
            <FileText size={18} /> Proposals
          </a>
          <a href="#notifications">
            <Bell size={18} /> Inbox
          </a>
        </nav>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Desktop foundation</p>
            <h2>Vertical Agent Launcher</h2>
          </div>
          <button className="primary" type="button" onClick={checkCli}>
            <RefreshCcw size={17} /> Check engine
          </button>
          <button className="secondary" type="button" onClick={checkPythonRuntime}>
            <Stethoscope size={17} /> Runtime details
          </button>
          <button className="secondary" type="button" onClick={checkReleaseReadiness}>
            <ShieldCheck size={17} /> Release readiness
          </button>
          <button className="secondary" type="button" onClick={runLocalSmokeTest}>
            <CheckCircle2 size={17} /> Local smoke test
          </button>
        </header>

        <section className="status-grid" aria-label="System status">
          <StatusTile label="Python engine" value={cliStatus} icon={<CheckCircle2 size={20} />} />
          <StatusTile label="Memory mode" value="Raw first" icon={<FolderInput size={20} />} />
          <StatusTile label="Policy" value="Approval first" icon={<ShieldCheck size={20} />} />
          <StatusTile label="Release mode" value="Candidate diffs" icon={<FileText size={20} />} />
        </section>

        <section className="dashboard-band" aria-label="Portfolio dashboard">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Portfolio dashboard</p>
              <h3>Selected workspace</h3>
            </div>
            <button className="secondary" type="button" onClick={loadPortfolioSummary}>
              <RefreshCcw size={17} /> Update dashboard
            </button>
          </div>
          <div className="dashboard-grid">
            <DashboardCard label="Workspace" value={portfolioDashboard.workspace} />
            <DashboardCard label="Health" value={portfolioDashboard.health} />
            <DashboardCard label="Report" value={portfolioDashboard.report} />
            <DashboardCard label="Notifications" value={portfolioDashboard.notifications} />
            <DashboardCard label="Memory drafts" value={portfolioDashboard.drafts} />
          </div>
        </section>

        <section id="agents" className="content-band">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Agents</p>
              <h3>Generated systems</h3>
            </div>
            <div className="button-row">
              <button className="primary" type="button" onClick={runFullPortfolioFlow}>
                <Play size={17} /> Run demo flow
              </button>
              <button className="secondary" type="button" onClick={resetPortfolioAgent}>
                <RefreshCcw size={17} /> Reset workspace
              </button>
              <button className="secondary" type="button" onClick={checkReadiness}>
                <ShieldCheck size={17} /> Check readiness
              </button>
              <button className="secondary" type="button" onClick={refreshPortfolioStatus}>
                <RefreshCcw size={17} /> Refresh status
              </button>
              <button className="secondary" type="button" onClick={loadPortfolioSummary}>
                <FileText size={17} /> Load summary
              </button>
              <button className="secondary" type="button" onClick={readPortfolioInbox}>
                <Bell size={17} /> Read inbox
              </button>
              <button className="secondary" type="button" onClick={readRuntimeLog}>
                <FileText size={17} /> Read runtime log
              </button>
              <label className="path-field">
                <span>Output</span>
                <input
                  value={portfolioOutputPath}
                  onChange={(event) => setPortfolioOutputPath(event.target.value)}
                  aria-label="Portfolio output path"
                />
              </label>
              <label className="path-field">
                <span>Seed</span>
                <input
                  value={seedConversationPath}
                  onChange={(event) => setSeedConversationPath(event.target.value)}
                  aria-label="Seed conversation path"
                />
              </label>
              <label className="path-field">
                <span>Conversation</span>
                <input
                  value={conversationPath}
                  onChange={(event) => setConversationPath(event.target.value)}
                  aria-label="Conversation path"
                />
              </label>
              <button className="secondary" type="button" onClick={importPortfolioConversationFromPath}>
                <FolderInput size={17} /> Import
              </button>
              <button className="secondary" type="button" onClick={extractPortfolioMemoryDrafts}>
                <FileText size={17} /> Extract drafts
              </button>
              <button className="secondary" type="button" onClick={reviewPortfolioDrafts}>
                <FileText size={17} /> Review drafts
              </button>
              <button className="secondary" type="button" onClick={checkPortfolioAgentHealth}>
                <Stethoscope size={17} /> Check health
              </button>
              <button className="secondary" type="button" onClick={runPortfolioAgentReport}>
                <FileText size={17} /> Run report
              </button>
              <button className="secondary" type="button" onClick={reviewPortfolioReport}>
                <FileText size={17} /> Review report
              </button>
              <button className="secondary" type="button" onClick={reviewPortfolioDashboardInsights}>
                <FileText size={17} /> Review insights
              </button>
            </div>
          </div>

          <div className="agent-list">
            {agents.map((agent) => (
              <article className="agent-card" key={agent.name}>
                <div>
                  <span>{agent.badge}</span>
                  <h4>{agent.name}</h4>
                  <p>{agent.detail}</p>
                </div>
                <div className="agent-actions">
                  <small>{agent.status}</small>
                  <button
                    aria-label={`Run ${agent.name}`}
                    disabled={agent.name !== "Portfolio Management OS" || actionStatus === "Generating"}
                    title={
                      agent.name === "Portfolio Management OS"
                        ? "Generate the local Portfolio Management OS example"
                        : "This blueprint is available from the CLI"
                    }
                    type="button"
                    onClick={agent.name === "Portfolio Management OS" ? createPortfolioAgent : undefined}
                  >
                    <Play size={17} />
                  </button>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="split">
          <div id="proposals" className="panel">
            <p className="eyebrow">Timeline</p>
            <h3>Recent work</h3>
            <ul>
              {activity.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>

          <div id="import" className="panel">
            <p className="eyebrow">Engine output</p>
            <h3>CLI contract</h3>
            <p className="panel-status">Portfolio action: {actionStatus}</p>
            <pre>{cliOutput || "Run Check engine to call python -m setup_os.cli --help."}</pre>
          </div>
        </section>

        <section className="panel data-imports" aria-label="Portfolio data imports">
          <p className="eyebrow">Portfolio data</p>
          <h3>Local CSV imports</h3>
          <DataImportRow
            label="Holdings"
            value={dataImportPaths.holdings}
            onChange={(value) => updateDataImportPath("holdings", value)}
            onImport={() => importPortfolioData("holdings")}
          />
          <DataImportRow
            label="Transactions"
            value={dataImportPaths.transactions}
            onChange={(value) => updateDataImportPath("transactions", value)}
            onImport={() => importPortfolioData("transactions")}
          />
          <DataImportRow
            label="Cash"
            value={dataImportPaths.cash}
            onChange={(value) => updateDataImportPath("cash", value)}
            onImport={() => importPortfolioData("cash")}
          />
          <DataImportRow
            label="Watchlist"
            value={dataImportPaths.watchlist}
            onChange={(value) => updateDataImportPath("watchlist", value)}
            onImport={() => importPortfolioData("watchlist")}
          />
          <DataImportRow
            label="Market data"
            value={dataImportPaths.marketData}
            onChange={(value) => updateDataImportPath("marketData", value)}
            onImport={() => importPortfolioData("marketData")}
          />
        </section>
      </section>
    </main>
  );
}

function DashboardCard({ label, value }: { label: string; value: string }) {
  return (
    <article className="dashboard-card">
      <p>{label}</p>
      <strong>{value}</strong>
    </article>
  );
}

function StatusTile({
  label,
  value,
  icon,
}: {
  label: string;
  value: string;
  icon: ReactNode;
}) {
  return (
    <div className="status-tile">
      {icon}
      <div>
        <p>{label}</p>
        <strong>{value}</strong>
      </div>
    </div>
  );
}

function DataImportRow({
  label,
  value,
  onChange,
  onImport,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  onImport: () => void;
}) {
  return (
    <div className="data-import-row">
      <label>
        <span>{label}</span>
        <input value={value} onChange={(event) => onChange(event.target.value)} />
      </label>
      <button className="secondary" type="button" onClick={onImport}>
        <FolderInput size={17} /> Import
      </button>
    </div>
  );
}
