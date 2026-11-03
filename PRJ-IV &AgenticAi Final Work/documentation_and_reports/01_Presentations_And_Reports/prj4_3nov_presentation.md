# PRJ4 Capstone Presentation (3 November 2026)
## What is NEW in KAVACH: Features Added Since the 29 September Mid-Term Synopsis
**Author & Lead Architect:** Dhruv Jain (Roll No. 230532)  
**Team Members:** Dhruv Jain, Dev Garg, Ansh Rohilla, Ansh Adhikari  
**Course & Department:** Project-IV (Major Capstone), Department of CSE, BML Munjal University  
**Faculty Coordinator:** Prof. Anusha Chhabra  

---

## 1. Quick Snapshot: 29 September vs. 3 November 2026

| Dimension | Mid-Term Synopsis (29 Sept 2026) | Today's Presentation (3 Nov 2026) | What This Means in Simple Words |
| :--- | :--- | :--- | :--- |
| **System Topology** | Single Python script running on 1 port. | Distributed Tri-Hub Ecosystem across Ports 8000, 8001, and 8002. | Instead of 1 program doing everything, we now have 3 specialized services talking to each other. |
| **Banking Simulator** | Printed mock text responses on the screen. | Real SQLite database (`core_bank.db`) with actual money accounts and ACID transactions. | The bank actually has real accounts and real balances that update live on disk. |
| **Capital Protection** | Theoretical discussion of banking safety. | Live A/B Demonstration: Without KAVACH drains ₹50 Lakhs; With KAVACH stops the loss 100%. | We can prove live in front of the professors: raw AI loses ₹50 Lakhs, KAVACH saves 100%. |
| **High-Value Wires** | No special rule for big amounts. | RBI Cyber Security Framework Dual-Custody Escrow (transfers > ₹50,000 locked). | Any big transfer is locked in a digital vault until 2 managers sign off. |
| **AI Agents** | 1 single pipeline step-by-step. | 6 specialized autonomous agents working as a collaborative safety team. | Like having 6 security guards in a bank, each doing one job (IDs, code, math, privacy). |
| **Cross-Framework** | No cross-framework agent communication. | Google ADK (Planner) talks directly to CrewAI (Auditor) via typed Pydantic bridge. | Two famous agent frameworks (Google ADK & CrewAI) working together smoothly. |
| **Loop Protection** | Simple ReAct retry limit ($N=3$). | Graph-of-Thoughts (GoT) with Kahn's Algorithm detecting infinite loops. | Mathematically guarantees the AI cannot get stuck in an expensive infinite loop. |
| **Privacy Protection**| Basic regex masking of numbers. | Differential Privacy Laplace Engine with an active Privacy Budget Odometer. | Adds scientific math noise so nobody can spy on customer data by asking clever questions. |
| **Package Security** | Only queried PyPI for HTTP 404. | Levenshtein Edit-Distance Typosquatting + Slopsquatting Firewall. | Catches fake packages even if someone makes a 1-letter typo (like `reqeusts` vs `requests`). |
| **Model Adapters** | Markdown documentation notes. | Real pluggable Python code adapters for Gemini, Ollama (DeepSeek), and Offline Rule Engine. | Can switch between cloud Gemini, local offline DeepSeek, or instant offline test mode. |
| **Test Suite** | 220 pytest cases. | 641 pytest tests + 16-attack automated live verification matrix (100% pass rate). | Almost 3x more tests, all running live in under 1 second. |

---

## 2. The 10 Major Brand New Features Explained in Simple Words

### Feature 1: From 1 Program to 3 Independent Hubs (The Tri-Hub Network)
- **Simple Explanation:** In September, our project was just a single backend script. Now, it is a distributed network of 3 distinct services running on different ports:
  - **Port 8001 (Master KAVACH Platform):** The central command cockpit where developers see code, architecture diagrams, and the 13 interactive security tabs.
  - **Port 8000 (Live Multi-Agent Swarm Engine):** The dedicated brain running 6 autonomous AI security agents collaborating in real time.
  - **Port 8002 (Bharat Core Bank Portal):** An enterprise banking portal where we demonstrate real-world cyber attacks against a bank.
- **Why this matters:** Evaluators can see that this is a real microservices system, not just a homework script.

### Feature 2: Real SQLite Banking Database (Real Money & Real Ledger)
- **Simple Explanation:** In September, our bank demo was just printing text messages. Now, there is an actual, persistent SQLite database (`core_bank.db`) on the computer.
  - **Real Accounts:** Bharat Corporate Reserve starts with ₹50,00,000 (50 Lakhs), TechCorp starts with ₹1,20,000, and a Cayman Offshore account starts with ₹0.
  - **Live Attack Reality:** When an attacker tricks a raw AI agent, the database literally updates: the reserve drops to ₹0, and Cayman gets ₹50 Lakhs!
  - **Live Defense Reality:** When KAVACH is turned ON, KAVACH intercepts the attack, refuses the update, and keeps all ₹50 Lakhs completely safe in the database.

### Feature 3: The RBI Dual-Custody Escrow Vault (The ₹50,000 Rule)
- **Simple Explanation:** In India, the Reserve Bank of India (RBI) mandates that no automated computer system can transfer huge sums of money without human supervision. We built this statutory rule directly into the code:
  - **Small Transfers (< ₹50,000):** If a user asks the AI to transfer ₹25,000, it is processed normally.
  - **Large Transfers (> ₹50,000):** If the transfer is ₹15,00,000 (15 Lakhs), KAVACH automatically locks the money into an Escrow Vault table. The AI is NOT allowed to complete the transfer until two authorized human bank officers give their digital signatures.

### Feature 4: 6 Specialized AI Agents Working as a Team (Swarm Architecture)
- **Simple Explanation:** Instead of one AI doing all the work, KAVACH now operates 6 specialized agents, like a well-trained security team in a bank:
  1. **Agent 1 (Sentinel Gate):** The security guard at the door. Checks prompts for passwords, injections, and identity cards in 0.04 milliseconds.
  2. **Agent 2 (AST Firewall):** The package inspector. Scans code to make sure nobody imports dangerous or fake Python packages.
  3. **Agent 3 (DPDP Tokenizer Vault):** The privacy locker. Takes real Aadhaar and PAN cards, puts them in an encrypted memory locker, and replaces them with safe fake tokens like `[VAULT:AADHAAR_9921]`.
  4. **Agent 4 (Graph-of-Thoughts Reasoner):** The logic checker. Maps out tasks as a graph and uses Kahn's algorithm to make sure the AI never gets caught in an infinite loop.
  5. **Agent 5 (Differential Privacy Engine):** The mathematician. Injects scientific privacy noise so competitors cannot guess private bank numbers.
  6. **Agent 6 (Cryptographic Attestor):** The notary officer. Signs the final code with a post-quantum cryptographic certificate (NIST ML-DSA) proving who approved the code.

### Feature 5: A2A Cross-Framework Bridge (Google ADK talking to CrewAI)
- **Simple Explanation:** In the AI world, Google has its own agent framework (Google Agent Development Kit / ADK) and the open-source community uses CrewAI. Usually, these two cannot talk to each other. We built a direct translation bridge:
  - Google ADK acts as the **Planner** (breaks user goals into steps).
  - CrewAI acts as the **Security Auditor** (checks each step for safety invariants).
  - They send each other typed JSON envelopes signed with HMAC-SHA256 digital seals in 1.12 milliseconds.

### Feature 6: Graph-of-Thoughts (GoT) Anti-Loop Shield (Kahn's Algorithm)
- **Simple Explanation:** One of the biggest fears of companies using AI agents is "Denial-of-Wallet" — where an attacker prompts the AI to do a task that loops forever, burning thousands of dollars in cloud API bills.
  - **How it Works:** We use Kahn's Topological Sorting algorithm (a famous computer science algorithm taught in data structures).
  - Before the AI executes a plan, Kahn's algorithm checks if there is any circular arrow (Task A needs B, B needs C, C needs A). If it finds a circle, it instantly kills the task in 0.5 milliseconds, saving the company's money.

### Feature 7: Differential Privacy Noise Machine with Privacy Budget Odometer
- **Simple Explanation:** Imagine a bank publishes how many fraud attempts were blocked today. If an attacker asks 100 tricky questions, they might figure out exactly which customer was targeted. Differential Privacy stops this:
  - It adds a tiny, calibrated amount of mathematical random noise (Laplace noise) to the reported numbers.
  - Like a car odometer that counts kilometers, our system tracks how much privacy budget ($\epsilon$) has been used today. If too many queries are asked, it refuses to answer to protect customer privacy.

### Feature 8: Smart Typosquatting Package Firewall (Levenshtein Distance)
- **Simple Explanation:** In September, our firewall only checked if a package existed on PyPI. But what if an attacker creates a real fake package with a 1-letter typo, like `reqeusts` instead of `requests`?
  - We now use Levenshtein distance (which measures how many letters differ between two words).
  - If the AI tries to install `reqeusts` or `cryptograpy`, KAVACH calculates that it is only 1 letter away from a famous library, identifies it as an AI hallucination / slopsquatting attack, and immediately stops the installation.

### Feature 9: Pluggable Multi-Model Adapters (Cloud, Local, and Offline)
- **Simple Explanation:** KAVACH is no longer locked into any single AI provider. We created clean, runnable Python adapter classes:
  - **Google Gemini Adapter:** For fast, high-power cloud reasoning.
  - **Local Ollama Adapter:** For running completely private models (DeepSeek-R1, LLaMA-3) on student laptops with zero internet.
  - **Deterministic Core Adapter:** For lab evaluations where you want instant, 0.001 millisecond verified answers with zero cost.

### Feature 10: 16-Attack Live Verification Matrix & 641 Total Tests
- **Simple Explanation:** In September, we had 220 tests. Today, we have:
  - **641 automated pytest test cases** in the main platform repository (100% passing).
  - A dedicated live script (`test_matrix.py`) that fires **16 real cyber attacks** (SQLi, Aadhaar leaks, AWS keys, prompt jailbreaks, typosquats) against the 6 agents, proving 100% defense in an average of 0.51 milliseconds.

---

## 3. The 2-Minute Simple Speaking Script for Your Presentation

When the professors ask: **"What have you done since your mid-term synopsis on 29 September?"**, speak these exact points:

> *"Good morning, respected professors. In our Mid-Term Synopsis on 29 September, we presented the foundational architecture of KAVACH as a single-pipeline security prototype with 220 tests.*
> 
> *Over the last five weeks, we took your feedback and made four massive, enterprise-grade leaps:*
> 
> *1. **Tri-Hub Microservices Architecture:** We evolved from a single script to a distributed 3-port network: Port 8001 runs the Master Platform, Port 8000 runs our 6-Agent Autonomous Swarm, and Port 8002 runs our Bharat Core Bank Portal.*
> 
> *2. **Real Transactional SQLite Banking:** In September, our bank demo was mock text. Today, it connects to a real SQLite database (`core_bank.db`). We can demonstrate live that an unshielded AI agent gets tricked by a prompt jailbreak and actually drains ₹50 Lakhs from the reserve, whereas KAVACH intercepts the attack, locks transactions over ₹50,000 into RBI Dual-Custody Escrow, and keeps 100% of the money safe.*
> 
> *3. **Cross-Framework A2A Protocol:** We built a standardized bridge connecting Google ADK (acting as the Planner) and CrewAI (acting as the Auditor), communicating over HMAC-SHA256 signed envelopes in 1.12 milliseconds.*
> 
> *4. **Advanced Mathematical Defenses:** We added real Graph-of-Thoughts Kahn's algorithm to eliminate infinite loops, Differential Privacy with a budget odometer, Levenshtein distance package firewalls, and expanded our test suite from 220 to 641 passing tests with a 16-attack live verification matrix.*
> 
> *All three hubs are live and running on localhost right now, and we are ready to demonstrate them."*

