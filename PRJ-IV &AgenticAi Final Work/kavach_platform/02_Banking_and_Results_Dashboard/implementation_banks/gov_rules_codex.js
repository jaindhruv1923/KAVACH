/**
 * Bharat Core Bank × KAVACH Platform
 * Official Government Rules & Statutory Regulatory Codex
 * Enforces Sovereign Directives of India: RBI, DPDP Act 2023, CERT-In, IT Act, MeitY, SEBI & Basel III
 * Enterprise Compliance Edition
 */

const GOV_RULES_DATA = [
  {
    id: "rbi_cyber_framework",
    category: "rbi",
    issueNum: "DIRECTIVE 01",
    soundBurst: "MANDATORY",
    burstColor: "#2563EB",
    title: "RBI Master Direction on Cyber Security Framework in Banks",
    officialRef: "RBI/2015-16/418 & Master Direction on IT Governance, Risk & Controls (Nov 2023)",
    gazette: "Section 35A Banking Regulation Act 1949 & RBI Cyber Security Guidelines",
    mandateComic: "No autonomous computer, AI agent, or single human operator can move banking reserves without authorized dual sets of credentials. Continuous boundary defense and 24x7 SOC event telemetry are strictly mandated.",
    legalText: "Mandates strict Four-Eyes Dual Control (Maker-Checker) for all privileged, administrative, and core banking transactions. Prohibits self-approval of financial batches. Requires continuous micro-segmentation, Privileged Access Management (PAM), and automated anomaly lockout.",
    penaltyBomb: "Cancellation of banking license, Section 47A statutory fine up to INR 50,00,000 per violation, and immediate regulatory embargo on digital onboarding of new customers.",
    kavachDefense: "Four-Eyes Dual Control console in Bharat Bank and KAVACH HITL Quarantine desk enforcing immutable Maker-Checker separation. Cryptographically prevents self-approval with HTTP 403 Forbidden.",
    liveActionLabel: "Launch 4-Eyes Dual Control Desk",
    liveActionId: "hitl"
  },
  {
    id: "rbi_payment_controls",
    category: "rbi",
    issueNum: "DIRECTIVE 02",
    soundBurst: "STATUTORY",
    burstColor: "#0284C7",
    title: "RBI Master Direction – Digital Payment Security Controls",
    officialRef: "DPSS.CO.OD.No.1934/06.08.005/2020-21 & 2024 Updates",
    gazette: "Section 18 read with Section 10(2) of Payment & Settlement Systems Act, 2007 (Act 51)",
    mandateComic: "High-value payments above INR 50,000 or anomalous AI payment memos are intercepted into a secure time-locked quarantine vault until authenticated supervisor clearance is confirmed.",
    legalText: "Mandates real-time velocity profiling, automated fraud risk scoring, step-up multi-factor verification, and Quarantined Escrow for transfers exceeding high-value thresholds (>INR 50,000) or displaying anomalous intent. Requires automated SAR filing with FIU-IND.",
    penaltyBomb: "Revocation of Payment System Operator (PSO) authorization, mandatory external forensic audit by RBI-empaneled CERT-In auditors, and personal civil liability for Chief Risk Officers.",
    kavachDefense: "Automated Quarantined Escrow pipeline holding all transfers > INR 50,000 for biometric supervisor clearance; continuous FIU-IND Suspicious Activity Reporting (SAR) radar with automated vector telemetry.",
    liveActionLabel: "Test INR 75,000 Quarantined Escrow",
    liveActionId: "escrow"
  },
  {
    id: "dpdp_act_2023",
    category: "dpdp",
    issueNum: "DIRECTIVE 03",
    soundBurst: "ZERO-KNOWLEDGE",
    burstColor: "#7C3AED",
    title: "Digital Personal Data Protection Act (DPDP Act) 2023",
    officialRef: "Act No. 22 of 2023 • Ministry of Law & Justice, Govt. of India",
    gazette: "Gazette of India Extraordinary, Part II, Section 1 • Sections 4, 6, 8, 9 & 33",
    mandateComic: "Customer Aadhaar, PAN, and account numbers must never be exposed to external AI models or prompt contexts. All Personally Identifiable Information (PII) must be masked with Zero-Knowledge cryptographic tokens.",
    legalText: "Prohibits Data Fiduciaries from processing personal data without lawful consent or legitimate uses. Mandates state-of-the-art technical safeguards to prevent leaks of customer Aadhaar (12-digit UIDAI), PAN, and financial identifiers to third-party LLMs and agents.",
    penaltyBomb: "Statutory penalties up to INR 250 Crore (INR 2,500,000,000 / USD ~30 Million) under Section 33(1) for failing to implement reasonable security safeguards preventing personal data breach.",
    kavachDefense: "DPDP Zero-Knowledge Token Vault in KAVACH security pipeline and Bharat Bank. Automatically tokenizes Aadhaar (e.g. AADHAAR_ZK_9821_VAULT) and PAN into immutable tokens before prompts or MCP tool arguments reach LLM contexts.",
    liveActionLabel: "Test DPDP Zero-Knowledge Tokenizer",
    liveActionId: "dpdp"
  },
  {
    id: "cert_in_directions",
    category: "cert-in",
    issueNum: "DIRECTIVE 04",
    soundBurst: "6-HR MANDATE",
    burstColor: "#EA580C",
    title: "CERT-In Cyber Security Directions (6-Hour Incident Mandate)",
    officialRef: "Directions No. 20(3)/2022-CERT-In under Section 70B(6) IT Act 2000",
    gazette: "Ministry of Electronics & Information Technology (MeitY) • 28 April 2022",
    mandateComic: "When an AI injection attack or security breach occurs, statutory notification to CERT-In is mandatory within 6 hours. System audit logs must be cryptographically archived for 180 days with NTP synchronization.",
    legalText: "Mandatory reporting of cyber security incidents (unauthorized access, malicious prompt injections, ransomware, or critical ledger anomalies) to CERT-In within 6 HOURS of discovery. Mandatory maintenance of system audit logs for 180 DAYS within Indian jurisdiction with NTP sync to NPL.",
    penaltyBomb: "Section 70B(7) IT Act: Imprisonment for up to 1 year or statutory fine up to INR 1,00,000, plus executive officer and CISO criminal liability for intentional non-reporting.",
    kavachDefense: "Real-time CERT-In Incident Dispatcher generating RFC-compliant JSON alerts with microsecond NTP timestamps and 180-day tamper-proof Merkle tree archives.",
    liveActionLabel: "Dispatch CERT-In 6-Hr Incident Alert",
    liveActionId: "cert-in"
  },
  {
    id: "it_act_sections",
    category: "cert-in",
    issueNum: "DIRECTIVE 05",
    soundBurst: "PENAL CODE",
    burstColor: "#B91C1C",
    title: "Information Technology Act 2000 — Criminal & Penal Sanctions",
    officialRef: "IT Act 2000 (Amended 2008) • Sections 43A, 65, 66, & 66F",
    gazette: "MeitY • Statutory Penal Code for Cyber Crimes & Critical Information Infrastructure",
    mandateComic: "Unauthorized tampering or rogue autonomous agents attempting to poison ledger records face criminal prosecution under Section 66F, which classifies attacks on critical banking networks as Cyber Terrorism.",
    legalText: "Section 43A mandates heavy compensation for failure to protect sensitive data; Section 65 penalizes tampering with computer source code; Section 66 penalizes hacking; Section 66F defines attacks on critical banking and economic infrastructure as CYBER TERRORISM.",
    penaltyBomb: "Punishment with imprisonment for life under Section 66F for cyber terrorism; up to 3 years imprisonment under Section 65 for source document tampering; unlimited civil damages under Section 43A.",
    kavachDefense: "FIPS 202 SHA3-512 Merkle tree audit engine sealing every transaction and ledger state mutation into immutable hash chains. Mathematical proof makes source and ledger tampering impossible to conceal.",
    liveActionLabel: "Run Merkle Tamper Detection Proof",
    liveActionId: "merkle"
  },
  {
    id: "meity_ai_advisory",
    category: "rbi",
    issueNum: "DIRECTIVE 06",
    soundBurst: "AI GOVERNANCE",
    burstColor: "#059669",
    title: "MeitY Advisory on Artificial Intelligence & Autonomous Agents",
    officialRef: "No. 2(4)/2023-Cyber-Laws-MeitY (March 1 & 15, 2024)",
    gazette: "Ministry of Electronics & Information Technology, Government of India",
    mandateComic: "Autonomous AI tools must operate under architectural guardrails. Every MCP tool execution must be screened for prompt injections, parameter poisoning, and unauthorized role elevation before execution.",
    legalText: "Entities deploying generative AI and autonomous agent systems must exercise strict due diligence to prevent unlawful transactions, synthetic fraud, and unverified transactional commitments. Mandatory architectural guardrails preventing LLM bypass.",
    penaltyBomb: "Complete loss of intermediary safe harbor protection under Section 79 of the IT Act; direct enterprise criminal and civil liability for autonomous financial offenses executed by AI agents.",
    kavachDefense: "Model Context Protocol (MCP) Sandbox in KAVACH enforcing Abstract Syntax Tree (AST) invariant checks (rejecting negative transfers, self-transactions, unauthorized freezes) and prompt injection screening.",
    liveActionLabel: "Test MCP Tool AST Invariant Sandbox",
    liveActionId: "mcp"
  },
  {
    id: "sebi_cscrf",
    category: "basel",
    issueNum: "DIRECTIVE 07",
    soundBurst: "ZERO-TRUST",
    burstColor: "#0891B2",
    title: "SEBI Cybersecurity and Cyber Resilience Framework (CSCRF 2024)",
    officialRef: "Circular SEBI/HO/ITD/ITD_PoD_1/P/CIR/2024/119 (June 2024)",
    gazette: "Securities and Exchange Board of India (SEBI)",
    mandateComic: "Zero-Trust Architecture is statutory policy across financial execution environments. Every transaction packet, API call, and agent query must pass sequential security gates before execution.",
    legalText: "Mandates Zero Trust Architecture (ZTA) across all algorithmic execution environments, micro-segmentation, continuous cryptographic verification, and air-gapped immutable audit logs for all transactions.",
    penaltyBomb: "Immediate suspension of algorithmic trading/payment settlement permissions, supervisory financial penalties, and mandatory blacklisting of compromised algorithmic software modules.",
    kavachDefense: "8-Gate Zero-Trust Autonomous Transaction Highway sequentially screening agent identity, rate limits, PII sanitization, prompt injection, AST parameter invariants, and 2PC saga locking.",
    liveActionLabel: "Run 8-Gate Zero-Trust Highway",
    liveActionId: "highway"
  },
  {
    id: "basel_iii_accord",
    category: "basel",
    issueNum: "DIRECTIVE 08",
    soundBurst: "CAPITAL ACCORD",
    burstColor: "#4F46E5",
    title: "Basel III International Capital Accord & Solvency Directives",
    officialRef: "Bank for International Settlements (BIS) & RBI Master Circular (2023-24)",
    gazette: "DOR.CAP.REC.15/21.06.201/2023-24 • Reserve Bank of India",
    mandateComic: "Institutions must maintain mandatory Tier-1 capital reserves (CRAR > 11.5%) and liquidity coverage (LCR > 100%) to ensure depositor protection even under concurrent automated transaction runs.",
    legalText: "Requires Tier-1 Capital Adequacy Ratio (CRAR) minimum 11.5% and Liquidity Coverage Ratio (LCR) > 100% under severe stress scenarios. Requires statutory printable supervisory dossiers for central bank review.",
    penaltyBomb: "Prompt Corrective Action (PCA) framework enforcement by central bank: mandatory suspension of dividend distributions, total restriction on loan expansion, and regulatory rating downgrade.",
    kavachDefense: "Continuous real-time CRAR (18.42%) and LCR (245%) calculation with automated OCC concurrency race defense and 1-click printable Statutory Regulatory Dossier generation.",
    liveActionLabel: "Generate Basel III Regulatory Dossier",
    liveActionId: "dossier"
  }
];

let activeGovFilter = "all";
let govRulesSearchQuery = "";

function renderGovRulesPanels() {
  const container = document.getElementById("gov-rules-panels-container");
  if (!container) return;

  const filtered = GOV_RULES_DATA.filter(item => {
    const matchCat = (activeGovFilter === "all" || item.category === activeGovFilter);
    const q = govRulesSearchQuery.toLowerCase().trim();
    const matchQuery = !q || (
      item.title.toLowerCase().includes(q) ||
      item.officialRef.toLowerCase().includes(q) ||
      item.mandateComic.toLowerCase().includes(q) ||
      item.penaltyBomb.toLowerCase().includes(q) ||
      item.kavachDefense.toLowerCase().includes(q) ||
      item.soundBurst.toLowerCase().includes(q)
    );
    return matchCat && matchQuery;
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="comic-empty-state">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:var(--primary-blue);margin-bottom:12px;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <h4 style="font-size:1.15rem;font-weight:700;margin:0 0 6px;color:var(--text-main);">NO STATUTES MATCH YOUR SEARCH</h4>
        <p style="font-size:0.86rem;color:var(--text-body);margin:0 0 14px;">Try searching for "Aadhaar", "Escrow", "Penalty", "6-Hour", or reset your category filter.</p>
        <button type="button" class="btn-primary" onclick="filterGovRules('all')">Reset All Filters</button>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(rule => `
    <article class="comic-panel-card" id="gov-card-${rule.id}">
      <div class="comic-panel-top">
        <div class="comic-issue-box">
          <span class="comic-issue-tag">${rule.issueNum}</span>
          <span class="comic-burst-tag">${rule.soundBurst}</span>
        </div>
        <div class="comic-statute-category">
          <span class="comic-cat-badge">${rule.category.toUpperCase()} COMPLIANCE</span>
        </div>
      </div>

      <h3 class="comic-statute-title">${rule.title}</h3>
      <div class="comic-citation-box">
        <span class="comic-cite-label">OFFICIAL DIRECTIVE:</span>
        <span class="comic-cite-text">${rule.officialRef}</span>
      </div>

      <div class="comic-mandate-speech">
        <div class="comic-mandate-label">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="vertical-align:middle;margin-right:4px;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          STATUTORY MANDATE
        </div>
        <p class="comic-mandate-text">"${rule.mandateComic}"</p>
      </div>

      <div class="comic-legal-box">
        <div class="comic-legal-header">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-right:4px;color:var(--text-muted);"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          <strong style="font-size:0.8rem;letter-spacing:0.3px;">LEGAL SECTION REQUIREMENT:</strong>
        </div>
        <p class="comic-legal-text">${rule.legalText}</p>
      </div>

      <div class="comic-penalty-box">
        <div class="comic-penalty-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="vertical-align:middle;margin-right:4px;"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          STATUTORY PENALTY &amp; SANCTIONS
        </div>
        <div class="comic-penalty-desc">${rule.penaltyBomb}</div>
      </div>

      <div class="comic-defense-box">
        <div class="comic-defense-header">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="vertical-align:middle;margin-right:4px;color:var(--primary-blue);"><polyline points="20 6 9 17 4 12"/></svg>
          <strong style="font-size:0.8rem;letter-spacing:0.3px;">KAVACH SYSTEM ENFORCEMENT:</strong>
        </div>
        <p class="comic-defense-text">${rule.kavachDefense}</p>
      </div>

      <div class="comic-action-strip">
        <button type="button" class="comic-interactive-btn" onclick="triggerGovRuleAction('${rule.liveActionId}', '${rule.title.replace(/'/g, "\\'")}')" title="Test this statutory enforcement live">
          <span>${rule.liveActionLabel}</span>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
        </button>
        <span class="comic-verified-tag">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" style="vertical-align:middle;margin-right:2px;"><polyline points="20 6 9 17 4 12"/></svg>
          ZERO-BYPASS VERIFIED
        </span>
      </div>
    </article>
  `).join("");
}

function filterGovRules(cat) {
  activeGovFilter = cat;
  document.querySelectorAll(".comic-pill-filter").forEach(btn => {
    if (btn.getAttribute("data-filter") === cat) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });
  renderGovRulesPanels();
}

function handleGovRulesSearch() {
  const input = document.getElementById("gov-rules-search");
  govRulesSearchQuery = input ? input.value : "";
  renderGovRulesPanels();
}

function openGovRulesModal(filter = "all") {
  const modal = document.getElementById("gov-rules-modal");
  if (!modal) return;
  activeGovFilter = filter;
  govRulesSearchQuery = "";
  const searchInput = document.getElementById("gov-rules-search");
  if (searchInput) searchInput.value = "";

  document.querySelectorAll(".comic-pill-filter").forEach(btn => {
    if (btn.getAttribute("data-filter") === filter) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  renderGovRulesPanels();
  modal.style.display = "flex";
  document.body.classList.add("modal-open");
}

function closeGovRulesModal() {
  const modal = document.getElementById("gov-rules-modal");
  if (modal) {
    modal.style.display = "none";
    document.body.classList.remove("modal-open");
  }
}

function triggerGovRuleAction(actionId, ruleTitle) {
  closeGovRulesModal();

  if (actionId === "hitl") {
    if (typeof switchTab === "function") switchTab("tab-hitl");
    showComicToast("RBI DUAL CONTROL: Navigated to Four-Eyes Quarantined Escrow Desk.");
  } else if (actionId === "escrow") {
    if (typeof switchTab === "function") switchTab("tab-transfer");
    const amountInput = document.getElementById("transfer-amount");
    const memoInput = document.getElementById("transfer-memo");
    if (amountInput) amountInput.value = "75000";
    if (memoInput) memoInput.value = "Statutory High-Value Purchase (Triggers RBI Escrow Quarantine)";
    showComicToast("RBI INR 50k+ RULE: Pre-filled INR 75,000 transfer. Click 'Execute Governed Transfer' to observe instant quarantined escrow.");
  } else if (actionId === "dpdp") {
    if (typeof switchTab === "function") switchTab("tab-accounts");
    showComicToast("DPDP ACT 2023: Customer Aadhaar & PAN are cryptographically tokenized in Core Ledgers.");
  } else if (actionId === "cert-in") {
    showCertInIncidentModal();
  } else if (actionId === "merkle") {
    if (typeof switchTab === "function") switchTab("tab-merkle");
    showComicToast("IT ACT SECTION 66F: Navigated to Post-Quantum Merkle Audit Ledger.");
  } else if (actionId === "mcp") {
    if (typeof switchTab === "function") switchTab("tab-mcp-agent");
    showComicToast("MeitY AI ADVISORY: Testing Model Context Protocol AST invariant screening.");
  } else if (actionId === "highway") {
    if (typeof switchTab === "function") switchTab("tab-highway");
    showComicToast("SEBI ZERO-TRUST: Navigated to 8-Gate Autonomous Transaction Highway.");
  } else if (actionId === "dossier") {
    if (typeof printBaselDossier === "function") {
      printBaselDossier();
    } else {
      if (typeof switchTab === "function") switchTab("tab-merkle");
      showComicToast("BASEL III: Generating Printable Statutory Regulatory Dossier.");
    }
  }
}

function showComicToast(msg) {
  let toast = document.getElementById("comic-toast-banner");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "comic-toast-banner";
    toast.className = "comic-toast-banner";
    document.body.appendChild(toast);
  }
  toast.innerHTML = `
    <span class="comic-toast-burst">ATTESTATION</span>
    <span class="comic-toast-text">${msg}</span>
    <button type="button" class="comic-toast-close" onclick="this.parentElement.classList.remove('active')">&times;</button>
  `;
  toast.classList.add("active");
  setTimeout(() => {
    if (toast) toast.classList.remove("active");
  }, 4500);
}

function showCertInIncidentModal() {
  const now = new Date();
  const incidentPayload = {
    incident_id: `CERTIN-INC-${now.getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`,
    reporting_statute: "CERT-In Cyber Security Directions (No. 20(3)/2022-CERT-In) Section 70B(6)",
    statutory_window_hours: 6,
    ntp_source: "National Physical Laboratory (NPL) New Delhi",
    timestamp_utc: now.toISOString(),
    severity: "CRITICAL_SEV1_CONTAINED",
    affected_infrastructure: "Bharat Core Banking System & Autonomous Payment Highway",
    attack_classification: "OWASP LLM01 Prompt Injection & Parameter Tampering Attempt",
    kavach_response_status: "AUTOMATICALLY_BLOCKED_AND_QUARANTINED",
    sha3_512_merkle_leaf: "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    audit_log_retention_days: 180,
    ciso_attestation: "Verified by Kavach Statutory Governance Module"
  };

  alert(`[CERT-In 6-HOUR STATUTORY INCIDENT DISPATCH SIMULATOR]\n\n` +
    `Incident ID: ${incidentPayload.incident_id}\n` +
    `Statutory Window: 6 Hours (Mandated by Section 70B(6))\n` +
    `NTP Sync: ${incidentPayload.ntp_source}\n` +
    `Timestamp: ${incidentPayload.timestamp_utc}\n` +
    `Verdict: ${incidentPayload.kavach_response_status}\n` +
    `Log Retention: 180 Days in Indian Jurisdiction\n\n` +
    `Payload dispatch successfully simulated and registered in cryptographic audit queue.`);
}

function printGovRulesDossier() {
  window.print();
}

window.openGovRulesModal = openGovRulesModal;
window.closeGovRulesModal = closeGovRulesModal;
window.filterGovRules = filterGovRules;
window.handleGovRulesSearch = handleGovRulesSearch;
window.triggerGovRuleAction = triggerGovRuleAction;
window.printGovRulesDossier = printGovRulesDossier;
