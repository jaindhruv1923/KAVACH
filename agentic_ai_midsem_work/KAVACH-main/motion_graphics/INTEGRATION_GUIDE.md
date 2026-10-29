# KAVACH Motion Graphics Integration Guide

This directory (`KAVACH-main/motion_graphics`) contains the isolated, pro-level **Vector & Lottie-Grade Motion Graphics Suite** built specifically for KAVACH's autonomous cyber defense and banking AI highway.

---

## 1. Quick Launch & Preview

Double click [`run_motion_studio.bat`](run_motion_studio.bat) or open [`index.html`](index.html) in any browser.

### Key Interactive Features:
- **Speed Controls**: Toggle `0.5x Slow`, `1.0x Normal`, `2.0x Warp` to see animation physics.
- **Threat Simulation**: Click `Simulate Threat` to see all shields switch to high-alert crimson intercept states.
- **Theme Toggle**: Switch between **Dark Cyber Ops** and **Enterprise Clean Light** (matches the main KAVACH dashboard).
- **Embed Modal**: Click `< / > Get Embed Code` on any card to copy the drop-in HTML snippet.

---

## 2. Motion Graphics Inventory

| Graphic Name | Architecture Mapping | Recommended Placement |
| :--- | :--- | :--- |
| **Cyber Sentinel Shield Radar** | USENIX Supply-Chain Perimeter Shield | `frontend/index.html` (Hero Banner / Header) |
| **Bharat Core Bank Quantum Highway** | Banking Memo AST/DPDP Streaming Pipeline | `02_Banking_and_Results_Dashboard` |
| **Threat Interceptor Matrix** | Attack Vector Interception & ReAct Shield | `frontend/console.html` (Live Attack Monitor) |
| **Multi-Agent FSM Mesh** | 10-Stage Coordinator / Specialist Orbs | `agentic_ai_midsem` (Architecture Showcase) |
| **Cryptographic Ledger Vault** | Tamper-Free SHA-256 Ledger Audit Seal | `docs/METRICS.md` & Banking Audit View |
| **0.006ms Latency Waveform** | Sub-Millisecond Guardrail Oscillograph | Performance Benchmarks Cockpit |

---

## 3. How to Drop Any Graphic into an Existing Page (Zero Risk)

Whenever you are ready to integrate after mid-sem evaluation:

1. Add the CSS import to the target HTML file:
   ```html
   <link rel="stylesheet" href="../motion_graphics/motion.css">
   ```
2. Copy the corresponding HTML snippet from the Studio's **"Get Embed Code"** button.
3. Done! The graphics are self-contained and run on pure 60fps vector animations with zero heavy external npm dependencies.
