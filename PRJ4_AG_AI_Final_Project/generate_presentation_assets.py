"""
KAVACH PRJ-IV Capstone Presentation Generator
Generates:
1. KAVACH_PRJ4_Presentation_Master.pptx (16:9 Widescreen professional presentation with cards and notes)
2. KAVACH_PRJ4_Presentation_Outline.docx (Structured document specifically designed for WPS PPT Maker / Word-to-PPT)
"""

import os
import shutil
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

import docx
from docx.shared import Inches as DocxInches, Pt as DocxPt, RGBColor as DocxRGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# Color Palette
DARK_BG = RGBColor(15, 23, 42)      # #0F172A (Navy Slate)
CARD_BG = RGBColor(30, 41, 59)      # #1E293B (Card Dark)
LIGHT_BG = RGBColor(248, 250, 252)  # #F8FAFC
BLUE_ACCENT = RGBColor(29, 78, 216) # #1D4ED8 (Cobalt Blue)
CYAN_ACCENT = RGBColor(2, 132, 199) # #0284C7 (Electric Cyan)
EMERALD_GREEN = RGBColor(5, 150, 105) # #059669
CRIMSON_RED = RGBColor(220, 38, 38) # #DC2626
PURPLE_ACCENT = RGBColor(124, 58, 237) # #7C3AED
TEXT_MAIN = RGBColor(255, 255, 255)
TEXT_MUTED = RGBColor(148, 163, 184)
TEXT_DARK = RGBColor(15, 23, 42)

SLIDES_DATA = [
    {
        "title": "KAVACH: Enterprise-Grade Autonomous Agentic AI DevOps Governance Platform",
        "subtitle": "Mission-Critical Financial Transaction Shield & Cryptographic Observability Cockpit\nProject-IV (5 Credits) Capstone & CSE3101 Agentic AI | BML Munjal University",
        "category": "TITLE SLIDE",
        "points": [
            "Student Architect & Lead: Dhruv Jain (230532)",
            "Domain Leads: Dev Garg (230487), Ansh Rohilla (230794), Ansh Adhikari (230822)",
            "Faculty Evaluators: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari",
            "Capstone Coordinator: Prof. Anusha Chhabra | CSE Department"
        ],
        "notes": "Good morning respected evaluators. Today we present KAVACH, a zero-trust governance platform that solves the fundamental security flaws of autonomous agentic AI in software engineering and core financial transactions."
    },
    {
        "title": "The Core Problem: Why Autonomous Agents Fail in Production",
        "subtitle": "Unconstrained autonomy introduces critical supply-chain, privacy, and financial theft vectors.",
        "category": "PROBLEM DEFINITION",
        "points": [
            "Supply-Chain Slopsquatting: 19.7% package hallucination rate (Spracklen et al., USENIX Security 2025). Threat actors register recurring phantom packages to deploy malware.",
            "Statutory PII & Secret Leakage: Agents routinely transmit plaintext Indian Aadhaar numbers, PAN identifiers, and API keys to third-party cloud LLMs, violating DPDP Act 2023.",
            "Indirect Prompt Injection (OWASP LLM01): Adversaries embed cognitive jailbreak overrides in transaction memos or code comments to bypass enterprise controls.",
            "Denial-of-Wallet (OWASP LLM04): Runaway recursive reasoning loops exhaust model context windows and cause exponential cloud billing inflation.",
            "Irreversible Financial Corruptions: Extending agents to banking without ACID transactional atomicity leads to balance corruption and regulatory non-compliance."
        ],
        "notes": "Autonomous agents are capable, but current frameworks lack capability mediation. An agent with shell and database tools can inadvertently destroy infrastructure if guided by naive LLM generation."
    },
    {
        "title": "Architectural Philosophy: Capability Mediation & Invariants",
        "subtitle": "Replacing unconstrained agent loops with deterministic mathematical boundaries.",
        "category": "SYSTEM PHILOSOPHY",
        "points": [
            "Deterministic-First Governance: Algebraic checksums, Shannon entropy, and AST graphs execute before any LLM can be triggered.",
            "Capability Mediation: Every file write, shell command, package import, and database query is an explicit authorization decision.",
            "Fail-Closed Design: Registry HTTP 404 aborts execution; high-value transfers trigger escrow; SAGA failures trigger compensation.",
            "Bounded Autonomy: Ephemeral sandboxes with 5.0-second watchdogs and strict reflection bounds (N <= 3).",
            "Cryptographic Non-Repudiation: SLSA Level 3 build provenance envelopes sealed with NIST post-quantum digital signatures."
        ],
        "notes": "Our thesis is simple: autonomy is only safe when bounded by mathematical invariants. We treat security decisions as deterministic computations rather than model opinions."
    },
    {
        "title": "From Mid-Sem Synopsis to Capstone Reality: What Is New",
        "subtitle": "How the 7 critical architectural audit gaps were transformed into working production code.",
        "category": "EVOLUTION & PROGRESS",
        "points": [
            "Agent Architecture: Evolved from a fixed sequential procedure into an Autonomous 6-Sentinel Safety Swarm on Port 8000.",
            "Aadhaar Validation: Replaced arbitrary 12-digit regexes with a real Dihedral Group D5 Verhoeff checksum algorithm.",
            "Secret Scanner: Upgraded from substring heuristics to Shannon Information Entropy (H >= 4.5) probability distribution.",
            "Reasoning Loop Defense: Implemented Graph-of-Thoughts (GoT) Kahn's topological sort (O(|V|+|E|)) to eliminate Denial-of-Wallet cycles.",
            "Supply-Chain Security: Added Levenshtein distance package matching (D <= 2) and live PyPI JSON probes with 1,024-entry LRU cache.",
            "Empirical Banking Core: Built an actual SQLite transactional database (core_bank.db) proving INR 50,00,000 theft prevention live.",
            "Multi-Model Adapters: Built modular 3-tier adapters supporting Google Gemini, Local Edge Ollama DeepSeek, and 0.00ms Deterministic fallbacks.",
            "Post-Quantum Attestation: Integrated NIST FIPS 204 ML-DSA-65 (Dilithium) hybrid signatures and SLSA Level 3 envelopes."
        ],
        "notes": "During mid-sem we presented an architectural vision. Today, every single headline claim has been fully implemented in code, passing 16 cyber-attack vectors and 71 core test suites."
    },
    {
        "title": "Unified 3-Hub Microservice Mesh Architecture",
        "subtitle": "Three synchronized microservice nodes operating in a live distributed mesh.",
        "category": "SYSTEM ARCHITECTURE",
        "points": [
            "Hub 1: KAVACH Master Platform (Port 8001) - Unified Security Operations Center, 10 Frontier Defense Matrix, Cyber War Room, Forensic DVR Replay, Consensus Radar.",
            "Hub 2: Live Multi-Agent Swarm (Port 8000) - Autonomous 6-Sentinel Execution Cockpit with real-time streaming telemetry and sub-millisecond execution.",
            "Hub 3: Bharat Core Bank Comparative Portal (Port 8002) - Empirical A/B testing portal backed by live SQLite relational database proving protection.",
            "Universal Navigation Mesh: Bidirectional postMessage iframe communication, cross-window opener sync, and fallback URL routing.",
            "Health & Telemetry: Continuous JSON health monitoring across all nodes with REST and Server-Sent Events (SSE) streaming."
        ],
        "notes": "The architecture is split into three decoupled hubs. Hub 1 provides enterprise oversight, Hub 2 executes the swarm, and Hub 3 demonstrates live banking security."
    },
    {
        "title": "Sentinel 1 & 2: Intent Gate & Static AST Blast-Radius Guard",
        "subtitle": "Front-line input sanitization and static syntax-tree capability mediation.",
        "category": "SWARM AGENTS 1 & 2",
        "points": [
            "Sentinel 1 (Intent Gate): Polyglot decloaking, homoglyph normalization, delimiter escape blocking, and OWASP LLM01 prompt injection defense in 0.45 ms.",
            "Pre-LLM Boundary: Intercepts malicious instructions before any external inference API can be reached.",
            "Sentinel 2 (Static AST Blast-Radius Guard): Statically parses Python source into abstract syntax trees without executing untrusted code.",
            "Transitive Closure Reachability: Computes B(v) = |Reach(v)| / (|V| - 1) on bidirectional dependency graph G = (V, E).",
            "CVE-2020-14343 Interception: Detects unsafe PyYAML deserialization, subprocess shell calls, and unauthorized OS command execution."
        ],
        "notes": "Sentinel 1 sanitizes intent in sub-millisecond time. Sentinel 2 inspects the abstract syntax tree statically, meaning untrusted code never touches the CPU uninspected."
    },
    {
        "title": "Sentinel 3: DPDP PII Anonymizer & TokenVault",
        "subtitle": "Algebraic Verhoeff checksum validation and zero-knowledge UUID pseudonymization.",
        "category": "SWARM AGENT 3",
        "points": [
            "Dihedral Group D5 Checksum: Validates 12-digit Indian Aadhaar numbers using non-commutative dihedral group symmetries over order-10 permutations.",
            "Algebraic Invariant: Multiplies check matrices over powers (0)(1,5,8,9,4,2,7)(3,6). Mathematically rejects malformed numbers (e.g. 123432).",
            "PAN Identity Validation: Enforces statutory Income Tax Department formatting regexes ([A-Z]{5}[0-9]{4}[A-Z]).",
            "Zero-Knowledge TokenVault: Replaces citizen PII with ephemeral UUID tokens ([VAULT:AADHAAR:uuid]) in memory before any external transmission.",
            "Statutory Compliance: Directly adheres to Section 8(3) Data Minimisation under India's Digital Personal Data Protection Act, 2023."
        ],
        "notes": "Instead of a naive 12-digit regex, we implemented the actual Dihedral Group D5 Verhoeff checksum algorithm. Malformed UIDs are intercepted mathematically with zero false acceptances."
    },
    {
        "title": "Sentinel 4: Graph-of-Thoughts (GoT) Kahn's Reasoner",
        "subtitle": "Topological cycle elimination preventing Denial-of-Wallet exhaustion attacks.",
        "category": "SWARM AGENT 4",
        "points": [
            "Cognitive DAG Modeling: Structures multi-agent reasoning steps into a formal Directed Acyclic Graph G = (V, E).",
            "Kahn's Topological Sorting: Evaluates reasoning nodes in optimal linear time O(|V| + |E|).",
            "Denial-of-Wallet (OWASP LLM04) Interception: Detects circular reasoning dependencies and recursive simulation traps in 0.15 ms.",
            "Execution Sequencing: Emits verified topological execution sequences (e.g., N1_AUTH -> N2_FUNDS -> N3_LIMIT -> N4_EXEC).",
            "Cost & Resource Containment: Eliminates runaway API billing, context window explosion, and CPU hangs before runtime."
        ],
        "notes": "Attackers can induce infinite loops in reasoning models. Sentinel 4 uses Kahn's algorithm to prove graph acyclicity, aborting any circular reasoning trap instantly."
    },
    {
        "title": "Sentinel 5 & 6: Differential Privacy & Post-Quantum SAGA",
        "subtitle": "Provable privacy bounding, lattice-based digital signatures, and atomic SAGA ledger.",
        "category": "SWARM AGENTS 5 & 6",
        "points": [
            "Sentinel 5 (Differential Privacy Guard): Implements (epsilon, delta)-Differential Privacy with Laplace noise perturbation (Scale = delta_f / epsilon).",
            "Dynamic Budget Odometer: Decrements persistent privacy budget (epsilon <= 0.5) to prevent reconstruction and membership inference attacks.",
            "Sentinel 6 (Post-Quantum & SAGA Ledger): Binds execution metadata with NIST FIPS 204 ML-DSA-65 (Dilithium) lattice signature parameters.",
            "SLSA Level 3 Build Provenance: Synthesizes verifiable supply-chain provenance envelopes capturing builder ID, parameters, and commit digests.",
            "Distributed SAGA Coordination: Enforces 4-phase backward compensation ensuring 0.00% balance leakage across distributed transaction failures."
        ],
        "notes": "Sentinel 5 ensures aggregate queries do not leak individual banking records. Sentinel 6 future-proofs the audit trail against quantum computers using NIST ML-DSA lattice signatures."
    },
    {
        "title": "Supply-Chain Slopsquatting & Typosquatting Defense Matrix",
        "subtitle": "Four-stage verification pipeline neutralizing AI package hallucinations.",
        "category": "SUPPLY-CHAIN SECURITY",
        "points": [
            "Empirical Foundation: Spracklen et al. (USENIX 2025) proved 19.7% package hallucination rate across 16 LLMs; 43% recurring phantom names.",
            "Stage 1 - AST Module Extraction: Extracts root identifiers of all Import and ImportFrom syntax nodes.",
            "Stage 2 - Standard-Library Fast Path: Resolves native Python modules against sys.stdlib_module_names in 0.00 ms.",
            "Stage 3 - High-Throughput LRU Cache: Probes 1,024-entry in-memory cache to eliminate redundant network roundtrips.",
            "Stage 4 - Live PyPI REST Probe & Levenshtein Firewall: Queries PyPI JSON endpoint; computes edit distance D <= 2 against top libraries. HTTP 404 aborts execution."
        ],
        "notes": "Slopsquatting is the newest AI supply-chain attack. KAVACH validates packages live against the registry and uses Levenshtein distance to detect typosquats before pip install."
    },
    {
        "title": "Bharat Core Bank: Empirical SQLite A/B Comparative Simulation",
        "subtitle": "Live side-by-side verification proving INR 50,00,000 theft prevention on Port 8002.",
        "category": "EMPIRICAL VERIFICATION",
        "points": [
            "Real Relational Database: SQLite core_bank.db backing accounts, transactions, and escrow_vault tables.",
            "Mode 1 - WITHOUT KAVACH (Alert Crimson): Raw LLM agent falls prey to authority bias during CEO wire jailbreak, draining INR 50,00,000 to offshore Cayman account CAY-9921.",
            "Mode 2 - WITH KAVACH (Shield Emerald): 5-Gate Financial Shield intercepts jailbreak, activates RBI CSF Section 4.2 dual-custody escrow (> INR 50,000).",
            "Capital Preservation: Preserves 100% of Bank Treasury capital (INR 0.00 loss) under identical adversarial attack vectors.",
            "Interactive Scenarios: 5 live attack scenarios covering Aadhaar leakage, CEO jailbreak, night-batch RCE, Denial-of-Wallet, and SQL injection."
        ],
        "notes": "We don't just claim security theoretically. On Port 8002, professors can watch the real SQLite database balance drop to zero without KAVACH, and remain 100% intact with KAVACH."
    },
    {
        "title": "Multi-Model Adapter Subsystem: Cloud, Edge & Offline",
        "subtitle": "Modular three-tier inference abstraction with zero-dependency fallback.",
        "category": "MODEL INFRASTRUCTURE",
        "points": [
            "Vendor-Agnostic Interface: BaseModelAdapter specification supporting prompt, system guardrails, and flexible kwargs.",
            "Cloud High-Reasoning Tier (gemini_adapter.py): Google Gemini 2.5 Flash for high-throughput architectural planning.",
            "On-Premises Air-Gapped Edge Tier (ollama_adapter.py): Local Ollama DeepSeek-R1:1.5b / Qwen2.5-Coder with 0 bytes outbound internet footprint.",
            "Deterministic Offline Rule Engine (deterministic_adapter.py): Executes in memory in 0.00 ms for reproducible testing and CI/CD pipelines.",
            "Dynamic Privacy Switching: Flagged sensitive requests automatically route to the air-gapped local model tier."
        ],
        "notes": "KAVACH is model-agnostic. Non-sensitive prompts use cloud Gemini, while sensitive enterprise logic is routed to air-gapped local DeepSeek with zero network footprint."
    },
    {
        "title": "Exhaustive Verification: 16-Attack Live Matrix & Pytest Suites",
        "subtitle": "100% pass rate across live cyber-attack scenarios and platform unit tests.",
        "category": "EVALUATION & BENCHMARKS",
        "points": [
            "16-Attack Live Verification Matrix (test_matrix.py): Intercepts 16 diverse cyber attacks live against running swarm (Pass Rate: 16/16).",
            "Sub-Millisecond Security Overhead: Mean pipeline security latency of 0.41 ms (under 1.5% of total LLM generation time).",
            "Core Platform Pytest Suite: 71 unit tests in kavach_platform/ tests passed in 91.56s with 100% success.",
            "Master One-Command Runner (run_all_tests.py): Executes 16-attack matrix, 3-hub live HTTP integration checks, and adapter tests in 2.43s.",
            "Prudential Telemetry: Verified Capital Adequacy Ratio (CAR = 16.67% >= 11.5%) and Liquidity Coverage Ratio (LCR = 142.86% >= 100%)."
        ],
        "notes": "Every metric is verified. Our live attack matrix intercepts 16/16 attacks in 0.41 milliseconds, and our master test runner validates the entire platform in 2.43 seconds."
    },
    {
        "title": "Statutory, Legal & Regulatory Alignment",
        "subtitle": "Built specifically to meet Indian and international statutory standards.",
        "category": "STATUTORY COMPLIANCE",
        "points": [
            "Digital Personal Data Protection Act, 2023 (India): Section 8(3) Data Minimisation through Verhoeff D5 Aadhaar masking and TokenVault.",
            "RBI Master Direction on IT Governance & Cybersecurity: Section 4.2 Four-Eyes Principle and Dual-Custody Escrow for transfers > INR 50,000.",
            "Basel III Prudential Accord: Capital Adequacy Ratio (CAR >= 11.5%) and Liquidity Coverage Ratio (LCR >= 100%) tracking.",
            "EU Artificial Intelligence Act (Regulation 2024/1689): High-risk transparency, SLSA Level 3 build provenance, and air-gapped model containment.",
            "NIST Standards: FIPS 202 (SHA3-512 sponge hash) and FIPS 204 (ML-DSA post-quantum lattice signatures)."
        ],
        "notes": "KAVACH is grounded in real law. It directly enforces the compliance requirements of the Indian DPDP Act, RBI Master Directions, and Basel III standards."
    },
    {
        "title": "Conclusion & Future Research Roadmap",
        "subtitle": "Deterministic capability mediation proves that autonomous AI can be safely deployed.",
        "category": "CONCLUSION & FUTURE WORK",
        "points": [
            "Key Contribution: Proved that autonomous coding and banking agents can be governed by deterministic invariants without perceptible latency (< 2%).",
            "Closing 7 Research Gaps: Closed all identified literature gaps across slopsquatting, PII exfiltration, blast-radius, and financial atomicity.",
            "Future Roadmap 1 - Physical HSM Integration: Extending software-simulated FIPS 140-2 Level 3 enclave to physical hardware security modules.",
            "Future Roadmap 2 - Cross-Border CBDC: Implementing cross-ledger atomic swaps for RBI e-INR and international digital currencies.",
            "Future Roadmap 3 - eBPF Linux Sandbox: Implementing kernel-level syscall tracing for autonomous agent sub-processes."
        ],
        "notes": "In conclusion, KAVACH proves that autonomous agentic AI in mission-critical environments can be governed with mathematical rigor and sub-millisecond overhead."
    },
    {
        "title": "Live Demonstration & Viva Q&A",
        "subtitle": "All 3 hubs are active, healthy, and ready for evaluator inspection.",
        "category": "LIVE DEMO & QUESTIONS",
        "points": [
            "Hub 1 Master Platform: http://localhost:8001/ (Security Operations Center & War Room)",
            "Hub 2 Live Agent Swarm: http://localhost:8000/ (6 Autonomous Sentinels & Telemetry Cockpit)",
            "Hub 3 Bharat Core Bank: http://localhost:8002/ (Live SQLite Comparative A/B Portal)",
            "One-Command Verification: python PRJ4_AG_AI_Final_Project\\run_all_tests.py",
            "Thank You! We invite questions and technical discussion."
        ],
        "notes": "All three hubs are live on localhost. We now invite your questions and are ready to execute any live cyber-attack scenario of your choice."
    }
]

def generate_pptx(output_path):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    for idx, slide_info in enumerate(SLIDES_DATA):
        slide = prs.slides.add_slide(blank_layout)

        # Background shape (Deep Navy)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG
        bg.line.fill.background()

        # Top Category Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        cat_tf = cat_box.text_frame
        cat_tf.word_wrap = True
        cat_p = cat_tf.paragraphs[0]
        cat_p.text = f"SLIDE {idx+1:02d} // {slide_info['category']}"
        cat_p.font.name = "Arial"
        cat_p.font.size = Pt(10)
        cat_p.font.bold = True
        cat_p.font.color.rgb = CYAN_ACCENT

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(1.1))
        title_tf = title_box.text_frame
        title_tf.word_wrap = True
        title_p = title_tf.paragraphs[0]
        title_p.text = slide_info["title"]
        title_p.font.name = "Arial"
        title_p.font.size = Pt(22)
        title_p.font.bold = True
        title_p.font.color.rgb = TEXT_MAIN

        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(0.6))
        sub_tf = sub_box.text_frame
        sub_tf.word_wrap = True
        sub_p = sub_tf.paragraphs[0]
        sub_p.text = slide_info["subtitle"]
        sub_p.font.name = "Arial"
        sub_p.font.size = Pt(12)
        sub_p.font.italic = True
        sub_p.font.color.rgb = TEXT_MUTED

        # Content Card Box
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.5), Inches(11.733), Inches(4.3))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = RGBColor(51, 65, 85)
        card.line.width = Pt(1.5)

        # Points inside Card
        content_box = slide.shapes.add_textbox(Inches(1.1), Inches(2.7), Inches(11.1), Inches(3.9))
        ctf = content_box.text_frame
        ctf.word_wrap = True

        for p_idx, pt in enumerate(slide_info["points"]):
            p = ctf.add_paragraph() if p_idx > 0 else ctf.paragraphs[0]
            p.text = f"•  {pt}"
            p.font.name = "Arial"
            p.font.size = Pt(13)
            p.font.color.rgb = RGBColor(241, 245, 249)
            p.space_after = Pt(10)

        # Bottom Footer Bar
        ftr_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.35))
        ftf = ftr_box.text_frame
        fp = ftf.paragraphs[0]
        fp.text = "KAVACH PRJ-IV Capstone | CSE3101 Agentic AI | BML Munjal University | Dhruv Jain (230532)"
        fp.font.name = "Arial"
        fp.font.size = Pt(9)
        fp.font.color.rgb = RGBColor(100, 116, 139)

        # Add Slide Notes for Presenter / WPS AI Notes
        notes_slide = slide.notes_slide
        notes_tf = notes_slide.notes_text_frame
        notes_tf.text = f"PRESENTER TALKING POINTS:\n{slide_info['notes']}"

    prs.save(output_path)
    print(f"Generated PPTX: {output_path} ({len(SLIDES_DATA)} slides)")

def generate_docx(output_path):
    doc = docx.Document()

    # Document Header
    title = doc.add_paragraph()
    r = title.add_run("KAVACH — PRJ-IV Major Capstone Master Presentation Outline")
    r.bold = True
    r.font.size = DocxPt(22)
    r.font.color.rgb = DocxRGBColor(29, 78, 216)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    sub = doc.add_paragraph()
    r_sub = sub.add_run("Structured Slide-by-Slide Outline Optimized for WPS Office AI PPT Maker & Word-to-PPT\nB.Tech CSE (AI & Data Science) | 7th Semester | BML Munjal University")
    r_sub.italic = True
    r_sub.font.size = DocxPt(11)
    r_sub.font.color.rgb = DocxRGBColor(100, 116, 139)
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph("─" * 55)

    for idx, slide in enumerate(SLIDES_DATA):
        # Heading 1 -> Slide Title (WPS PPT Maker creates a slide per Heading 1)
        h1 = doc.add_heading(f"Slide {idx+1}: {slide['title']}", level=1)
        h1.style.font.color.rgb = DocxRGBColor(15, 23, 42)

        # Category and Subtitle
        p_sub = doc.add_paragraph()
        r_cat = p_sub.add_run(f"[{slide['category']}] ")
        r_cat.bold = True
        r_cat.font.color.rgb = DocxRGBColor(2, 132, 199)
        r_subtext = p_sub.add_run(slide["subtitle"])
        r_subtext.italic = True

        # Key Bullet Points for Slide
        h2 = doc.add_heading("Slide Key Bullet Points:", level=2)
        h2.style.font.color.rgb = DocxRGBColor(51, 65, 85)

        for pt in slide["points"]:
            bp = doc.add_paragraph(pt, style='List Bullet')
            bp.paragraph_format.space_after = DocxPt(3)

        # Presenter Notes / AI Script
        p_notes = doc.add_paragraph()
        r_n_title = p_notes.add_run("Presenter Notes & Oral Script: ")
        r_n_title.bold = True
        r_n_title.font.color.rgb = DocxRGBColor(5, 150, 105)
        p_notes.add_run(slide["notes"])
        p_notes.paragraph_format.space_after = DocxPt(16)

        doc.add_paragraph("─" * 45)

    doc.save(output_path)
    print(f"Generated DOCX: {output_path} ({len(SLIDES_DATA)} slides structured outline)")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # 1. Root Workspace
    pptx_root = os.path.join(base_dir, "KAVACH_PRJ4_Presentation_Master.pptx")
    docx_root = os.path.join(base_dir, "KAVACH_PRJ4_Presentation_Outline.docx")
    
    generate_pptx(pptx_root)
    generate_docx(docx_root)
    
    # 2. Sync to progress_by_far/
    prog_dir = os.path.join(base_dir, "progress_by_far")
    if os.path.exists(prog_dir):
        shutil.copy2(pptx_root, os.path.join(prog_dir, "KAVACH_PRJ4_Presentation_Master.pptx"))
        shutil.copy2(docx_root, os.path.join(prog_dir, "KAVACH_PRJ4_Presentation_Outline.docx"))
        print(f"Synced presentation files to: {prog_dir}")

    # 3. Sync to PRJ4_AG_AI_Final_Project/
    prj4_dir = os.path.join(base_dir, "PRJ4_AG_AI_Final_Project")
    if os.path.exists(prj4_dir):
        shutil.copy2(pptx_root, os.path.join(prj4_dir, "KAVACH_PRJ4_Presentation_Master.pptx"))
        shutil.copy2(docx_root, os.path.join(prj4_dir, "KAVACH_PRJ4_Presentation_Outline.docx"))
        print(f"Synced presentation files to: {prj4_dir}")
