import {
  ArrowRight,
  Bell,
  BookOpen,
  Bot,
  CheckCircle2,
  ClipboardCheck,
  Database,
  FileText,
  FolderInput,
  LayoutDashboard,
  Play,
  RefreshCcw,
  Route,
  Settings2,
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
  previewPortfolioConversation,
  readPortfolioNotifications,
  readRuntimeNodeLog,
  resetPortfolioWorkspace,
  reviewPortfolioHandoffGuidance,
  reviewPortfolioFunctionalEvolutionReport,
  reviewPortfolioEvolutionReviewPacket,
  reviewPortfolioExtractorRollback,
  reviewPortfolioMemoryDrafts,
  reviewPortfolioMemoryUpdateReport,
  reviewPortfolioInsights,
  reviewPortfolioReportSections,
  runLocalUtilitySmokeTest,
  runPortfolioDemoFlow,
  runPortfolioReport,
  writePortfolioHandoff,
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
  handoff: string;
  notifications: string;
  drafts: string;
};

type SurfaceId = "work" | "review" | "operator";
type PrimaryNavId = "agents" | "imports" | "proposals" | "inbox";
type GuideId = "start" | "how" | "use";

const surfaces: Array<{
  id: SurfaceId;
  label: string;
  description: string;
  icon: ReactNode;
}> = [
  {
    id: "work",
    label: "Work",
    description: "Create or open the local Portfolio OS loop.",
    icon: <LayoutDashboard size={17} />,
  },
  {
    id: "review",
    label: "Review",
    description: "Inspect reports, memory drafts, handoff, and inbox state.",
    icon: <ClipboardCheck size={17} />,
  },
  {
    id: "operator",
    label: "Operator",
    description: "Run diagnostics, release checks, smoke tests, and logs.",
    icon: <Settings2 size={17} />,
  },
];

const guides: Array<{ id: GuideId; label: string; icon: ReactNode }> = [
  { id: "start", label: "Start", icon: <Play size={16} /> },
  { id: "how", label: "How it works", icon: <Route size={16} /> },
  { id: "use", label: "How to use", icon: <BookOpen size={16} /> },
];

const primaryNav: Array<{
  id: PrimaryNavId;
  label: string;
  title: string;
  description: string;
  surface: SurfaceId;
  icon: ReactNode;
}> = [
  {
    id: "agents",
    label: "Agents",
    title: "Agents",
    description: "Create or run local vertical systems.",
    surface: "work",
    icon: <Bot size={18} />,
  },
  {
    id: "imports",
    label: "Imports",
    title: "Imports",
    description: "Choose local conversations and CSV snapshots.",
    surface: "work",
    icon: <FolderInput size={18} />,
  },
  {
    id: "proposals",
    label: "Proposals",
    title: "Proposals",
    description: "Review reports, memory drafts, evolution packets, and rollback readiness.",
    surface: "review",
    icon: <FileText size={18} />,
  },
  {
    id: "inbox",
    label: "Inbox",
    title: "Inbox",
    description: "Inspect notifications, handoff guidance, runtime logs, and release diagnostics.",
    surface: "operator",
    icon: <Bell size={18} />,
  },
];

const onboardingSteps = [
  { label: "Choose", detail: "Pick a saved conversation." },
  { label: "Generate", detail: "Create the local OS." },
  { label: "Review", detail: "Check outputs before trust." },
];

const systemFlow = ["Conversation", "Spec", "Local OS", "Reports", "Evolution"];

const useSteps = [
  "Run demo flow",
  "Import your conversation",
  "Review report",
  "Write handoff",
];

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
    handoff: valueAfter(
      "- OK: Local utility handoff",
      valueAfter("- MISSING: Local utility handoff", "Unknown"),
    ),
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
    handoff: "Unknown",
    notifications: "Unknown",
    drafts: "Unknown",
  });
  const [activeSurface, setActiveSurface] = useState<SurfaceId>("work");
  const [activePrimaryNav, setActivePrimaryNav] = useState<PrimaryNavId>("agents");
  const [activeGuide, setActiveGuide] = useState<GuideId>("start");

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

  function showActionStart(status: string, output: string) {
    setActionStatus(status);
    setCliOutput(output);
  }

  function openPrimaryNav(item: (typeof primaryNav)[number]) {
    setActivePrimaryNav(item.id);
    setActiveSurface(item.surface);
  }

  function openSurface(surface: SurfaceId) {
    setActiveSurface(surface);
    const fallbackNav = surface === "work" ? "agents" : surface === "review" ? "proposals" : "inbox";
    setActivePrimaryNav(fallbackNav);
  }

  async function checkCli() {
    setCliStatus("Checking");
    showActionStart("Checking engine", "Checking the Setup OS engine...");
    try {
      const output = await getSetupOsHelp();
      setCliOutput(output);
      setCliStatus("Ready");
      setActionStatus("Engine checked");
    } catch (error) {
      setCliStatus("Needs attention");
      setActionStatus("Needs attention");
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
    showActionStart("Checking release readiness", "Checking release readiness...");
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
    showActionStart("Running local smoke test", "Running the local Setup OS utility smoke test...");
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

    showActionStart(
      "Generating",
      `Creating Portfolio Management OS in ${portfolioOutputPath} from ${seedConversationPath}...`,
    );
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

    showActionStart(
      "Resetting workspace",
      `Archiving and recreating ${portfolioOutputPath} from ${seedConversationPath}...`,
    );
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

    showActionStart("Running report", "Running generated Portfolio Management OS report...");
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

    showActionStart("Reviewing report", "Loading generated Portfolio report sections...");
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

    showActionStart("Checking health", "Running generated Portfolio Management OS health check...");
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

    showActionStart("Reviewing insights", "Loading Portfolio dashboard insights...");
    try {
      const output = await reviewPortfolioInsights(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Insights loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function previewPortfolioConversationFromPath() {
    if (!requirePath("Conversation path", conversationPath)) {
      return;
    }

    showActionStart("Previewing conversation", `Previewing ${conversationPath}...`);
    try {
      const output = await previewPortfolioConversation(conversationPath);
      setCliOutput(output);
      setActionStatus("Conversation previewed");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function importPortfolioConversationFromPath() {
    if (!requirePortfolioOutput() || !requirePath("Conversation path", conversationPath)) {
      return;
    }

    showActionStart("Importing conversation", `Importing ${conversationPath} into raw Portfolio memory...`);
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

    showActionStart(`Importing ${labels[kind]}`, `Importing ${path} into Portfolio ${labels[kind]}...`);
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

    showActionStart("Extracting memory", "Extracting review-only Portfolio memory drafts...");
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

    showActionStart("Reviewing drafts", "Loading review-only Portfolio memory drafts...");
    try {
      const output = await reviewPortfolioMemoryDrafts(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Drafts loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function reviewPortfolioMemoryReport() {
    if (!requirePortfolioOutput()) {
      return;
    }

    showActionStart("Reviewing memory report", "Loading the Memory Update Report...");
    try {
      const output = await reviewPortfolioMemoryUpdateReport(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Memory report loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function reviewPortfolioFunctionalEvolution() {
    if (!requirePortfolioOutput()) {
      return;
    }

    showActionStart("Reviewing functional evolution", "Loading the Functional Evolution Report...");
    try {
      const output = await reviewPortfolioFunctionalEvolutionReport(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Functional evolution loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function reviewPortfolioEvolutionPacket() {
    if (!requirePortfolioOutput()) {
      return;
    }

    showActionStart("Reviewing evolution packet", "Loading the Evolution Review Packet...");
    try {
      const output = await reviewPortfolioEvolutionReviewPacket(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Evolution packet loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function reviewPortfolioRollbackReadiness() {
    if (!requirePortfolioOutput()) {
      return;
    }

    showActionStart("Reviewing rollback", "Loading extractor snapshots and rollback readiness...");
    try {
      const output = await reviewPortfolioExtractorRollback(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Rollback review loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function refreshPortfolioStatus() {
    if (!requirePortfolioOutput()) {
      return;
    }

    showActionStart("Refreshing status", "Refreshing Portfolio workspace status...");
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

    showActionStart("Loading summary", "Loading Portfolio dashboard summary...");
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

    showActionStart("Reading inbox", "Reading Portfolio notification inbox...");
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

    showActionStart("Reading runtime log", "Reading runtime node log...");
    try {
      const output = await readRuntimeNodeLog(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Runtime log loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function writeLocalHandoff() {
    if (!requirePortfolioOutput()) {
      return;
    }

    showActionStart("Writing handoff", "Writing local utility handoff...");
    try {
      const output = await writePortfolioHandoff(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Handoff ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function reviewLocalHandoffGuidance() {
    if (!requirePortfolioOutput()) {
      return;
    }

    showActionStart("Reviewing handoff", "Loading handoff guidance...");
    try {
      const output = await reviewPortfolioHandoffGuidance(portfolioOutputPath);
      setCliOutput(output);
      setActionStatus("Handoff guidance loaded");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function runFullPortfolioFlow() {
    if (!requirePortfolioOutput()) {
      return;
    }

    showActionStart("Running full flow", "Running the full local Portfolio Management OS flow...");
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

  const currentPrimaryView = primaryNav.find((item) => item.id === activePrimaryNav) || primaryNav[0];

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
          {primaryNav.map((item) => (
            <button
              className={activePrimaryNav === item.id ? "active" : ""}
              key={item.id}
              type="button"
              onClick={() => openPrimaryNav(item)}
            >
              {item.icon}
              {item.label}
            </button>
          ))}
        </nav>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Setup OS</p>
            <h2>Portfolio OS</h2>
          </div>
          <div className="topbar-actions">
            <button className="primary" type="button" onClick={runFullPortfolioFlow}>
              <Play size={17} /> Run demo flow
            </button>
            <button className="secondary" type="button" onClick={loadPortfolioSummary}>
              <RefreshCcw size={17} /> Update dashboard
            </button>
          </div>
        </header>

        <section className="onboarding-shell" aria-label="Setup OS onboarding">
          <div className="onboarding-main">
            <div className="guide-tabs" aria-label="Onboarding views">
              {guides.map((guide) => (
                <button
                  className={activeGuide === guide.id ? "guide-tab active" : "guide-tab"}
                  key={guide.id}
                  type="button"
                  onClick={() => setActiveGuide(guide.id)}
                >
                  {guide.icon}
                  {guide.label}
                </button>
              ))}
            </div>

            {activeGuide === "start" && (
              <div className="guide-panel">
                <div>
                  <p className="eyebrow">Start here</p>
                  <h3>{actionStatus === "Ready" ? "Create a local Portfolio OS" : actionStatus}</h3>
                </div>
                <div className="step-grid">
                  {onboardingSteps.map((step, index) => (
                    <article className="step-card" key={step.label}>
                      <span>{index + 1}</span>
                      <strong>{step.label}</strong>
                      <small>{step.detail}</small>
                    </article>
                  ))}
                </div>
                <div className="guide-actions">
                  <button className="primary" type="button" onClick={runFullPortfolioFlow}>
                    <ArrowRight size={18} /> Continue
                  </button>
                  <button className="secondary" type="button" onClick={previewPortfolioConversationFromPath}>
                    <FileText size={17} /> Preview input
                  </button>
                </div>
              </div>
            )}

            {activeGuide === "how" && (
              <div className="guide-panel">
                <div>
                  <p className="eyebrow">How it works</p>
                  <h3>Conversation becomes a local system</h3>
                </div>
                <div className="flow-map" aria-label="Setup OS system flow">
                  {systemFlow.map((item, index) => (
                    <div className="flow-node" key={item}>
                      <span>{item}</span>
                      {index < systemFlow.length - 1 && <ArrowRight size={16} />}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeGuide === "use" && (
              <div className="guide-panel">
                <div>
                  <p className="eyebrow">How to use</p>
                  <h3>One low-risk loop</h3>
                </div>
                <div className="use-list">
                  {useSteps.map((step, index) => (
                    <button
                      className={index === 0 ? "use-step active" : "use-step"}
                      key={step}
                      type="button"
                      onClick={index === 0 ? runFullPortfolioFlow : undefined}
                    >
                      <span>{index + 1}</span>
                      {step}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          <aside className="state-panel" aria-label="Current workspace state">
            <p className="eyebrow">Current state</p>
            <StatusTile label="Engine" value={cliStatus} icon={<CheckCircle2 size={18} />} />
            <StatusTile label="Workspace" value={portfolioDashboard.workspace} icon={<LayoutDashboard size={18} />} />
            <StatusTile label="Report" value={portfolioDashboard.report} icon={<FileText size={18} />} />
            <button className="secondary state-button" type="button" onClick={loadPortfolioSummary}>
              <RefreshCcw size={16} /> Refresh
            </button>
          </aside>
        </section>

        <section className="details-drawer" aria-label="Workspace details">
          <details>
            <summary>Workspace details</summary>
            <div className="dashboard-grid">
              <DashboardCard label="Health" value={portfolioDashboard.health} />
              <DashboardCard label="Handoff" value={portfolioDashboard.handoff} />
              <DashboardCard label="Notifications" value={portfolioDashboard.notifications} />
              <DashboardCard label="Memory drafts" value={portfolioDashboard.drafts} />
            </div>
          </details>
        </section>

        <section className="action-output" aria-live="polite" aria-label="Latest action output">
          <div>
            <p className="eyebrow">Latest action</p>
            <h3>{actionStatus}</h3>
          </div>
          <pre>{cliOutput || "Click an action to see status and output here."}</pre>
        </section>

        <section className="surface-tabs" aria-label="Workspace modes">
          {surfaces.map((surface) => (
            <button
              className={activeSurface === surface.id ? "surface-tab active" : "surface-tab"}
              key={surface.id}
              type="button"
              title={surface.description}
              onClick={() => openSurface(surface.id)}
            >
              {surface.icon}
              <span>{surface.label}</span>
            </button>
          ))}
        </section>

        <section className="primary-view-heading" aria-live="polite">
          <div>
            <p className="eyebrow">Current view</p>
            <h3>{currentPrimaryView.title}</h3>
          </div>
          <p>{currentPrimaryView.description}</p>
        </section>

        <section className="content-band">
          {activePrimaryNav === "agents" && (
            <div className="surface-grid">
              <section className="panel action-panel">
                <p className="eyebrow">Work</p>
                <h3>Local Portfolio loop</h3>
                <div className="action-row">
                  <button className="primary" type="button" onClick={createPortfolioAgent}>
                    <Play size={17} /> Create Portfolio OS
                  </button>
                  <button className="secondary" type="button" onClick={previewPortfolioConversationFromPath}>
                    <FileText size={17} /> Preview conversation
                  </button>
                  <button className="secondary" type="button" onClick={importPortfolioConversationFromPath}>
                    <FolderInput size={17} /> Import conversation
                  </button>
                </div>
                <details className="inline-details">
                  <summary>Paths</summary>
                  <div className="path-grid">
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
                  </div>
                </details>
              </section>

              <section className="panel action-panel">
                <p className="eyebrow">Systems</p>
                <h3>Verticals</h3>
                <div className="agent-list compact-list">
                  {agents.map((agent) => (
                    <article className="agent-card" key={agent.name}>
                      <div>
                        <span>{agent.badge}</span>
                        <h4>{agent.name}</h4>
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
            </div>
          )}

          {activePrimaryNav === "imports" && (
            <div className="surface-grid">
              <section className="panel action-panel full-span">
                <p className="eyebrow">Conversation</p>
                <h3>Input paths</h3>
                <div className="action-row">
                  <button className="primary" type="button" onClick={previewPortfolioConversationFromPath}>
                    <FileText size={17} /> Preview conversation
                  </button>
                  <button className="secondary" type="button" onClick={importPortfolioConversationFromPath}>
                    <FolderInput size={17} /> Import conversation
                  </button>
                </div>
                <div className="path-grid visible-path-grid">
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
                </div>
              </section>
              <section className="panel data-imports full-span" aria-label="Portfolio data imports">
                <p className="eyebrow">Local CSV imports</p>
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
            </div>
          )}

          {activePrimaryNav === "proposals" && (
            <div className="surface-grid">
              <section className="panel action-panel">
                <p className="eyebrow">Review</p>
                <h3>Evidence and outputs</h3>
                <div className="action-row">
                  <button className="primary" type="button" onClick={runPortfolioAgentReport}>
                    <FileText size={17} /> Run report
                  </button>
                  <button className="secondary" type="button" onClick={reviewPortfolioReport}>
                    <FileText size={17} /> Review report
                  </button>
                  <button className="secondary" type="button" onClick={reviewPortfolioDashboardInsights}>
                    <Database size={17} /> Review insights
                  </button>
                  <button className="secondary" type="button" onClick={extractPortfolioMemoryDrafts}>
                    <FileText size={17} /> Extract drafts
                  </button>
                  <button className="secondary" type="button" onClick={reviewPortfolioDrafts}>
                    <ClipboardCheck size={17} /> Review drafts
                  </button>
                  <button className="secondary" type="button" onClick={reviewPortfolioMemoryReport}>
                    <FileText size={17} /> Review memory report
                  </button>
                  <button className="secondary" type="button" onClick={reviewPortfolioFunctionalEvolution}>
                    <FileText size={17} /> Review functional evolution
                  </button>
                  <button className="secondary" type="button" onClick={reviewPortfolioEvolutionPacket}>
                    <FileText size={17} /> Review evolution packet
                  </button>
                  <button className="secondary" type="button" onClick={reviewPortfolioRollbackReadiness}>
                    <ShieldCheck size={17} /> Review rollback
                  </button>
                </div>
              </section>

              <section className="panel action-panel">
                <p className="eyebrow">Handoff</p>
                <h3>Local readiness</h3>
                <div className="action-row">
                  <button className="primary" type="button" onClick={writeLocalHandoff}>
                    <FileText size={17} /> Write handoff
                  </button>
                  <button className="secondary" type="button" onClick={reviewLocalHandoffGuidance}>
                    <ClipboardCheck size={17} /> Review guidance
                  </button>
                  <button className="secondary" type="button" onClick={refreshPortfolioStatus}>
                    <RefreshCcw size={17} /> Refresh status
                  </button>
                  <button className="secondary" type="button" onClick={loadPortfolioSummary}>
                    <LayoutDashboard size={17} /> Load summary
                  </button>
                </div>
              </section>
            </div>
          )}

          {activePrimaryNav === "inbox" && (
            <div className="surface-grid">
              <section className="panel action-panel">
                <p className="eyebrow">Inbox</p>
                <h3>Notifications and logs</h3>
                <div className="action-row">
                  <button className="primary" type="button" onClick={readPortfolioInbox}>
                    <Bell size={17} /> Read inbox
                  </button>
                  <button className="secondary" type="button" onClick={readRuntimeLog}>
                    <FileText size={17} /> Runtime log
                  </button>
                  <button className="secondary" type="button" onClick={reviewLocalHandoffGuidance}>
                    <ClipboardCheck size={17} /> Review guidance
                  </button>
                </div>
              </section>

              <section className="panel action-panel">
                <p className="eyebrow">Diagnostics</p>
                <h3>Runtime and health</h3>
                <div className="action-row">
                  <button className="primary" type="button" onClick={checkCli}>
                    <RefreshCcw size={17} /> Check engine
                  </button>
                  <button className="secondary" type="button" onClick={checkPythonRuntime}>
                    <Stethoscope size={17} /> Runtime details
                  </button>
                  <button className="secondary" type="button" onClick={checkPortfolioAgentHealth}>
                    <Stethoscope size={17} /> Check health
                  </button>
                  <button className="secondary" type="button" onClick={checkReadiness}>
                    <ShieldCheck size={17} /> Check readiness
                  </button>
                </div>
              </section>

              <section className="panel action-panel">
                <p className="eyebrow">Release and reset</p>
                <h3>Operator actions</h3>
                <div className="action-row">
                  <button className="primary" type="button" onClick={runLocalSmokeTest}>
                    <CheckCircle2 size={17} /> Local smoke test
                  </button>
                  <button className="secondary" type="button" onClick={checkReleaseReadiness}>
                    <ShieldCheck size={17} /> Release readiness
                  </button>
                  <button className="secondary danger" type="button" onClick={resetPortfolioAgent}>
                    <RefreshCcw size={17} /> Reset workspace
                  </button>
                </div>
              </section>
            </div>
          )}
        </section>

        <section className="details-drawer output-drawer" aria-label="Engine output">
          <details>
            <summary>Engine output</summary>
            <p className="panel-status">Portfolio action: {actionStatus}</p>
            <pre>{cliOutput || "Output appears here after an action."}</pre>
          </details>
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
