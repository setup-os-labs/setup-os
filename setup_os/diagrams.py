"""Standard diagram pack generation for Setup OS outputs."""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

from setup_os.spec import AgentSpec


DIAGRAM_MANIFEST = {
    "name": "setup_os_standard_diagram_pack",
    "version": "0.1.0",
    "purpose": "Standard architecture diagram outputs for every Setup OS-generated vertical OS.",
    "diagrams": [
        {
            "id": "overview_orchestration",
            "title": "Overview Orchestration",
            "purpose": "Give the user the big-picture mental model in one glance.",
            "outputs": ["overview_orchestration.d2", "overview_orchestration.html"],
        },
        {
            "id": "runtime_architecture",
            "title": "Runtime Architecture",
            "purpose": "Show what Setup OS wires together locally.",
            "outputs": ["runtime_architecture.d2", "runtime_architecture.html"],
        },
        {
            "id": "evolution_safety_flow",
            "title": "Evolution / Safety Flow",
            "purpose": "Show how the generated OS matures without unsafe self-mutation.",
            "outputs": ["evolution_safety_flow.d2", "evolution_safety_flow.html"],
        },
    ],
    "asset_requirements": {
        "local_icons": True,
        "no_remote_runtime_assets": True,
        "recommended_icon_folder": "docs/diagrams/icons",
    },
    "acceptance_criteria": [
        "All three diagrams are generated.",
        "Each HTML diagram opens locally with file://.",
        "Icons render without internet access.",
        "D2 source references local icon files.",
        "Overview has no more than five major visual groups.",
        "Runtime Architecture shows adapters and safety gates.",
        "Evolution / Safety Flow shows approval before strategy mutation.",
    ],
}


ICON_FILES = {
    "conversation.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 58 58"><polygon fill="#EDEADA" points="52,19 38,5 11,5 11,58 52,58"/><polygon fill="#C1BCA4" points="11,5 38,5 47,14 47,0 6,0 6,53 11,53"/><g fill="#CEC9AE"><path d="M19,26h25c.552,0,1-.447,1-1s-.448-1-1-1H19c-.552,0-1,.447-1,1s.448,1,1,1z"/><path d="M19,18h10c.552,0,1-.447,1-1s-.448-1-1-1H19c-.552,0-1,.447-1,1s.448,1,1,1z"/><path d="M44,32H19c-.552,0-1,.447-1,1s.448,1,1,1h25c.552,0,1-.447,1-1s-.448-1-1-1z"/><path d="M44,40H19c-.552,0-1,.447-1,1s.448,1,1,1h25c.552,0,1-.447,1-1s-.448-1-1-1z"/></g><polygon fill="#CEC9AE" points="38,5 38,19 52,19"/></svg>""",
    "evolution.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 58 58"><circle fill="#7383BF" cx="29" cy="29" r="8"/><g fill="#424A60"><path d="M29,0l4,10h-8z"/><path d="M29,58l-4-10h8z"/><path d="M0,29l10-4v8z"/><path d="M58,29l-10,4v-8z"/></g><path fill="#EDEADA" d="M29,14a15,15 0 1,0 0,30a15,15 0 1,0 0,-30zM29,20a9,9 0 1,1 0,18a9,9 0 1,1 0,-18z"/></svg>""",
    "memory.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 58 58"><ellipse fill="#7383BF" cx="29" cy="10" rx="24" ry="8"/><path fill="#556080" d="M5,10v34c0,4.4 10.7,8 24,8s24-3.6 24-8V10c0,4.4-10.7,8-24,8S5,14.4 5,10z"/><path fill="#EDEADA" d="M5,22c0,4.4 10.7,8 24,8s24-3.6 24-8v8c0,4.4-10.7,8-24,8S5,34.4 5,30z" opacity=".65"/></svg>""",
    "runtime.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path fill="#3776AB" d="M32,4c-10,0-14,4-14,10v8h18v4H12c-6,0-10,5-10,12s4,12 10,12h8v-8c0-6 5-10 11-10h18c6,0 11-5 11-11v-7C60,8 50,4 32,4z"/><circle fill="#fff" cx="24" cy="13" r="3"/><path fill="#FFD43B" d="M32,60c10,0 14-4 14-10v-8H28v-4h24c6,0 10-5 10-12s-4-12-10-12h-8v8c0,6-5,10-11,10H15C9,32 4,37 4,43v7c0,6 10,10 28,10z"/><circle fill="#fff" cx="40" cy="51" r="3"/></svg>""",
    "alerts.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60"><path fill="#EEAF4B" d="M16,51c11,2 17,2 28,0l9-2c-5-5-7-10-7-17v-9c0-12-9-17-16-17s-16,5-16,17v9c0,7-2,12-7,17z"/><path fill="#DC9628" d="M22,51c1.4,3.3 4.6,6 8,6s6.6-2.7 8-6c-6,.8-10,.8-16,0z"/></svg>""",
    "data.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 58 58"><rect fill="#14A085" x="8" y="10" width="42" height="34" rx="4"/><path fill="#424A60" d="M14,20h30v4H14zm0,8h30v4H14zm0,8h20v4H14z"/></svg>""",
    "tests.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60"><path fill="#7383BF" d="M30,2l23,9v17c0,14-9,25-23,30C16,53 7,42 7,28V11z"/><path fill="#fff" d="M26,39L15,28l4-4l7,7l15-16l4,4z"/></svg>""",
    "reports.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 58 58"><polygon fill="#EDEADA" points="52,19 38,5 11,5 11,58 52,58"/><polygon fill="#CEC9AE" points="38,5 38,19 52,19"/><g fill="#CEC9AE"><rect x="18" y="25" width="27" height="3"/><rect x="18" y="33" width="27" height="3"/><rect x="18" y="41" width="20" height="3"/></g></svg>""",
    "broker.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 150 150"><path fill="#3A556A" d="M8,140h134v5H3V8h5z"/><rect fill="#709584" x="28" y="91" width="20" height="50"/><rect fill="#21B3A9" x="58" y="68" width="20" height="73"/><rect fill="#FE7058" x="88" y="77" width="20" height="64"/><rect fill="#029BC5" x="118" y="40" width="20" height="101"/><path fill="#3A556A" d="M32,62l30-23l31,12l33-36l4,4l-36,39l-31-13l-28,21z"/></svg>""",
    "approval.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 58 58"><circle fill="#F0C419" cx="29" cy="18" r="12"/><path fill="#7383BF" d="M8,56c2-15 13-24 21-24s19,9 21,24z"/></svg>""",
    "plugins.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 58 58"><path fill="#EBBA16" d="M2,12h18l5,7h31v28c0,3-2,5-5,5H7c-3,0-5-2-5-5z"/><path fill="#EFCE4A" d="M2,22h54L47,52H2z"/></svg>""",
}


def write_standard_diagram_pack(spec: AgentSpec, output_dir: Path) -> Path:
    """Write the standard three-diagram pack for a generated vertical."""
    diagram_dir = output_dir / "docs" / "diagrams"
    icon_dir = diagram_dir / "icons"
    icon_dir.mkdir(parents=True, exist_ok=True)

    for filename, svg in ICON_FILES.items():
        _write(icon_dir / filename, svg)

    _write(diagram_dir / "diagram_manifest.json", json.dumps(DIAGRAM_MANIFEST, indent=2) + "\n")
    _write(diagram_dir / "overview_orchestration.d2", _overview_d2(spec))
    _write(diagram_dir / "runtime_architecture.d2", _runtime_d2(spec))
    _write(diagram_dir / "evolution_safety_flow.d2", _evolution_d2(spec))
    _write(diagram_dir / "overview_orchestration.html", _diagram_html(spec, "Overview Orchestration", "overview"))
    _write(diagram_dir / "runtime_architecture.html", _diagram_html(spec, "Runtime Architecture", "runtime"))
    _write(diagram_dir / "evolution_safety_flow.html", _diagram_html(spec, "Evolution / Safety Flow", "evolution"))
    return diagram_dir


def _overview_d2(spec: AgentSpec) -> str:
    return f"""vars: {{ d2-config: {{ sketch: true }} }}
direction: right
chat: "Conversations" {{ icon: ./icons/conversation.svg }}
evolution: "Evolution Layer\\npropose diffs, ask approval" {{ icon: ./icons/evolution.svg }}
memory: "Versioned Memory\\nstrategy + audit log" {{ icon: ./icons/memory.svg }}
core: "{spec.name} Core" {{ icon: ./icons/runtime.svg }}
outputs: "Reports / alerts / actions" {{ icon: ./icons/alerts.svg }}
plugins: "Plug-in adapters" {{ icon: ./icons/plugins.svg }}
chat -> evolution: "import" {{ style.animated: true }}
evolution -> memory: "approved update" {{ style.animated: true }}
memory -> core: "current strategy" {{ style.animated: true }}
plugins -> core: "swap capabilities" {{ style.animated: true }}
core -> outputs: "confidence-scored output" {{ style.animated: true }}
"""


def _runtime_d2(spec: AgentSpec) -> str:
    return f"""vars: {{ d2-config: {{ sketch: true }} }}
direction: right
memory: "Memory\\nlocal files + vector store" {{ icon: ./icons/memory.svg }}
data: "Data adapters\\nimports + APIs" {{ icon: ./icons/data.svg }}
tests: "Safety checks\\npolicy + limits" {{ icon: ./icons/tests.svg }}
core: "{spec.name} Runtime" {{ icon: ./icons/runtime.svg }}
reports: "Reports" {{ icon: ./icons/reports.svg }}
alerts: "Alerts" {{ icon: ./icons/alerts.svg }}
broker: "Broker adapter\\napproval-first" {{ icon: ./icons/broker.svg }}
memory -> core: "strategy context" {{ style.animated: true }}
data -> core: "signals" {{ style.animated: true }}
tests -> core: "guardrails" {{ style.animated: true }}
core -> reports: "daily state" {{ style.animated: true }}
core -> alerts: "recommendations" {{ style.animated: true }}
core -> broker: "approved only" {{ style.animated: true }}
"""


def _evolution_d2(spec: AgentSpec) -> str:
    return """vars: { d2-config: { sketch: true } }
direction: right
chat: "New conversation" { icon: ./icons/conversation.svg }
extract: "Extract facts + rules" { icon: ./icons/data.svg }
diff: "Strategy diff" { icon: ./icons/evolution.svg }
checks: "Safety gates" { icon: ./icons/tests.svg }
approval: "Human approval" { icon: ./icons/approval.svg }
release: "Versioned release" { icon: ./icons/memory.svg }
runtime: "Runtime uses it" { icon: ./icons/runtime.svg }
feedback: "Feedback loop" { icon: ./icons/alerts.svg }
chat -> extract: "parse" { style.animated: true }
extract -> diff: "propose" { style.animated: true }
diff -> checks: "validate" { style.animated: true }
checks -> approval: "review" { style.animated: true }
approval -> release: "approved only" { style.animated: true }
release -> runtime: "deploy locally" { style.animated: true }
runtime -> feedback: "observe" { style.animated: true }
feedback -> chat: "next chat" { style.animated: true }
"""


def _diagram_html(spec: AgentSpec, title: str, kind: str) -> str:
    cards = {
        "overview": [
            ("Conversations", "Chat exports and notes", "conversation.svg"),
            ("Evolution", "Propose diffs, ask approval", "evolution.svg"),
            ("Memory", "Strategy versions and audit log", "memory.svg"),
            ("Runtime", f"{spec.name} core", "runtime.svg"),
            ("Outputs", "Reports, alerts, actions", "alerts.svg"),
        ],
        "runtime": [
            ("Memory", "Local files and vector store", "memory.svg"),
            ("Data", "Imports and APIs", "data.svg"),
            ("Safety", "Policy, limits, backtests", "tests.svg"),
            ("Runtime", f"{spec.name} agents", "runtime.svg"),
            ("Outputs", "Reports, alerts, broker adapter", "broker.svg"),
        ],
        "evolution": [
            ("Import", "New conversation", "conversation.svg"),
            ("Extract", "Facts, goals, rules", "data.svg"),
            ("Diff", "Proposed strategy change", "evolution.svg"),
            ("Check", "Safety gates", "tests.svg"),
            ("Approve", "Human review before release", "approval.svg"),
        ],
    }[kind]
    card_markup = []
    for index, (heading, body, icon) in enumerate(cards):
        x = 40 + index * 220
        card_markup.append(
            f"""<g class="card"><rect x="{x}" y="180" width="180" height="150" rx="16"/><image x="{x + 22}" y="205" width="34" height="34" href="icons/{icon}"/><text class="heading" x="{x + 22}" y="272">{heading}</text><text class="body" x="{x + 22}" y="302">{body}</text></g>"""
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{spec.name} - {title}</title>
  <style>
    body {{ margin: 0; background: #fffaf0; color: #26211b; font-family: "Segoe Print", "Comic Sans MS", system-ui, sans-serif; }}
    main {{ width: min(1180px, 100vw); margin: 0 auto; padding: 32px; }}
    h1 {{ margin: 0 0 8px; font-size: 44px; line-height: 1; }}
    p {{ margin: 0 0 24px; font: 700 15px/1.4 "Trebuchet MS", system-ui, sans-serif; }}
    svg {{ width: 100%; height: auto; display: block; }}
    .card rect {{ fill: #dff1ff; stroke: #26211b; stroke-width: 3; filter: url(#shadow); }}
    .card:nth-of-type(2n) rect {{ fill: #e8f7df; }}
    .card:nth-of-type(3n) rect {{ fill: #ffe2dc; }}
    .heading {{ font: 800 20px "Segoe Print", system-ui, sans-serif; fill: #26211b; }}
    .body {{ font: 700 12px "Trebuchet MS", system-ui, sans-serif; fill: #332f28; }}
    .arrow {{ fill: none; stroke: #26211b; stroke-width: 3; marker-end: url(#arrow); stroke-dasharray: 8 10; animation: dash 8s linear infinite; }}
    @keyframes dash {{ to {{ stroke-dashoffset: -140; }} }}
  </style>
</head>
<body>
  <main>
    <h1>{title}</h1>
    <p>{spec.summary}</p>
    <svg viewBox="0 0 1140 420" role="img" aria-label="{title}">
      <defs><filter id="shadow"><feDropShadow dx="4" dy="5" stdDeviation="0.1" flood-opacity="0.16"/></filter><marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#26211b"/></marker></defs>
      {''.join(card_markup)}
      <path class="arrow" d="M220 255 C250 245 270 245 300 255"/><path class="arrow" d="M440 255 C470 245 490 245 520 255"/><path class="arrow" d="M660 255 C690 245 710 245 740 255"/><path class="arrow" d="M880 255 C910 245 930 245 960 255"/>
    </svg>
  </main>
</body>
</html>
"""


def _write(path: Path, content: str) -> None:
    path.write_text(dedent(content).lstrip(), encoding="utf-8")
