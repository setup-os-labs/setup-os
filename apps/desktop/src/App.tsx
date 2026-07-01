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
import { useState } from "react";
import {
  checkPortfolioHealth,
  createPortfolioExample,
  extractPortfolioMemory,
  getSetupOsHelp,
  importPortfolioConversationExample,
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

export function App() {
  const [cliStatus, setCliStatus] = useState("Not checked");
  const [cliOutput, setCliOutput] = useState("");
  const [actionStatus, setActionStatus] = useState("Ready");

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

  async function createPortfolioAgent() {
    setActionStatus("Generating");
    setCliOutput("Creating Portfolio Management OS in generated/desktop-portfolio-os...");
    try {
      const output = await createPortfolioExample();
      setCliOutput(output);
      setActionStatus("Generated");
      setCliStatus("Ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function runPortfolioAgentReport() {
    setActionStatus("Running report");
    setCliOutput("Running generated Portfolio Management OS report...");
    try {
      const output = await runPortfolioReport();
      setCliOutput(output);
      setActionStatus("Report ready");
      setCliStatus("Ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function checkPortfolioAgentHealth() {
    setActionStatus("Checking health");
    setCliOutput("Running generated Portfolio Management OS health check...");
    try {
      const output = await checkPortfolioHealth();
      setCliOutput(output);
      setActionStatus("Healthy");
      setCliStatus("Ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function importPortfolioConversation() {
    setActionStatus("Importing conversation");
    setCliOutput("Importing examples/portfolio_update.md into raw Portfolio memory...");
    try {
      const output = await importPortfolioConversationExample();
      setCliOutput(output);
      setActionStatus("Conversation imported");
      setCliStatus("Ready");
    } catch (error) {
      setActionStatus("Needs attention");
      setCliOutput(error instanceof Error ? error.message : String(error));
    }
  }

  async function extractPortfolioMemoryDrafts() {
    setActionStatus("Extracting memory");
    setCliOutput("Extracting review-only Portfolio memory drafts...");
    try {
      const output = await extractPortfolioMemory();
      setCliOutput(output);
      setActionStatus("Memory drafts ready");
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
        </header>

        <section className="status-grid" aria-label="System status">
          <StatusTile label="Python engine" value={cliStatus} icon={<CheckCircle2 size={20} />} />
          <StatusTile label="Memory mode" value="Raw first" icon={<FolderInput size={20} />} />
          <StatusTile label="Policy" value="Approval first" icon={<ShieldCheck size={20} />} />
          <StatusTile label="Release mode" value="Candidate diffs" icon={<FileText size={20} />} />
        </section>

        <section id="agents" className="content-band">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Agents</p>
              <h3>Generated systems</h3>
            </div>
            <div className="button-row">
              <button className="secondary" type="button" onClick={importPortfolioConversation}>
                <FolderInput size={17} /> Import conversation
              </button>
              <button className="secondary" type="button" onClick={extractPortfolioMemoryDrafts}>
                <FileText size={17} /> Extract drafts
              </button>
              <button className="secondary" type="button" onClick={checkPortfolioAgentHealth}>
                <Stethoscope size={17} /> Check health
              </button>
              <button className="secondary" type="button" onClick={runPortfolioAgentReport}>
                <FileText size={17} /> Run report
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
      </section>
    </main>
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
