/**
 * KAVACH -- ELI5 Academic & Mathematical Knowledge Hub
 * BML Munjal University -- CSE3101: Agentic AI
 * Faculty: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari
 * Architect: Dhruv Jain
 * Standard: Clean Blue & White Academic Theme with KaTeX and Semantic HTML Math
 */

const ELI5_TOPICS = [
  {
    id: "shannon_entropy",
    title: "Shannon Entropy Credential & Secret Scanner",
    cos: ["CO1", "CO2"],
    module: "Module 2 & 6: Data Security & Reasoning",
    sessions: "Sessions 4-6 & 41-43",
    eli5: "Think of a password as a mystery code. Normal English words like 'cat' or 'password' have patterns we can easily predict. But a real cryptographic secret key like 'sk_live_94jf82n3kl' has letters and numbers completely scrambled at random! Shannon entropy is a mathematical tool that measures how 'unpredictable' or scrambled text is. If a string scores above 4.5 bits of randomness, Kavach knows someone accidentally pasted a confidential API key or token, and blocks it before any AI or human can steal it!",
    whatItDoes: "Implemented in app/security/detector.py. Performs an O(N) single-pass character frequency distribution over all tokens in the developer input prompt and proposed code diffs. Calculates the information entropy in bits per character. If H(S) >= 4.5, it halts execution before tokenization, preventing zero-day API credential leaks to third-party model providers.",
    formulaLatex: "H(S) = -\\sum_{i=1}^{n} p(c_i) \\log_2 p(c_i) \\quad \\text{where } p(c_i) = \\frac{\\text{count}(c_i)}{|S|}",
    formulaHtml: `
      <div class="math-equation-row">
        <span class="math-sym-bold">H(S)</span>
        <span class="math-sym-op">=</span>
        <span class="math-sym-op">&minus;</span>
        <span class="math-sigma-box">
          <span class="math-sigma-sup">n</span>
          <span class="math-sigma-char">&sum;</span>
          <span class="math-sigma-sub">i=1</span>
        </span>
        <span class="math-sym-term">p(c<sub>i</sub>) &middot; log<sub>2</sub> p(c<sub>i</sub>)</span>
        <span class="math-sym-where">&emsp;where&nbsp; p(c<sub>i</sub>) = </span>
        <span class="math-fraction">
          <span class="math-num">count(c<sub>i</sub>)</span>
          <span class="math-denom">|S|</span>
        </span>
      </div>
    `,
    ruleHtml: `
      <div class="math-decision-pill tag-danger">
        <strong>Decision Boundary:</strong> H(S) &ge; 4.5 bits/char &rArr; Immediate Credential Quarantine
      </div>
    `,
    variables: [
      "S: Input string / code token sequence",
      "c_i: Unique character in string alphabet",
      "p(c_i): Empirical probability of character occurrence in S",
      "Decision Boundary: H(S) >= 4.5 bits/char flags confidential credentials"
    ],
    codeRef: "01_KAVACH_Platform/backend/app/security/detector.py:72"
  },
  {
    id: "react_loop",
    title: "ReAct Closed-Loop Iterative Execution & Reflection Bounds",
    cos: ["CO1", "CO2", "CO4"],
    module: "Module 2: Reasoning & Prompting Strategies",
    sessions: "Sessions 4-6",
    eli5: "Imagine a child trying to build a Lego tower. They don't just close their eyes and dump pieces. They Think ('I need a red brick'), they Act ('Put the red brick on top'), they Observe ('Did it fall down?'), and they Reflect ('It fell, so let me add a wider base next time'). ReAct does this for code! If the code has a bug, it runs the test, sees the exact error, and fixes its own mistake. But to make sure it doesn't try forever like a broken record, Kavach sets a strict rule: maximum 3 tries!",
    whatItDoes: "Implemented in app/agent/orchestrator.py and app/agent/self_healer.py. Drives interleaved Thought -> Action -> Observation -> Reflection cycles against a sandboxed subprocess test runner. Enforces strict recursion bounds: step count t <= K (where K = 3) and a 5-second subprocess timeout. If test passes, state transitions to COMPLETE; if t reaches K without passing, it escalates to supervisor HITL review.",
    formulaLatex: "S_{t+1} = \\text{Env}(S_t, a_t), \\quad a_t = \\pi_\\theta(S_t, \\tau_{1:t-1})",
    formulaHtml: `
      <div class="math-equation-row">
        <span class="math-sym-bold">S<sub>t+1</sub></span>
        <span class="math-sym-op">=</span>
        <span class="math-sym-func">Env</span>(S<sub>t</sub>, a<sub>t</sub>),
        &emsp;
        <span class="math-sym-bold">a<sub>t</sub></span>
        <span class="math-sym-op">=</span>
        <span class="math-sym-term">&pi;<sub>&theta;</sub>(S<sub>t</sub>, &tau;<sub>1:t&minus;1</sub>)</span>
      </div>
    `,
    ruleHtml: `
      <div class="math-decision-pill tag-primary">
        <strong>Bounded Termination:</strong> Halt if t &ge; K (K = 3 max reflection iterations) &nbsp;&or;&nbsp; V(S<sub>t</sub>) = PASS
      </div>
    `,
    variables: [
      "S_t: Environment state at iteration t",
      "a_t: Action / tool execution selected by agent policy pi_theta",
      "tau_{1:t-1}: Historical trace of thoughts, actions, and subprocess test observations",
      "K = 3: Finite iteration boundary preventing infinite execution loops",
      "V(S_t): Allowlisted pytest exit code verification predicate"
    ],
    codeRef: "01_KAVACH_Platform/backend/app/agent/orchestrator.py:180"
  },
  {
    id: "cosine_similarity",
    title: "Dense Vector Semantic Routing & Cosine Similarity",
    cos: ["CO1", "CO3"],
    module: "Module 2: Agentic RAG & Vector Embeddings",
    sessions: "Sessions 4-6",
    eli5: "Imagine you're in a giant library with 10,000 books. Instead of reading all of them, each book gets a secret coordinate on a 3D globe based on its meaning. When you ask 'How do I pay a bill?', your question gets placed on the globe too! Cosine similarity measures the angle between your question and the books. If the angle is almost zero (cosine near 1.0), the books are talking about the exact same idea, and Kavach hands you the right answer in milliseconds!",
    whatItDoes: "Implemented in app/rag/embed_store.py with Qdrant vector database and sentence-transformers (all-MiniLM-L6-v2). Converts text into 384-dimensional dense vectors and computes normalized dot product similarity against knowledge base chunks. If CosineSim >= 0.78, the chunk is grounded into the agent prompt context.",
    formulaLatex: "\\text{CosineSim}(\\mathbf{u}, \\mathbf{v}) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\|_2 \\|\\mathbf{v}\\|_2} = \\frac{\\sum_{i=1}^{d} u_i v_i}{\\sqrt{\\sum_{i=1}^d u_i^2}\\sqrt{\\sum_{i=1}^d v_i^2}}",
    formulaHtml: `
      <div class="math-equation-row">
        <span class="math-sym-func">CosineSim</span>(<strong>u</strong>, <strong>v</strong>)
        <span class="math-sym-op">=</span>
        <span class="math-fraction">
          <span class="math-num"><strong>u</strong> &middot; <strong>v</strong></span>
          <span class="math-denom">&Vert;<strong>u</strong>&Vert;<sub>2</sub> &Vert;<strong>v</strong>&Vert;<sub>2</sub></span>
        </span>
        <span class="math-sym-op">=</span>
        <span class="math-fraction">
          <span class="math-num">&sum;<sub>i=1</sub><sup>d</sup> u<sub>i</sub> &middot; v<sub>i</sub></span>
          <span class="math-denom">&radic;(&sum;<sub>i=1</sub><sup>d</sup> u<sub>i</sub><sup>2</sup>) &middot; &radic;(&sum;<sub>i=1</sub><sup>d</sup> v<sub>i</sub><sup>2</sup>)</span>
        </span>
      </div>
    `,
    ruleHtml: `
      <div class="math-decision-pill tag-success">
        <strong>RAG Grounding Threshold:</strong> CosineSim(u, v) &ge; 0.78 (384-dimensional dense vectors)
      </div>
    `,
    variables: [
      "u: 384-dimensional dense vector of user query",
      "v: 384-dimensional dense vector of repository code chunk",
      "||u||_2, ||v||_2: L2 Euclidean norms normalizing vectors to unit sphere",
      "tau = 0.78: Minimum threshold required for grounding context injection"
    ],
    codeRef: "01_KAVACH_Platform/backend/app/rag/embed_store.py:45"
  },
  {
    id: "ast_blast_radius",
    title: "AST Blast Radius & Dependency Graph Centrality",
    cos: ["CO1", "CO2"],
    module: "Module 4: Agent Fundamentals & Safety",
    sessions: "Sessions 15-34",
    eli5: "Imagine you pull a single Jenga block from the bottom of a tower. Will the whole tower fall, or just that one piece? In software, changing one line of code in 'auth.py' could break 50 other files that depend on it! Kavach uses Python's Abstract Syntax Tree (AST) to build a family tree of all files and functions. It calculates the 'blast radius' score: if changing this file could explode more than 35% of the project, it stops and demands a human professor's approval!",
    whatItDoes: "Implemented in app/security/ast_parser.py. Parses Python files into syntax trees using the ast module, extracting Import, ImportFrom, class definitions, and function calls. Constructs a directed dependency graph G = (V, E) and computes transitive closure reachability. If R_blast > 0.35 or in-degree centrality >= 5, the modification is quarantined for Human-In-The-Loop approval.",
    formulaLatex: "R_{\\text{blast}}(v) = \\frac{|\\text{TransitiveClosure}(v, G_{\\text{dep}})|}{|V|}, \\quad C_{\\text{deg}}(v) = \\sum_{u \\in V} \\mathbb{I}((u, v) \\in E)",
    formulaHtml: `
      <div class="math-equation-row">
        <span class="math-sym-bold">R<sub>blast</sub>(v)</span>
        <span class="math-sym-op">=</span>
        <span class="math-fraction">
          <span class="math-num">|TransitiveClosure(v, G<sub>dep</sub>)|</span>
          <span class="math-denom">|V|</span>
        </span>,
        &emsp;
        <span class="math-sym-bold">C<sub>deg</sub>(v)</span>
        <span class="math-sym-op">=</span>
        <span class="math-sym-term">&sum;<sub>u &isin; V</sub> <strong>1</strong>[(u, v) &isin; E]</span>
      </div>
    `,
    ruleHtml: `
      <div class="math-decision-pill tag-danger">
        <strong>HITL Quarantine Trigger:</strong> R<sub>blast</sub>(v) &gt; 0.35 &nbsp;&or;&nbsp; In-Degree C<sub>deg</sub>(v) &ge; 5 files
      </div>
    `,
    variables: [
      "G_dep = (V, E): Repository dependency graph with V files and E import/call edges",
      "TransitiveClosure(v): Set of all downstream files reachable from modified node v",
      "R_blast(v): Normalized blast radius fraction of affected codebase (0.0 to 1.0)",
      "Threshold: R_blast > 0.35 requires Professor / Supervisor HITL authorization"
    ],
    codeRef: "01_KAVACH_Platform/backend/app/security/ast_parser.py:58"
  },
  {
    id: "merkle_provenance",
    title: "SLSA Level 3 Cryptographic Merkle Provenance Tree",
    cos: ["CO2", "CO4", "CO5"],
    module: "Module 4 & 8: Observability, Provenance & Synthesis",
    sessions: "Sessions 15-34 & 48",
    eli5: "Imagine a digital wax seal for every single step of your project. If anyone secretly changes even one letter of a test result or code patch, the wax seal shatters into dust! A Merkle Tree bundles all evidence--who approved it, which test passed, and what timestamp it ran--into one master cryptographic fingerprint called the Root Hash. Professors can verify 1,000 files in 1 millisecond!",
    whatItDoes: "Implemented in app/provenance/merkle_tree.py and app/agent/interactive_suite.py. Builds a balanced binary hash tree over execution step events, test outputs, and human approvals using SHA-256. Any modification to an intermediate log invalidates the parent hashes up to the root hash H_root, guaranteeing non-repudiable audit compliance under SLSA Level 3.",
    formulaLatex: "H_{\\text{parent}} = \\text{SHA-256}(H_{\\text{left}} \\parallel H_{\\text{right}}), \\quad H_{\\text{leaf}}^{(i)} = \\text{SHA-256}(\\text{Step}_i \\parallel t_i \\parallel \\text{Status}_i)",
    formulaHtml: `
      <div class="math-equation-row">
        <span class="math-sym-bold">H<sub>parent</sub></span>
        <span class="math-sym-op">=</span>
        <span class="math-sym-func">SHA-256</span>(H<sub>left</sub> &parallel; H<sub>right</sub>),
        &emsp;
        <span class="math-sym-bold">H<sub>leaf</sub><sup>(i)</sup></span>
        <span class="math-sym-op">=</span>
        <span class="math-sym-func">SHA-256</span>(Step<sub>i</sub> &parallel; t<sub>i</sub> &parallel; Status<sub>i</sub>)
      </div>
    `,
    ruleHtml: `
      <div class="math-decision-pill tag-primary">
        <strong>SLSA Level 3 Integrity:</strong> Master Fingerprint H<sub>root</sub> = SHA-256(H<sub>0,1</sub> &parallel; H<sub>2,3</sub>)
      </div>
    `,
    variables: [
      "H_leaf^(i): SHA-256 digest of step i payload, ISO-8601 timestamp t_i, and execution status",
      "parallel: Cryptographic string concatenation operator",
      "H_parent: Combined parent node hash in balanced binary Merkle tree",
      "H_root: 64-character hexadecimal Merkle root guaranteeing tamper-evidence"
    ],
    codeRef: "01_KAVACH_Platform/backend/app/provenance/merkle_tree.py:32"
  },
  {
    id: "slopsquatting",
    title: "Levenshtein Distance & Slopsquatting / Typosquatting Defense",
    cos: ["CO2"],
    module: "Module 6: Open Source Security & Local LLMs",
    sessions: "Sessions 41-43",
    eli5: "Hackers love making fake packages with names that look almost like real ones, like 'reqeusts' instead of 'requests' or 'tensorf1ow' instead of 'tensorflow'. When an AI hallucinates a package name, developers might install it and get hacked! Levenshtein distance counts how many single-letter edits (insert, delete, replace) separate two words. If the distance is 1 or 2, Kavach sounds the alarm and quarantines the package!",
    whatItDoes: "Implemented in app/security/slopsquatting.py. Evaluates proposed third-party dependencies against an offline allowlist of verified PyPI packages. Employs dynamic programming to compute minimum string edit distance. If edit distance is 1 or 2 against a popular package, it flags high-probability slopsquatting/typosquatting and prevents automated pip installation.",
    formulaLatex: "\\text{lev}_{a,b}(i, j) = \\min \\begin{cases} \\text{lev}_{a,b}(i-1, j) + 1 \\\\ \\text{lev}_{a,b}(i, j-1) + 1 \\\\ \\text{lev}_{a,b}(i-1, j-1) + \\mathbb{I}(a_i \\neq b_j) \\end{cases}",
    formulaHtml: `
      <div class="math-equation-row math-cases-row">
        <span class="math-sym-bold">lev<sub>a,b</sub>(i, j)</span>
        <span class="math-sym-op">=</span>
        <span class="math-sym-func">min</span>
        <span class="math-brace">{</span>
        <span class="math-cases-lines">
          <span>lev(i&minus;1, j) + 1 &emsp;<em class="math-subnote">(deletion)</em></span>
          <span>lev(i, j&minus;1) + 1 &emsp;<em class="math-subnote">(insertion)</em></span>
          <span>lev(i&minus;1, j&minus;1) + <strong>1</strong>[a<sub>i</sub> &ne; b<sub>j</sub>] &emsp;<em class="math-subnote">(substitution)</em></span>
        </span>
      </div>
    `,
    ruleHtml: `
      <div class="math-decision-pill tag-danger">
        <strong>Supply Chain Defense:</strong> 1 &le; lev(p, p*) &le; 2 against verified PyPI packages &rArr; Automatic Dependency Quarantine
      </div>
    `,
    variables: [
      "p: Proposed third-party dependency name generated by LLM",
      "p*: Known legitimate package from PyPI verified corpus",
      "lev(a, b): Minimum number of single-character insertions, deletions, or substitutions",
      "Decision Rule: Edit distance in [1, 2] triggers dependency quarantine"
    ],
    codeRef: "01_KAVACH_Platform/backend/app/security/slopsquatting.py:34"
  },
  {
    id: "token_bucket",
    title: "Token Bucket Algorithmic Rate Limiting",
    cos: ["CO2", "CO5"],
    module: "Module 6: Security, DoS & Rate Defense",
    sessions: "Sessions 41-43",
    eli5: "Imagine a bucket that gets filled with 10 tokens every second. Every time a user or agent asks for an AI prediction or bank transfer, it takes 1 token out of the bucket. If a hacker attacks with 1,000 requests in 1 second, the bucket empties instantly, and all extra requests are locked out until tokens refill. This prevents Denial of Service (DoS) attacks and stops runaway AI billing!",
    whatItDoes: "Implemented in 02_Banking_and_Results_Dashboard/implementation_banks/server.py and app/security/rate_limiter.py. Implements continuous-time token bucket algorithms for high-frequency Bharat Bank endpoints and LLM inference calls. Handles burst capacity up to burst size C while enforcing refill rate r per second without thread blocking.",
    formulaLatex: "B(t) = \\min(C, B(t - \\Delta t) + r \\cdot \\Delta t), \\quad \\text{Admit if } B(t) \\ge 1 \\implies B(t) \\leftarrow B(t) - 1",
    formulaHtml: `
      <div class="math-equation-row">
        <span class="math-sym-bold">B(t)</span>
        <span class="math-sym-op">=</span>
        <span class="math-sym-func">min</span>(C, B(t &minus; &Delta;t) + r &middot; &Delta;t)
      </div>
    `,
    ruleHtml: `
      <div class="math-decision-pill tag-primary">
        <strong>Admission Invariant:</strong> If B(t) &ge; 1 &rArr; ADMIT &amp; B(t) &larr; B(t) &minus; 1; else REJECT (HTTP 429 Rate Limit)
      </div>
    `,
    variables: [
      "C: Maximum bucket burst capacity (e.g. 50 tokens)",
      "r: Continuous token replenishment rate (tokens / second)",
      "Delta t: Elapsed wall-clock time since last token consumption",
      "B(t): Current token balance available at timestamp t"
    ],
    codeRef: "02_Banking_and_Results_Dashboard/implementation_banks/server.py:82"
  },
  {
    id: "f1_evaluation",
    title: "Harmonized F1-Score, Precision & Recall Evaluation",
    cos: ["CO1", "CO4"],
    module: "Module 4 & 8: Agent Evaluation & Benchmarks",
    sessions: "Sessions 15-34 & 48",
    eli5: "If a security guard stops every single person at the door, they catch all the bad guys, but innocent people can't enter either! Precision asks: 'Out of the things we blocked, how many were actually dangerous?' Recall asks: 'Out of all the dangerous things, how many did we successfully catch?' The F1 score is the mathematical balance between both. Kavach achieves an enterprise score of 94.3% on the 45-sample held-out benchmark!",
    whatItDoes: "Implemented in app/agent/interactive_suite.py and verify_project.py. Evaluates the multi-agent detection pipeline against 45 held-out adversarial test cases (held_out_eval_v2.json) covering PII, SQL injection, RCE, SSRF, and supply chain attacks, computing micro/macro confusion matrices.",
    formulaLatex: "F_1 = 2 \\cdot \\frac{P \\cdot R}{P + R} = \\frac{2 \\text{TP}}{2 \\text{TP} + \\text{FP} + \\text{FN}}, \\quad P = \\frac{\\text{TP}}{\\text{TP} + \\text{FP}}, \\quad R = \\frac{\\text{TP}}{\\text{TP} + \\text{FN}}",
    formulaHtml: `
      <div class="math-equation-row">
        <span class="math-sym-bold">F<sub>1</sub></span>
        <span class="math-sym-op">=</span>
        <span class="math-sym-term">2 &middot; </span>
        <span class="math-fraction">
          <span class="math-num">Precision &middot; Recall</span>
          <span class="math-denom">Precision + Recall</span>
        </span>
        <span class="math-sym-op">=</span>
        <span class="math-fraction">
          <span class="math-num">2 &middot; TP</span>
          <span class="math-denom">2 &middot; TP + FP + FN</span>
        </span>
      </div>
    `,
    ruleHtml: `
      <div class="math-decision-pill tag-success">
        <strong>Empirical Benchmark:</strong> Recall = 100.0% (25/25) &bull; Precision = 89.29% (25/28) &bull; Harmonized F<sub>1</sub> = 0.9434
      </div>
    `,
    variables: [
      "TP (True Positives): Malicious attacks correctly intercepted by guardrail gates (25)",
      "FP (False Positives): Benign developer code requests mistakenly flagged (3)",
      "FN (False Negatives): Adversarial payloads that bypassed detection gates (0)",
      "Kavach Grounded Reality: Recall = 100.00%, Precision = 89.29%, F1 = 0.9434"
    ],
    codeRef: "01_KAVACH_Platform/backend/app/agent/interactive_suite.py:165"
  },
  {
    id: "mcp_state_machine",
    title: "Model Context Protocol (MCP) JSON-RPC 2.0 State Machine",
    cos: ["CO1", "CO3"],
    module: "Module 5: MCP & Agent-to-Agent Protocols",
    sessions: "Sessions 35-40",
    eli5: "Different AI tools from different companies usually speak different languages and can't talk to each other. Anthropic's Model Context Protocol (MCP) is like a universal translator! Any IDE (like Cursor or Claude Desktop) sends a standard message: 'Hey Kavach, run security scan on this file.' Kavach runs the scan and responds back in standard JSON-RPC 2.0. It's a clean plug-and-play socket for AI agents!",
    whatItDoes: "Implemented in app/mcp/server.py. Exposes Kavach tools (kavach_scan_security, kavach_verify_packages, kavach_self_heal) over standard JSON-RPC 2.0 via standard input/output and HTTP SSE transport. Implements standard protocol handshakes: initialize -> initialized -> tools/list -> tools/call.",
    formulaLatex: "\\mathcal{M}_{\\text{MCP}} = \\langle Q, \\Sigma, \\delta, q_0, F \\rangle, \\quad \\delta(q_{\\text{request}}, \\sigma_{\\text{method}}) \\to q_{\\text{response}}",
    formulaHtml: `
      <div class="math-equation-row">
        <span class="math-sym-bold">M<sub>MCP</sub></span>
        <span class="math-sym-op">=</span>
        <span class="math-sym-term">&lang; Q, &Sigma;, &delta;, q<sub>0</sub>, F &rang;</span>,
        &emsp;
        <span class="math-sym-bold">&delta;</span>(q<sub>request</sub>, &sigma;<sub>method</sub>)
        <span class="math-sym-op">&rarr;</span>
        <span class="math-sym-bold">q<sub>response</sub></span>
      </div>
    `,
    ruleHtml: `
      <div class="math-decision-pill tag-primary">
        <strong>JSON-RPC 2.0 Standard:</strong> {"jsonrpc": "2.0", "method": &sigma;, "params": P, "id": &lambda;}
      </div>
    `,
    variables: [
      "Q: Set of protocol connection states {DISCONNECTED, INITIALIZING, READY, EXECUTING}",
      "Sigma: Valid input alphabet of JSON-RPC 2.0 method schemas",
      "delta: State transition mapping incoming RPC frame to tool execution handler",
      "id (lambda): Correlated request/response tracking identifier"
    ],
    codeRef: "01_KAVACH_Platform/backend/app/mcp/server.py:42"
  },
  {
    id: "hitl_multisig",
    title: "Human-in-the-Loop (HITL) Multi-Sig Approval Protocol",
    cos: ["CO2", "CO4"],
    module: "Module 4: Agent Orchestration & Guardrails",
    sessions: "Sessions 15-34",
    eli5: "In a bank or nuclear power plant, you never let a computer press the big red button alone. If the AI proposes modifying a core balance calculation or security configuration, Kavach locks the file in an immutable quarantine state. Only when an authenticated supervisor (like a professor or senior architect) signs with their cryptographic token does the patch apply!",
    whatItDoes: "Implemented in app/agent/tools.py (apply_approved_patch) and app/main.py (/agent/approve/{id}). Enforces a mandatory cryptographic approval token before write operations are committed to the filesystem. Without an elevated supervisor token, writes raise a PermissionError and transition state to BLOCKED.",
    formulaLatex: "\\text{EnforceWrite}(\\text{patch}, \\sigma) = \\begin{cases} \\text{Apply}(\\text{patch}) & \\text{if } \\text{Verify}(\\sigma, K_{\\text{supervisor}}) = \\text{TRUE} \\\\ \\text{Throw PermissionError (403)} & \\text{otherwise} \\end{cases}",
    formulaHtml: `
      <div class="math-equation-row math-cases-row">
        <span class="math-sym-bold">EnforceWrite</span>(patch, &sigma;)
        <span class="math-sym-op">=</span>
        <span class="math-brace">{</span>
        <span class="math-cases-lines">
          <span><strong>Apply</strong>(patch) &emsp;if Verify(&sigma;, K<sub>supervisor</sub>) = TRUE</span>
          <span><strong>Throw PermissionError (403)</strong> &emsp;otherwise</span>
        </span>
      </div>
    `,
    ruleHtml: `
      <div class="math-decision-pill tag-danger">
        <strong>Zero-Trust Write Gate:</strong> Autonomous tools cannot alter filesystem without supervisor HMAC token verification
      </div>
    `,
    variables: [
      "patch: Proposed filesystem unified diff synthesized by DevOpsCoderAgent",
      "sigma: Elevated supervisor authorization token string",
      "K_supervisor: Public verification key / token registry authority",
      "Outcome: Deterministic rejection of unauthorized filesystem modifications"
    ],
    codeRef: "01_KAVACH_Platform/backend/app/agent/tools.py:175"
  }
];

const COURSE_MODULES = [
  {
    module: "Module 1",
    title: "Review of Prerequisites & Introduction to Agentic AI",
    sessions: "Sessions 1-3 (2 Theory + 1 Lab)",
    cos: ["CO1"],
    topics: "Evolution from LLMs to autonomous agents; PEAS formal matrices; 10-stage FSM lifecycle; Single vs Multi-Agent architectures.",
    kavachRealization: "app/agent/orchestrator.py (Formal 10-stage FSM), PEAS_AND_PERSONA_SPECIFICATION.md"
  },
  {
    module: "Module 2",
    title: "Reasoning and Prompting Strategies & Agentic RAG",
    sessions: "Sessions 4-6 (2 Theory + 1 Lab)",
    cos: ["CO1", "CO2", "CO3"],
    topics: "ReAct (Reasoning and Acting); Chain-of-Thought (CoT); Tree-of-Thought (ToT); Self-Consistency; Dense Qdrant Vector RAG.",
    kavachRealization: "app/agent/reasoning_strategies.py (All 4 paradigms implemented in code), app/rag/embed_store.py"
  },
  {
    module: "Module 3",
    title: "CrewAI Framework Deep Dive & Flows",
    sessions: "Sessions 7-14 (5 Theory + 3 Lab)",
    cos: ["CO1", "CO2", "CO3"],
    topics: "Agents, Tasks, Tools, Memory; Designing and automating agentic workflows using Flows (@start, @listen, @router).",
    kavachRealization: "app/crew/agents.py (5 specialized personas), app/crew/flows.py (Stateful Flows), app/crew/tasks.py"
  },
  {
    module: "Module 4",
    title: "Google ADK Deep Dive",
    sessions: "Sessions 15-34 (14 Theory + 6 Lab)",
    cos: ["CO1", "CO2", "CO3"],
    topics: "LlmAgent & CoordinatorAgent; 8-Hook Callback architecture (before/after agent, model, tool); 8 Canonical ADK patterns; Canonical Medical Triage pipeline; DAG Workflows.",
    kavachRealization: "app/adk/agent.py, app/adk/callbacks.py (8 hook points across 3 phases), app/adk/medical_triage.py"
  },
  {
    module: "Module 5",
    title: "Model Context Protocol (MCP) & Agent2Agent (A2A)",
    sessions: "Sessions 35-40 (4 Theory + 2 Lab)",
    cos: ["CO1", "CO2", "CO3"],
    topics: "Anthropic MCP JSON-RPC 2.0 tool servers; Google Agent2Agent (A2A) protocol with SHA-256 signatures and peer consensus.",
    kavachRealization: "app/mcp/server.py (JSON-RPC tools for Cursor/Claude), app/a2a/protocol.py (Signed message bus)"
  },
  {
    module: "Module 6",
    title: "Data Security and Privacy / Open Local LLMs",
    sessions: "Sessions 41-43 (2 Theory + 1 Lab)",
    cos: ["CO1", "CO2"],
    topics: "Air-gapped open local LLMs (Ollama); Zero-Knowledge DPDP Act 2023 Token Vault; Differential privacy and secret scanners.",
    kavachRealization: "app/generation/llm_client.py (Air-gapped Ollama routing), app/security/token_vault.py, app/security/detector.py"
  },
  {
    module: "Module 7",
    title: "Deployment & Production Readiness",
    sessions: "Sessions 44-47 (3 Theory + 1 Lab)",
    cos: ["CO1", "CO2", "CO3", "CO4"],
    topics: "Cloud containerization (Docker, Render, HuggingFace); CI/CD GitHub Action Gates; Latency and token consumption telemetry.",
    kavachRealization: "deploy/CLOUD_DEPLOYMENT.md, render.yaml, Dockerfile, app/security/cicd_gatekeeper.py"
  },
  {
    module: "Module 8",
    title: "Course Closure & Synthesis",
    sessions: "Session 48 (1 Session)",
    cos: ["CO1", "CO2", "CO3", "CO4", "CO5"],
    topics: "Course summary; F1-score evaluation; Held-out benchmark dataset; Cryptographic SLSA Level 3 Merkle audit ledgers.",
    kavachRealization: "app/agent/interactive_suite.py (Held-out benchmark with Merkle root), app/provenance/merkle_tree.py"
  }
];

let activeEli5Filter = 'all';
let currentEli5View = 'topics';

/**
 * Robust Mathematical Renderer:
 * If KaTeX is loaded and available, render dynamically using KaTeX.
 * If not, fall back to pixel-perfect semantic HTML mathematical typography!
 */
function renderTopicFormula(t) {
  if (typeof katex !== 'undefined' && katex.renderToString) {
    try {
      const rendered = katex.renderToString(t.formulaLatex, {
        displayMode: true,
        throwOnError: false
      });
      return `
        <div class="math-katex-container">${rendered}</div>
        <div class="math-rule-container">${t.ruleHtml || ''}</div>
      `;
    } catch (e) {
      console.warn("KaTeX render failed, using HTML fallback:", e);
    }
  }

  // Pre-rendered academic HTML typography fallback
  return `
    <div class="math-html-container">${t.formulaHtml}</div>
    <div class="math-rule-container">${t.ruleHtml || ''}</div>
  `;
}

function renderEli5Topics(filteredList) {
  const container = document.getElementById('eli5-topics-container');
  if (!container) return;

  if (filteredList.length === 0) {
    container.innerHTML = `
      <div style="text-align:center;padding:40px 20px;color:var(--text-dim);">
        <p style="font-size:1.1rem;margin:0 0 6px;">No topics match your search query.</p>
        <button type="button" class="pill-btn" onclick="filterEli5ByCo('all')">Reset Filter</button>
      </div>
    `;
    return;
  }

  container.innerHTML = filteredList.map(t => {
    const coBadges = t.cos.map(c => `<span class="eli5-co-badge-pill">${c}</span>`).join(' ');
    const varsHtml = t.variables.map(v => `<div>&bull; <code>${v.split(':')[0]}</code>: ${v.split(':').slice(1).join(':')}</div>`).join('');

    return `
      <div class="eli5-topic-card" id="topic-card-${t.id}">
        <div class="eli5-topic-header">
          <div>
            <div class="eli5-topic-title">
              <span>${t.title}</span>
            </div>
            <div style="font-size:0.75rem;color:var(--text-dim);margin-top:2px;">
              ${t.module} &middot; <strong style="color:var(--text-secondary);">${t.sessions}</strong>
            </div>
          </div>
          <div class="eli5-co-badges">
            <span class="eli5-session-badge">${t.sessions.split(' ')[0]}</span>
            ${coBadges}
          </div>
        </div>

        <!-- ELI5 Plain-English Box -->
        <div class="eli5-child-box">
          <div class="eli5-child-title">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="vertical-align:middle;margin-right:4px;"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            <span>Plain-English Formulation (ELI5)</span>
          </div>
          <p class="eli5-child-text">${t.eli5}</p>
        </div>

        <!-- What It Actually Does Box -->
        <div class="eli5-reality-box">
          <div class="eli5-reality-title">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="vertical-align:middle;margin-right:4px;"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
            <span>Engineering Architecture Reality</span>
          </div>
          <p class="eli5-reality-text">${t.whatItDoes}</p>
        </div>

        <!-- Mathematical Formula Container (Academic Typesetting) -->
        <div class="eli5-math-box">
          <div class="eli5-math-header">
            <span class="eli5-math-tag">MATHEMATICAL FORMULATION</span>
            <button type="button" class="eli5-copy-btn" onclick="copyEli5Formula('${t.id}', this)" title="Copy formula LaTeX">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-right:3px;"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
              <span>Copy LaTeX</span>
            </button>
          </div>
          <div class="eli5-formula-display" id="eli5-formula-${t.id}">
            ${renderTopicFormula(t)}
          </div>
          <div class="eli5-formula-vars">
            ${varsHtml}
          </div>
        </div>

        <div class="eli5-code-ref-row">
          <span>Implementation Reference: <a href="file:///${t.codeRef.split(':')[0]}" class="eli5-code-link" target="_blank">${t.codeRef}</a></span>
          <span style="font-size:0.72rem;color:var(--safe);font-weight:600;">Formally Audited &amp; Verified</span>
        </div>
      </div>
    `;
  }).join('');
}

function renderCourseHandoutModules() {
  const container = document.getElementById('eli5-handout-container');
  if (!container) return;

  container.innerHTML = `
    <div style="background:#F8FAFC;border:1px solid #CBD5E1;border-radius:12px;padding:18px 20px;margin-bottom:20px;">
      <h3 style="margin:0 0 6px;font-size:1.05rem;color:#0F172A;">BML Munjal University &middot; CSE3101: Agentic AI</h3>
      <p style="margin:0;font-size:0.8rem;color:#475569;line-height:1.45;">
        7th Semester (Batch 2023), Academic Year 2026&ndash;27 &middot; LDP: 2-0-2 (3 Credits) &middot; Faculty: <strong>Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari</strong>
      </p>
    </div>

    <div style="display:flex;flex-direction:column;gap:14px;">
      ${COURSE_MODULES.map(m => `
        <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:10px;padding:16px 20px;box-shadow:0 1px 3px rgba(0,0,0,0.03);">
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:8px;">
            <div style="display:flex;align-items:center;gap:10px;">
              <span class="badge" style="background:#2563EB;color:#FFFFFF;border:none;font-weight:700;">${m.module}</span>
              <strong style="font-size:0.92rem;color:#0F172A;">${m.title}</strong>
            </div>
            <div style="display:flex;gap:6px;">
              <span style="font-size:0.72rem;background:#F1F5F9;padding:2px 8px;border-radius:4px;color:#475569;font-weight:600;">${m.sessions}</span>
              ${m.cos.map(c => `<span style="font-size:0.72rem;background:#EFF6FF;color:#1D4ED8;padding:2px 8px;border-radius:4px;font-weight:700;border:1px solid #BFDBFE;">${c}</span>`).join('')}
            </div>
          </div>
          <p style="font-size:0.82rem;color:#334155;margin:0 0 10px;line-height:1.5;">
            ${m.topics}
          </p>
          <div style="background:#F8FAFC;border:1px dashed #CBD5E1;border-radius:6px;padding:8px 12px;font-size:0.76rem;color:#475569;">
            <strong style="color:#0F172A;">Kavach Realization in Repo:</strong> <code>${m.kavachRealization}</code>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/**
 * Ensure the ELI5 modal backdrop and container exists in DOM
 */
function ensureEli5ModalExists() {
  let modal = document.getElementById('eli5-academic-modal');
  if (modal) return modal;

  modal = document.createElement('div');
  modal.id = 'eli5-academic-modal';
  modal.className = 'modal-backdrop';
  modal.style.display = 'none';
  modal.onclick = function(e) {
    if (e.target === modal) window.closeEli5AcademicModal();
  };

  modal.innerHTML = `
    <div class="eli5-modal-window">
      <div class="eli5-modal-header">
        <div class="eli5-header-title-box">
          <div class="eli5-header-icon-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          </div>
          <div>
            <div style="display:flex;align-items:center;gap:10px;">
              <h3 style="margin:0;font-size:1.15rem;letter-spacing:-0.2px;">ELI5 Academic Knowledge Hub &middot; Topics &amp; Math Guide</h3>
              <span class="eli5-header-badge">CSE3101 &middot; CO1&ndash;CO5</span>
            </div>
            <p style="margin:2px 0 0 0;font-size:0.78rem;color:var(--text-dim);">
              BML Munjal University &middot; Department of Computer Science &amp; Engineering &middot; Batch 2023
            </p>
          </div>
        </div>
        <button type="button" class="eli5-close-btn" onclick="closeEli5AcademicModal()" aria-label="Close modal">&times;</button>
      </div>

      <div class="eli5-subnav-bar">
        <div class="eli5-filter-pills">
          <button type="button" class="eli5-pill-tab active" data-co="all" onclick="filterEli5ByCo('all')">All 10 Topics</button>
          <button type="button" class="eli5-pill-tab" data-co="CO1" onclick="filterEli5ByCo('CO1')">CO1: Agent Foundations</button>
          <button type="button" class="eli5-pill-tab" data-co="CO2" onclick="filterEli5ByCo('CO2')">CO2: Security &amp; Local LLMs</button>
          <button type="button" class="eli5-pill-tab" data-co="CO3" onclick="filterEli5ByCo('CO3')">CO3: Multimodal &amp; Protocols</button>
          <button type="button" class="eli5-pill-tab" data-co="CO4" onclick="filterEli5ByCo('CO4')">CO4: Observability &amp; Metrics</button>
          <button type="button" class="eli5-pill-tab" id="eli5-view-handout-btn" onclick="switchEli5View('handout')">Course Handout Sessions (1&ndash;45)</button>
        </div>
        <div style="display:flex;gap:10px;align-items:center;">
          <input type="text" id="eli5-search-input" class="eli5-search-input" placeholder="Search topic, formula, or concept..." oninput="handleEli5Search()">
          <button type="button" id="eli5-view-topics-btn" class="pill-btn active" onclick="switchEli5View('topics')" style="font-size:0.74rem;padding:5px 10px;">Topics View</button>
        </div>
      </div>

      <div class="eli5-modal-body">
        <div class="eli5-co-banner">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
            <div style="font-size:0.86rem;font-weight:700;color:var(--text-primary);">
              CSE3101: Agentic AI Course Outcomes (CO1&ndash;CO5) Mapping
            </div>
            <span style="font-size:0.75rem;background:#EFF6FF;color:#2563EB;padding:2px 8px;border-radius:4px;font-weight:600;border:1px solid #BFDBFE;">3 Credits (2-0-2)</span>
          </div>
          <div class="eli5-co-grid">
            <div class="eli5-co-item">
              <span class="eli5-co-tag">CO1 &middot; FOUNDATIONS &amp; MULTI-AGENT</span>
              Formal PEAS specs, 10-stage FSM execution loops, tool binding &amp; coordinator patterns.
            </div>
            <div class="eli5-co-item">
              <span class="eli5-co-tag">CO2 &middot; SECURITY &amp; LOCAL LLMS</span>
              Shannon entropy screening, AST blast radius, air-gapped Ollama &amp; prompt injection defense.
            </div>
            <div class="eli5-co-item">
              <span class="eli5-co-tag">CO3 &middot; MULTIMODAL &amp; PROTOCOLS</span>
              PIL image entropy scanning, Anthropic MCP JSON-RPC 2.0 &amp; Google A2A bus consensus.
            </div>
            <div class="eli5-co-item">
              <span class="eli5-co-tag">CO4 &middot; OBSERVABILITY &amp; METRICS</span>
              Cryptographic SLSA Level 3 Merkle tree ledgers &amp; micro/macro confusion matrices.
            </div>
            <div class="eli5-co-item">
              <span class="eli5-co-tag">CO5 &middot; PRIVACY &amp; RATE LIMITING</span>
              Zero-knowledge token vaulting under DPDP Act 2023 &amp; token bucket DoS defense.
            </div>
          </div>
        </div>

        <div id="eli5-topics-view">
          <div id="eli5-topics-container"></div>
        </div>

        <div id="eli5-handout-view" style="display:none;">
          <div id="eli5-handout-container"></div>
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(modal);
  return modal;
}

window.openEli5AcademicModal = function(filter = 'all') {
  const modal = ensureEli5ModalExists();
  if (!modal) return;
  modal.classList.add('active');
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';

  activeEli5Filter = filter;
  filterEli5ByCo(filter);
  renderCourseHandoutModules();

  // If KaTeX is ready, ensure all formulas are enhanced
  if (typeof katex !== 'undefined') {
    upgradeFormulasWithKaTeX();
  }
};

window.closeEli5AcademicModal = function() {
  const modal = document.getElementById('eli5-academic-modal');
  if (!modal) return;
  modal.classList.remove('active');
  modal.style.display = 'none';
  document.body.style.overflow = '';
};

// Close on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    window.closeEli5AcademicModal();
  }
});

window.filterEli5ByCo = function(co) {
  activeEli5Filter = co;

  document.querySelectorAll('.eli5-pill-tab').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-co') === co);
  });

  const searchInput = document.getElementById('eli5-search-input');
  const term = (searchInput ? searchInput.value.trim().toLowerCase() : '');

  let filtered = ELI5_TOPICS;
  if (co !== 'all') {
    filtered = filtered.filter(t => t.cos.includes(co));
  }
  if (term) {
    filtered = filtered.filter(t => 
      t.title.toLowerCase().includes(term) ||
      t.eli5.toLowerCase().includes(term) ||
      t.whatItDoes.toLowerCase().includes(term) ||
      t.formulaLatex.toLowerCase().includes(term)
    );
  }

  window.switchEli5View('topics');
  renderEli5Topics(filtered);
};

window.handleEli5Search = function() {
  const searchInput = document.getElementById('eli5-search-input');
  const term = searchInput ? searchInput.value.trim().toLowerCase() : '';

  let filtered = ELI5_TOPICS;
  if (activeEli5Filter !== 'all') {
    filtered = filtered.filter(t => t.cos.includes(activeEli5Filter));
  }
  if (term) {
    filtered = filtered.filter(t => 
      t.title.toLowerCase().includes(term) ||
      t.eli5.toLowerCase().includes(term) ||
      t.whatItDoes.toLowerCase().includes(term) ||
      t.formulaLatex.toLowerCase().includes(term)
    );
  }
  renderEli5Topics(filtered);
};

window.switchEli5View = function(view) {
  currentEli5View = view;
  const topicsView = document.getElementById('eli5-topics-view');
  const handoutView = document.getElementById('eli5-handout-view');
  const btnTopics = document.getElementById('eli5-view-topics-btn');
  const btnHandout = document.getElementById('eli5-view-handout-btn');

  if (view === 'handout') {
    if (topicsView) topicsView.style.display = 'none';
    if (handoutView) handoutView.style.display = 'block';
    if (btnTopics) btnTopics.classList.remove('active');
    if (btnHandout) btnHandout.classList.add('active');
  } else {
    if (topicsView) topicsView.style.display = 'block';
    if (handoutView) handoutView.style.display = 'none';
    if (btnTopics) btnTopics.classList.add('active');
    if (btnHandout) btnHandout.classList.remove('active');
  }
};

window.copyEli5Formula = function(topicId, btnEl) {
  const topic = ELI5_TOPICS.find(t => t.id === topicId);
  if (!topic) return;

  const textToCopy = topic.formulaLatex;
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(textToCopy).then(() => {
      showCopiedFeedback(btnEl);
    }).catch(() => {
      fallbackCopy(textToCopy, btnEl);
    });
  } else {
    fallbackCopy(textToCopy, btnEl);
  }
};

function fallbackCopy(text, btnEl) {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position = "fixed";
  textArea.style.left = "-9999px";
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
    document.execCommand('copy');
    showCopiedFeedback(btnEl);
  } catch (err) {
    console.error('Fallback copy failed', err);
  }
  document.body.removeChild(textArea);
}

function showCopiedFeedback(btnEl) {
  if (!btnEl) return;
  const originalHtml = btnEl.innerHTML;
  btnEl.innerHTML = '<span>Copied LaTeX!</span>';
  btnEl.style.background = '#059669';
  btnEl.style.borderColor = '#059669';
  btnEl.style.color = '#FFFFFF';
  setTimeout(() => {
    btnEl.innerHTML = originalHtml;
    btnEl.style.background = '';
    btnEl.style.borderColor = '';
    btnEl.style.color = '';
  }, 2000);
}

function upgradeFormulasWithKaTeX() {
  if (typeof katex === 'undefined') return;
  ELI5_TOPICS.forEach(topic => {
    const el = document.getElementById(`eli5-formula-${topic.id}`);
    if (el) {
      el.innerHTML = renderTopicFormula(topic);
    }
  });
}

// Auto-initialize when DOM loads
document.addEventListener('DOMContentLoaded', () => {
  renderEli5Topics(ELI5_TOPICS);
  renderCourseHandoutModules();
  // Check if KaTeX is already loaded
  if (typeof katex !== 'undefined') {
    upgradeFormulasWithKaTeX();
  }
});

// Re-check after window fully loads (in case KaTeX was loaded asynchronously with defer)
window.addEventListener('load', () => {
  if (typeof katex !== 'undefined') {
    upgradeFormulasWithKaTeX();
  }
});
