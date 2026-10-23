/**
 * 💭 KAVACH COMIC CLOUD EXPLAINER & ELI5 COMPREHENSION ENGINE
 * CSE3101: Agentic AI — Mid-Semester Project Evaluation
 * Faculty: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari
 * Team: Dhruv Jain (230532), Dev Garg (230487), Ansh Rohilla (230794), Ansh Adhikari (230822)
 *
 * Provides animated comic-book thought/speech bubbles with punchy 1-liners,
 * playful metaphors, and full technical dossiers (equations, files, test commands).
 */

(function () {
  'use strict';

  const COMIC_TOPICS = [
    {
      id: "shannon_entropy",
      badge: "💥 POW!",
      badgeColor: "#EF4444",
      topic: "Shannon Information Entropy (H ≥ 4.0)",
      oneLiner: "Like a noise-detector: normal code has a regular rhythm, but secret passwords look like chaotic gibberish that immediately rings the alarm!",
      metaphor: "Think of regular code like composed music and leaked secret keys like static noise on a broken radio.",
      math: "H(S) = -\\sum_{i=1}^{k} P(c_i) \\log_2 P(c_i)",
      details: "Calculates the entropy of character frequencies. Normal English source code exhibits H ≈ 1.5–3.2. High-entropy strings (e.g. AWS secret keys, base64 tokens) have H ≥ 4.0 and are instantly intercepted before the LLM is invoked.",
      codeFile: "backend/app/security/secret_detector.py",
      testCmd: "pytest tests/test_security_v2.py -k test_detects_high_entropy_password",
      rubric: "Criterion C7 (Technical Understanding — 5 Marks)"
    },
    {
      id: "verhoeff_d5",
      badge: "🛡️ SHIELD!",
      badgeColor: "#059669",
      topic: "Verhoeff Dihedral Group (D₅) Aadhaar Validation",
      oneLiner: "Like an ancient polygon puzzle where spinning a 10-sided pentagon catches mistyped Indian Aadhaar cards with 100% mathematical certainty!",
      metaphor: "A regular regex matches any random 12-digit number; Verhoeff uses abstract algebra to ensure only genuinely valid Indian citizen IDs are flagged.",
      math: "(\\sum_{i=0}^{n-1} d(\\text{perm}[i \\bmod 8], c_i)) = 0",
      details: "Computes non-commutative permutations over the dihedral symmetry group D₅. Catches 100% of single-digit substitution errors and adjacent transposition errors (ab ↔ ba), preventing false-positive blocks on non-Aadhaar integers.",
      codeFile: "backend/app/security/detector.py",
      testCmd: "pytest tests/test_security.py -k test_bare_aadhaar_detection",
      rubric: "Criterion C7 (Technical Understanding — 5 Marks)"
    },
    {
      id: "ast_blast_radius",
      badge: "⚡ ZAP!",
      badgeColor: "#F59E0B",
      topic: "AST Call Graph DAG & Transitive Blast Radius",
      oneLiner: "Like an X-ray of your entire house's electrical wiring: if you touch one wire, it highlights every room that might spark before an explosion happens!",
      metaphor: "Instead of guessing what will break, the compiler walks the call graph tree to calculate reachability across all downstream services.",
      math: "B(v) = \\frac{|\\text{Reach}(v)|}{|V| - 1}, \\quad \\text{where } \\text{Reach}(v) = \\{u \\in V \\mid v \\rightsquigarrow u\\}",
      details: "Uses Python's native `ast.parse` to construct a Directed Acyclic Graph (DAG) of symbol definitions, imports, and calls. If blast radius B(v) > 0.40, KAVACH halts and mandates Human-In-The-Loop approval.",
      codeFile: "backend/app/impact/analyzer.py",
      testCmd: "pytest tests/test_impact.py -k test_analyze_impact_scoring",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "adk_callbacks",
      badge: "🧠 BRAIN BLAST!",
      badgeColor: "#8B5CF6",
      topic: "Google ADK 8-Hook Callbacks (adk.dev/callbacks)",
      oneLiner: "8 invisible security guards posted at every door of the agent (before model, after tool, on error) so no AI agent can wander off or go rogue!",
      metaphor: "Like a flight checklist where the autopilot cannot take off, adjust flaps, or land without triggering signed telemetry checks.",
      math: "\\text{Phases: } \\{ \\text{Agent Lifecycle}, \\text{Model Call}, \\text{Tool Invocation} \\} \\times \\{ \\text{before}, \\text{after}, \\text{error} \\}",
      details: "Conforms 100% to Google ADK specification across 3 execution phases: `before_agent`, `after_agent`, `before_model`, `after_model`, `before_tool`, `after_tool`, `on_model_error`, and `on_tool_error`.",
      codeFile: "backend/app/adk/callbacks.py",
      testCmd: "pytest tests/test_adk_callbacks_and_triage.py -k test_adk_all_eight_hook_points",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "medical_triage",
      badge: "🚑 CODE RED!",
      badgeColor: "#EF4444",
      topic: "Canonical Medical Triage Multi-Agent Pipeline",
      oneLiner: "Instantly routes chest pain to Call 112/108 with strictly NO medicine, while giving simple Paracetamol for a reading headache—zero dangerous hallucinations!",
      metaphor: "A smart hospital emergency room nurse that triages critical trauma straight to the ambulance and directs mild aches to over-the-counter care.",
      math: "\\text{Triage Route: } \\begin{cases} \\text{Urgent} \\to \\text{emergency\\_agent} \\to \\text{Call 112/108 (NO MEDS)} \\\\ \\text{Normal} \\to \\text{persona\\_agent} \\to \\text{medicine\\_agent} \\to \\text{Paracetamol 500mg} \\end{cases}",
      details: "Two-branch deterministic triage: High urgency executes `only_if_urgent` guardrails issuing zero drug recommendations. Normal symptomatic relief coordinates persona and medicine agents to query Tavily/local database for safe relief.",
      codeFile: "backend/app/adk/medical_triage.py",
      testCmd: "pytest tests/test_adk_callbacks_and_triage.py -k test_medical_triage_high_urgency_cardiac_emergency",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "crewai_flows",
      badge: "🎬 ACTION!",
      badgeColor: "#3B82F6",
      topic: "CrewAI Stateful Flows (@start, @listen, @router)",
      oneLiner: "Like a Hollywood movie crew where the Director kicks off with @start, the Camera and Sound crews listen with @listen, and nobody shoots out of turn!",
      metaphor: "Stateful reactive flow engineering preventing chaotic multi-agent race conditions by enforcing structured DAG dependencies.",
      math: "\\text{Flow: } @\\text{start} \\to \\text{Ingest} \\xrightarrow{@\\text{listen}} \\text{Security Audit} \\xrightarrow{@\\text{router}} \\text{Safe vs Blocked}",
      details: "Implements CrewAI Flows architecture with structured `@start` initializers, `@listen` reactive listeners, and conditional `@router` branches passing state dictionaries through immutable audit logs.",
      codeFile: "backend/app/crew/flows.py",
      testCmd: "pytest tests/test_syllabus_advanced_modules.py -k test_crewai_flows_stateful_automation",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "qdrant_rag",
      badge: "📚 SUPER MEMORY!",
      badgeColor: "#059669",
      topic: "Agentic RAG & Qdrant 384-d Vector Store",
      oneLiner: "Converts your entire code into 384-dimensional GPS coordinates so the agent teleports directly to the exact function in milliseconds!",
      metaphor: "Instead of flipping through a 10,000-page book page-by-page, it has a semantic index that points straight to the paragraph you need.",
      math: "\\text{Similarity: } \\cos(\\theta) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\| \\|\\mathbf{v}\\|}, \\quad \\mathbf{u}, \\mathbf{v} \\in \\mathbb{R}^{384}",
      details: "Extracts classes and functions using AST chunking. Embeds code snippets into 384-dimensional vectors using `all-MiniLM-L6-v2` and indexes them into Qdrant vector database for k=5 nearest-neighbor context retrieval.",
      codeFile: "backend/app/rag/embed_store.py",
      testCmd: "pytest tests/test_rag.py -k test_search_basic",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "package_firewall",
      badge: "🦹 BUSTED!",
      badgeColor: "#DC2626",
      topic: "PyPI Slopsquatting & Package Hallucination Firewall",
      oneLiner: "Catches fake package names invented by AI before hackers can publish malicious Trojan code on PyPI to hijack your laptop!",
      metaphor: "A passport checkpoint for software libraries: if the library isn't registered on the official PyPI database, it gets denied entry instantly.",
      math: "\\text{Levenshtein: } d_{a,b}(i,j) = \\min \\{ \\text{del}, \\text{ins}, \\text{sub}, \\text{trans} \\}",
      details: "Scans all generated AST `import` statements against Python Standard Library and live PyPI registry LRU cache. Uses Damerau-Levenshtein distance to detect typosquatting attacks (e.g., `reqeusts` vs `requests`).",
      codeFile: "backend/app/security/package_firewall.py",
      testCmd: "pytest tests/test_advanced_features.py -k test_hallucinated_package_blocked",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "mcp_protocol",
      badge: "🔌 USB-C FOR AI!",
      badgeColor: "#7C3AED",
      topic: "Anthropic Model Context Protocol (MCP) JSON-RPC 2.0",
      oneLiner: "A universal USB-C plug that lets Cursor, Claude, or any external IDE instantly plug into our security scanner, RAG, and blast-radius tools!",
      metaphor: "Just like USB-C replaced 10 different charger cables, MCP standardizes how AI agents talk to external tools.",
      math: "\\text{JSON-RPC 2.0: } \\{ \\text{\"jsonrpc\"}: \\text{\"2.0\"}, \\text{\"method\"}: \\text{\"tools/call\"}, \\text{\"params\"}: \\{...\\} \\}",
      details: "Exposes 4 standardized security and retrieval tools (`kavach_scan_security`, `kavach_query_rag`, `kavach_analyze_impact`, `kavach_verify_package`) over standard input/output and HTTP SSE for external IDE integration.",
      codeFile: "backend/app/mcp/server.py",
      testCmd: "pytest tests/test_advanced_features.py -k test_mcp_tool_call_scan_security",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "a2a_protocol",
      badge: "🤝 TRUST COUNCIL!",
      badgeColor: "#2563EB",
      topic: "Google Agent-to-Agent (A2A) Signed Envelopes & Consensus",
      oneLiner: "Agents don't blindly trust each other—they digitally sign their messages with SHA-256 and vote with 2/3 majority before high-risk changes!",
      metaphor: "A multi-signature bank vault where 3 trusted officers must turn their keys simultaneously before the safe door unlocks.",
      math: "\\text{Consensus: } \\frac{\\sum_{i=1}^{M} \\mathbb{I}(\\text{vote}_i = \\text{ALLOW})}{M} \\ge \\frac{2}{3}",
      details: "Implements Google A2A protocol with P2P peer discovery, HMAC-SHA256 message signing, payload tamper protection, and Byzantine consensus across Sentinel, Coder, and Auditor agents.",
      codeFile: "backend/app/a2a/protocol.py",
      testCmd: "pytest tests/test_syllabus_advanced_modules.py -k test_a2a_multi_agent_consensus",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "airgap_privacy",
      badge: "🔐 FORT KNOX!",
      badgeColor: "#059669",
      topic: "Air-Gapped Privacy Switch & Local Ollama Routing",
      oneLiner: "Flips an invisible airlock switch that keeps your top-secret code locked inside your computer with local Ollama, never touching the internet!",
      metaphor: "Like taking your sensitive bank paperwork into a soundproof, disconnected room where no microphones or internet cables exist.",
      math: "\\text{Network Egress: } \\Delta_{\\text{CloudBytes}} = 0 \\quad \\text{when Air-Gap = Active}",
      details: "Enforces Indian DPDP Act 2023 compliance. Automatically reroutes requests containing sensitive intellectual property or credentials to local Ollama (`qwen2.5-coder:7b`) with zero cloud egress.",
      codeFile: "backend/app/generation/llm_client.py",
      testCmd: "pytest tests/test_syllabus_advanced_modules.py -k test_privacy_routing_toggle",
      rubric: "Criterion C7 (Technical Understanding — 5 Marks)"
    },
    {
      id: "reasoning_paradigms",
      badge: "💡 THINK TANK!",
      badgeColor: "#F59E0B",
      topic: "Cognitive Reasoning Paradigms (ReAct, CoT, ToT, COTS)",
      oneLiner: "Instead of shooting from the hip, the agent thinks step-by-step (CoT), explores tree branches (ToT), and acts with reflection loops (ReAct)!",
      metaphor: "Playing chess by thinking 4 moves ahead across multiple branches instead of making the first impulsive move you see.",
      math: "\\text{Tree-of-Thought: } \\text{argmax}_{p \\in \\text{Paths}} \\sum_{s \\in p} \\text{HeuristicScore}(s)",
      details: "Features a side-by-side comparative benchmarking engine across Chain-of-Thought (linear deduction), Tree-of-Thought (heuristic branch exploration), ReAct (Thought-Action-Observation), and Self-Consistency (majority voting).",
      codeFile: "backend/app/agent/reasoning_strategies.py",
      testCmd: "pytest tests/test_syllabus_advanced_modules.py -k test_reasoning_comparison_benchmark",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "self_healing_sandbox",
      badge: "🩹 IMMORTAL AGENT!",
      badgeColor: "#10B981",
      topic: "Ephemeral Self-Healing Pytest Sandbox",
      oneLiner: "If newly synthesized code fails a unit test, the agent catches the traceback, figures out what broke, patches itself, and tries again (max 3 times)!",
      metaphor: "A student taking a practice test who immediately reviews the answer key on mistakes, learns the correct rule, and retakes until achieving 100%.",
      math: "\\text{Bounded Reflexion Loop: } N \\le 3 \\quad \\text{with invariant state preservation}",
      details: "Spawns an isolated Python subprocess sandbox running targeted pytest test assertions. Parses stderr tracebacks and loops back into the coder agent with targeted error hints up to 3 bounded iterations.",
      codeFile: "backend/app/agent/self_healer.py",
      testCmd: "pytest tests/test_advanced_features.py -k test_autonomous_self_healer",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "fsm_orchestrator",
      badge: "🎮 MASTER CONTROLLER!",
      badgeColor: "#3B82F6",
      topic: "Deterministic 8-Stage Finite State Machine (FSM)",
      oneLiner: "Prevents AI chaos by locking the agent into 8 strict stages—it cannot generate code until it finishes planning, RAG, impact analysis, and safety checks!",
      metaphor: "A secure airlock chamber where Door 2 physically cannot unlock until Door 1 is completely closed and sterilized.",
      math: "\\text{FSM: } S_0 \\to S_1 \\to S_2 \\to S_3 \\to S_4 \\to S_5 \\to S_6 \\to S_7 \\quad (S_i \\in \\text{Stages})",
      details: "Strict deterministic workflow orchestration traversing `REQUEST_RECEIVED` → `PLANNING` → `CONTEXT_RETRIEVAL` → `IMPACT_ANALYSIS` → `SECURITY_EVALUATION` → `GENERATION` → `VALIDATION` → `COMPLETE` / `BLOCKED`.",
      codeFile: "backend/app/agent/orchestrator.py",
      testCmd: "pytest tests/test_agent.py -k test_workflow_end_to_end",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "vision_auditor",
      badge: "👁️ CYBER VISION!",
      badgeColor: "#9333EA",
      topic: "Multimodal Vision Architecture Security Auditor",
      oneLiner: "Looks at network architecture diagrams with computer vision to flag unencrypted port 80 or public databases before you deploy!",
      metaphor: "A structural building inspector who reviews architectural blueprints to find missing fire exits and weak load-bearing walls.",
      math: "\\text{Vision Classifier: } f(\\text{DiagramImage}) \\to \\{ \\text{Threats}, \\text{Port Vulnerabilities}, \\text{Verdict} \\}",
      details: "Audits system architecture and network topology diagrams. Flags insecure unencrypted HTTP ingress, exposed ports, and direct public database bindings.",
      codeFile: "backend/app/security/multimodal_vision.py",
      testCmd: "pytest tests/test_syllabus_advanced_modules.py -k test_multimodal_vision_auditor_threat_detection",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "hitl_quarantine",
      badge: "🚨 HALT & CATCH FIRE!",
      badgeColor: "#DC2626",
      topic: "Human-in-the-Loop (HITL) Dynamic Quarantine Gate",
      oneLiner: "If an agent wants to delete database tables or change >40% of the codebase, it is frozen in mid-air until a living human engineer signs off!",
      metaphor: "The red nuclear launch button requiring two physical keys turned by two human officers before any irreversible payload fires.",
      math: "\\text{Verdict} = \\begin{cases} \\text{EXECUTE} & \\text{if } B(v) \\le 0.40 \\land \\text{Risk} = \\text{LOW} \\\\ \\text{QUARANTINE} & \\text{if } B(v) > 0.40 \\lor \\text{Destructive Op} \\end{cases}",
      details: "Intercepts high-risk AST modifications (SQL DROP TABLE, rm -rf, os.system) and transitive blast radius B(v) > 0.40 into an interactive HITL approval inbox before code application.",
      codeFile: "backend/app/agent/hitl_quarantine.py",
      testCmd: "pytest tests/test_syllabus_advanced_modules.py -k test_human_in_the_loop",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "merkle_audit",
      badge: "⛓️ UNBREAKABLE CHAIN!",
      badgeColor: "#0284C7",
      topic: "Cryptographic Merkle Tree Audit Trail",
      oneLiner: "Hashes every single agent thought, prompt, and tool invocation into a cryptographic blockchain tree—if anyone tampers with a single character, the root hash shatters!",
      metaphor: "Like stamping a wax royal seal on every page of a legal contract; any eraser smudge instantly reveals tampering.",
      math: "H_{\\text{root}} = H(H_{\\text{left}} \\parallel H_{\\text{right}}), \\quad H(x) = \\text{SHA-256}(x)",
      details: "Builds a balanced binary Merkle hash tree over all intermediate agent transitions. Provides O(log N) inclusion proofs for tamper-evident compliance during audit inspections.",
      codeFile: "backend/app/audit/merkle_tree.py",
      testCmd: "pytest tests/test_syllabus_advanced_modules.py -k test_merkle_provenance",
      rubric: "Criterion C7 (Technical Understanding — 5 Marks)"
    },
    {
      id: "cyclonedx_sbom",
      badge: "📜 NUTRITION LABEL!",
      badgeColor: "#4F46E5",
      topic: "CycloneDX SBOM & SLSA Level 3 Attestation",
      oneLiner: "Generates a certified software ingredient list showing every library, author, license, and cryptographic hash—zero mystery blackbox code!",
      metaphor: "The FDA food nutrition label on cereal boxes: shows exact calories, ingredients, and allergen warnings before you take a bite.",
      math: "\\text{SBOM} = \\{ \\text{UUID}, \\text{Metadata}, \\text{Components } c_i = (\\text{name}, \\text{version}, \\text{hash}, \\text{license}) \\}",
      details: "Produces CycloneDX v1.5 standard JSON/XML Software Bill of Materials (SBOM) and signed SLSA Level 3 build provenance records for all synthesized software artifacts.",
      codeFile: "backend/app/security/sbom.py",
      testCmd: "pytest tests/test_syllabus_advanced_modules.py -k test_cyclonedx_sbom",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "react_reflexion",
      badge: "🔄 SECOND CHANCE!",
      badgeColor: "#D97706",
      topic: "ReAct Reflexion & Closed-Loop Episodic Memory",
      oneLiner: "The agent writes in its diary: 'I tried X, it returned an error, so I deduced Y and will now try Z'—learning dynamically instead of repeating the same mistake!",
      metaphor: "A gamer who loses a life on Level 3, remembers where the spike trap was, and jumps over it on the second try.",
      math: "\\tau_t = (s_t, a_t, o_t, r_t) \\implies M_{t+1} = M_t \\cup \\{ \\text{Reflexion}(\\tau_t) \\}",
      details: "Implements Yao et al. & Shinn et al. Reflexion memory buffers where verbal error self-reflections are prepended into episodic agent state to guide subsequent retry cycles.",
      codeFile: "backend/app/agent/reflexion.py",
      testCmd: "pytest tests/test_syllabus_advanced_modules.py -k test_closed_loop_react",
      rubric: "Criterion C8 (Requirements Met — 10 Marks)"
    },
    {
      id: "dpdp_vault",
      badge: "🛡️ SHREDDER!",
      badgeColor: "#059669",
      topic: "DPDP Act 2023 Zero-Knowledge Privacy Vault",
      oneLiner: "Instantly masks Indian Aadhaar, PAN, phone numbers, and emails with random synthetic tokens before any LLM sees them, and unmasks them only upon return!",
      metaphor: "A coat-check desk at a luxury event: you give your real coat, you get a plastic claim ticket #42, and nobody inside knows what your real coat looks like.",
      math: "\\text{Tokenize: } x \\mapsto t_x \\in \\mathcal{T}, \\quad \\text{Vault}(t_x) = x \\quad (\\text{Egress}_{\\text{PII}} = \\emptyset)",
      details: "Complies with India's Digital Personal Data Protection Act 2023. Intercepts sensitive citizen data, creates in-memory nonces, and sends only pseudonymized representations to LLMs.",
      codeFile: "backend/app/security/privacy_vault.py",
      testCmd: "pytest tests/test_syllabus_advanced_modules.py -k test_dpdp_privacy_vault",
      rubric: "Criterion C7 (Technical Understanding — 5 Marks)"
    }
  ];

  // Helper to render comic cloud HTML
  function renderComicCloudCard(topic, isExpanded) {
    return `
      <div class="comic-cloud-card ${isExpanded ? 'drawer-open' : ''}" id="comic-card-${topic.id}" data-id="${topic.id}">
        <!-- Floating Animated Comic Cloud -->
        <div class="comic-thought-bubble">
          <div class="comic-cloud-header">
            <span class="comic-action-badge" style="background:${topic.badgeColor};">${topic.badge}</span>
            <span class="comic-topic-title">${topic.topic}</span>
          </div>

          <!-- Comic Speech One-Liner -->
          <div class="comic-speech-text">
            &ldquo;${topic.oneLiner}&rdquo;
          </div>

          <!-- Metaphor Bar -->
          <div class="comic-metaphor-bar">
            💡 <strong>ELI5 Metaphor:</strong> ${topic.metaphor}
          </div>

          <!-- Bottom Action Buttons inside the cloud -->
          <div class="comic-cloud-footer">
            <button type="button" class="comic-btn-toggle" onclick="window.toggleComicDetails('${topic.id}')">
              ${isExpanded ? '▲ Hide Technical Dossier' : '▼ Inspect Full Technical Dossier & Formula'}
            </button>
            <span class="comic-rubric-tag">${topic.rubric}</span>
          </div>
        </div>

        <!-- Hidden/Expandable Full Information Drawer -->
        <div class="comic-details-drawer ${isExpanded ? 'open' : ''}" id="comic-details-${topic.id}">
          <div class="comic-details-content">
            <div class="comic-detail-row">
              <span class="comic-detail-label">📐 Mathematical Formulation:</span>
              <code class="comic-math-code">${topic.math}</code>
            </div>
            <div class="comic-detail-row">
              <span class="comic-detail-label">⚙️ Detailed Engineering Mechanics:</span>
              <p class="comic-detail-p">${topic.details}</p>
            </div>
            <div class="comic-detail-row" style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;">
              <div>
                <span class="comic-detail-label">📂 Codebase Implementation:</span>
                <code class="comic-file-path">${topic.codeFile}</code>
              </div>
              <div>
                <span class="comic-detail-label">🧪 Pytest Verification:</span>
                <code class="comic-cmd-code">${topic.testCmd}</code>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  // Global toggle function
  window.toggleComicDetails = function (id) {
    const drawer = document.getElementById(`comic-details-${id}`);
    const card = document.getElementById(`comic-card-${id}`);
    if (!drawer || !card) return;
    const isOpen = drawer.classList.contains("open");
    drawer.classList.toggle("open", !isOpen);
    card.classList.toggle("drawer-open", !isOpen);
    const btn = card.querySelector(".comic-btn-toggle");
    if (btn) {
      btn.innerHTML = !isOpen ? '▲ Hide Technical Dossier' : '▼ Inspect Full Technical Dossier & Formula';
    }
  };

  // Toggle transparency peek mode so background page is 100% visible
  window.toggleComicModalTransparency = function () {
    const modal = document.getElementById("comic-explainer-modal");
    const btn = document.getElementById("comic-peek-btn");
    if (!modal) return;
    const isPeek = modal.classList.toggle("peek-mode");
    if (btn) {
      btn.innerHTML = isPeek ? '👓 Normal View' : '👓 Peek Behind';
      btn.style.background = isPeek ? '#10B981' : '#FFFFFF';
      btn.style.color = isPeek ? '#FFFFFF' : '#0F172A';
    }
  };

  // Open Full Comic Explainer Modal
  window.openComicExplainerModal = function (filterId) {
    let modal = document.getElementById("comic-explainer-modal");
    if (!modal) {
      modal = document.createElement("div");
      modal.id = "comic-explainer-modal";
      modal.className = "comic-modal-backdrop";
      document.body.appendChild(modal);
    }

    const topicsToRender = filterId ? COMIC_TOPICS.filter(t => t.id === filterId) : COMIC_TOPICS;

    modal.innerHTML = `
      <div class="comic-modal-window">
        <!-- Sticky Header with Comic Title -->
        <div class="comic-modal-header">
          <div style="display:flex; align-items:center; gap:12px;">
            <div class="comic-header-icon">💭</div>
            <div>
              <div style="display:flex; align-items:center; gap:8px;">
                <h2 class="comic-modal-h2">KAVACH Comic-Book Chronicles &middot; ELI5 Explainer Clouds</h2>
                <span class="comic-count-badge">${topicsToRender.length} TOPICS COVERED</span>
              </div>
              <p class="comic-modal-sub">
                CSE3101: Agentic AI &middot; Fun 1-liner animated comic clouds for every topic, backed by 100% rigorous mathematics &amp; code dossiers!
              </p>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <button type="button" class="comic-btn-expand-all" id="comic-peek-btn" onclick="window.toggleComicModalTransparency()" title="Peek at dashboard behind modal">👓 Peek Behind</button>
            <button type="button" class="comic-btn-expand-all" onclick="window.toggleAllComicDetails(true)">Expand All Dossiers</button>
            <button type="button" class="comic-btn-expand-all" onclick="window.toggleAllComicDetails(false)">Collapse All</button>
            <button type="button" class="comic-modal-close" onclick="window.closeComicExplainerModal()" title="Close">&times;</button>
          </div>
        </div>

        <!-- Filter Bar -->
        <div class="comic-modal-filterbar">
          <button type="button" class="comic-filter-chip active" onclick="window.filterComicTopics('all')">All 20 Topics</button>
          <button type="button" class="comic-filter-chip" onclick="window.filterComicTopics('security')">🛡️ Security &amp; Sentinel</button>
          <button type="button" class="comic-filter-chip" onclick="window.filterComicTopics('adk')">🧠 Google ADK &amp; Triage</button>
          <button type="button" class="comic-filter-chip" onclick="window.filterComicTopics('rag')">📚 RAG &amp; AST Blast Radius</button>
          <button type="button" class="comic-filter-chip" onclick="window.filterComicTopics('protocols')">🔌 MCP &amp; A2A Protocols</button>
          <button type="button" class="comic-filter-chip" onclick="window.filterComicTopics('orchestration')">🎬 FSM &amp; CrewAI Flows</button>
        </div>

        <!-- Scrollable Cards Grid -->
        <div class="comic-modal-body" id="comic-cards-container">
          ${topicsToRender.map(t => renderComicCloudCard(t, false)).join("")}
        </div>
      </div>
    `;

    modal.onclick = function (e) {
      if (e.target === modal) window.closeComicExplainerModal();
    };

    modal.classList.remove("peek-mode");
    modal.classList.add("open");
    modal.style.display = "flex";
  };

  window.closeComicExplainerModal = function () {
    const modal = document.getElementById("comic-explainer-modal");
    if (modal) {
      modal.classList.remove("open", "peek-mode");
      modal.style.display = "none";
    }
  };

  window.toggleAllComicDetails = function (expand) {
    document.querySelectorAll(".comic-details-drawer").forEach(drawer => {
      drawer.classList.toggle("open", expand);
    });
    document.querySelectorAll(".comic-cloud-card").forEach(card => {
      card.classList.toggle("drawer-open", expand);
    });
    document.querySelectorAll(".comic-btn-toggle").forEach(btn => {
      btn.innerHTML = expand ? '▲ Hide Technical Dossier' : '▼ Inspect Full Technical Dossier & Formula';
    });
  };

  window.filterComicTopics = function (category) {
    document.querySelectorAll(".comic-filter-chip").forEach(chip => {
      chip.classList.remove("active");
      if (chip.getAttribute("onclick") && chip.getAttribute("onclick").includes(`'${category}'`)) {
        chip.classList.add("active");
      }
    });

    let filtered = COMIC_TOPICS;
    if (category === 'security') {
      filtered = COMIC_TOPICS.filter(t => ['shannon_entropy', 'verhoeff_d5', 'package_firewall', 'airgap_privacy', 'dpdp_vault', 'hitl_quarantine', 'merkle_audit', 'cyclonedx_sbom'].includes(t.id));
    } else if (category === 'adk') {
      filtered = COMIC_TOPICS.filter(t => ['adk_callbacks', 'medical_triage'].includes(t.id));
    } else if (category === 'rag') {
      filtered = COMIC_TOPICS.filter(t => ['qdrant_rag', 'ast_blast_radius'].includes(t.id));
    } else if (category === 'protocols') {
      filtered = COMIC_TOPICS.filter(t => ['mcp_protocol', 'a2a_protocol'].includes(t.id));
    } else if (category === 'orchestration') {
      filtered = COMIC_TOPICS.filter(t => ['fsm_orchestrator', 'crewai_flows', 'reasoning_paradigms', 'self_healing_sandbox', 'vision_auditor', 'react_reflexion'].includes(t.id));
    }

    const container = document.getElementById("comic-cards-container");
    if (container) {
      container.innerHTML = filtered.map(t => renderComicCloudCard(t, false)).join("");
    }
    const inpage = document.getElementById("comic-inpage-container");
    if (inpage) {
      inpage.innerHTML = filtered.map(t => renderComicCloudCard(t, false)).join("");
    }
    const cockpitContainer = document.getElementById("comic-cockpit-cards-container");
    if (cockpitContainer) {
      cockpitContainer.innerHTML = filtered.map(t => renderComicCloudCard(t, false)).join("");
    }
  };

  // Popover tooltip engine for hover/click on specific topics
  window.showComicPopover = function (event, topicId) {
    const topic = COMIC_TOPICS.find(t => t.id === topicId);
    if (!topic) return;

    let popover = document.getElementById("comic-floating-popover");
    if (!popover) {
      popover = document.createElement("div");
      popover.id = "comic-floating-popover";
      popover.className = "comic-floating-popover";
      document.body.appendChild(popover);
    }

    popover.innerHTML = `
      <div class="comic-popover-cloud">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <span class="comic-action-badge" style="background:${topic.badgeColor}; font-size:0.68rem; padding:2px 7px;">${topic.badge}</span>
          <button type="button" onclick="window.hideComicPopover()" style="background:none; border:none; color:#0F172A; font-weight:800; cursor:pointer; font-size:1.1rem; line-height:1;">&times;</button>
        </div>
        <div style="font-weight:800; font-size:0.86rem; color:#0F172A; margin-bottom:6px;">${topic.topic}</div>
        <div style="font-size:0.82rem; line-height:1.4; color:#1E293B; background:#FEF9C3; border:1px dashed #CA8A04; border-radius:8px; padding:8px 10px; margin-bottom:8px;">
          &ldquo;${topic.oneLiner}&rdquo;
        </div>
        <div style="font-size:0.75rem; color:#475569; margin-bottom:8px;">
          💡 <strong>Metaphor:</strong> ${topic.metaphor}
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <code style="font-size:0.7rem; color:#7C3AED; background:#FAF5FF; padding:2px 6px; border-radius:4px;">${topic.math}</code>
          <button type="button" onclick="window.openComicExplainerModal('${topic.id}')" style="background:#0F172A; color:#FEF08A; border:none; padding:4px 10px; border-radius:6px; font-size:0.72rem; font-weight:700; cursor:pointer;">
            Full Dossier &rarr;
          </button>
        </div>
      </div>
    `;

    const rect = event.currentTarget.getBoundingClientRect();
    const x = Math.min(window.innerWidth - 340, Math.max(16, rect.left));
    const y = rect.bottom + 10;

    popover.style.left = `${x}px`;
    popover.style.top = `${y}px`;
    popover.classList.add("visible");
  };

  window.hideComicPopover = function () {
    const popover = document.getElementById("comic-floating-popover");
    if (popover) {
      popover.classList.remove("visible");
    }
  };

  // Mount Floating Comic Trigger Button in Corner & Init Inpage Container
  function initComicComponents() {
    // 1. Floating trigger button
    if (!document.getElementById("comic-floating-trigger")) {
      const btn = document.createElement("button");
      btn.id = "comic-floating-trigger";
      btn.className = "comic-floating-trigger";
      btn.type = "button";
      btn.innerHTML = `
        <span class="comic-trigger-tail"></span>
        <span class="comic-trigger-icon">💭</span>
        <span class="comic-trigger-text">Comic Clouds (ELI5)</span>
      `;
      btn.onclick = () => window.openComicExplainerModal();
      btn.title = "Click to open KAVACH Animated Comic Cloud Explainers (ELI5 for Every Topic!)";
      document.body.appendChild(btn);
    }

    // 2. Render In-Page Showcase if container is present
    const inpage = document.getElementById("comic-inpage-container");
    if (inpage && inpage.children.length === 0) {
      inpage.innerHTML = COMIC_TOPICS.map(t => renderComicCloudCard(t, false)).join("");
    }
  }

  // Initialize once DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initComicComponents);
  } else {
    initComicComponents();
  }

  // Expose dataset globally
  window.KAVACH_COMIC_TOPICS = COMIC_TOPICS;
  window.renderComicCloudCard = renderComicCloudCard;

})();

