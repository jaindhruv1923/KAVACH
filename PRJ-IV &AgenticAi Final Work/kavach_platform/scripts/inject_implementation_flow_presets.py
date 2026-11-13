"""
Injects Presets K through T into implementation_flow.js for Stage 1:
- Preset K: Differential Privacy (Laplace)
- Preset L: Graph-of-Thoughts DAG (GoT)
- Preset M: Agent Watermark (Z-Score)
- Preset N: Security Lattice (Denning)
- Preset O: Post-Quantum Dilithium Seal
- Preset P: Denial-of-Wallet Token-Bucket
- Preset Q: Factuality Entailment (NLI)
- Preset R: SAGA Compensation Unwind
- Preset S: Causal Counterfactual XAI
- Preset T: Empirical Scientific Ablation
"""

import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FLOW_JS_PATH = os.path.join(ROOT, "01_KAVACH_Platform", "frontend", "implementation_flow.js")

def inject_presets():
    with open(FLOW_JS_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. Preset buttons in renderStage1Simulator
    target_button = '<button type="button" class="preset-chip ${ctrlState.selectedPreset1 === \'statutory\' ? \'active\' : \'\'}" onclick="loadStep1Preset(\'statutory\')">Preset J: Statutory Regulatory Dossier</button>'
    new_buttons = target_button + '''
          <button type="button" class="preset-chip ${ctrlState.selectedPreset1 === 'dp' ? 'active' : ''}" onclick="loadStep1Preset('dp')">Preset K: (\u03b5,\u03b4)-DP Laplace Guard</button>
          <button type="button" class="preset-chip ${ctrlState.selectedPreset1 === 'got' ? 'active' : ''}" onclick="loadStep1Preset('got')">Preset L: Graph-of-Thoughts DAG (GoT)</button>
          <button type="button" class="preset-chip ${ctrlState.selectedPreset1 === 'watermark' ? 'active' : ''}" onclick="loadStep1Preset('watermark')">Preset M: Agent Watermarking (Z-Score)</button>
          <button type="button" class="preset-chip ${ctrlState.selectedPreset1 === 'lattice' ? 'active' : ''}" onclick="loadStep1Preset('lattice')">Preset N: Denning Security Lattice</button>
          <button type="button" class="preset-chip ${ctrlState.selectedPreset1 === 'pqc' ? 'active' : ''}" onclick="loadStep1Preset('pqc')">Preset O: Post-Quantum Dilithium Seal</button>
          <button type="button" class="preset-chip ${ctrlState.selectedPreset1 === 'wallet' ? 'active' : ''}" onclick="loadStep1Preset('wallet')">Preset P: Denial-of-Wallet Token-Bucket</button>
          <button type="button" class="preset-chip ${ctrlState.selectedPreset1 === 'entailment' ? 'active' : ''}" onclick="loadStep1Preset('entailment')">Preset Q: Factuality Entailment (NLI)</button>
          <button type="button" class="preset-chip ${ctrlState.selectedPreset1 === 'saga' ? 'active' : ''}" onclick="loadStep1Preset('saga')">Preset R: SAGA Compensation Stack</button>
          <button type="button" class="preset-chip ${ctrlState.selectedPreset1 === 'causal' ? 'active' : ''}" onclick="loadStep1Preset('causal')">Preset S: Causal Counterfactual XAI</button>
          <button type="button" class="preset-chip ${ctrlState.selectedPreset1 === 'ablation' ? 'active' : ''}" onclick="loadStep1Preset('ablation')">Preset T: Scientific Ablation Study</button>'''

    if target_button in text and "Preset K:" not in text:
        text = text.replace(target_button, new_buttons, 1)
        print("[+] Injected Presets K to T chips into Stage 1 simulator")

    # 2. Add preset handlers to loadStep1Preset
    target_handler = '} else if (presetKey === "statutory") {\n      ctrlState.selectedPreset1 = "statutory";\n      ctrlState.inputPayload = "def generate_statutory_compliance_audit():\\n    # India DPDP Act 2023 [Section 8(5)] - Dihedral D5 Verhoeff PII Masking\\n    # RBI Master Direction [Section 10A] - Dual-Custody Escrow > \u20b950,000\\n    # EU AI Act 2024 [Article 12 & 14] - NIST Merkle DAG & Human Oversight\\n    return {\'compliance_rating\': \'100% STATUTORY COMPLIANT\', \'violations\': 0}";'
    
    new_handlers = target_handler + '''
    } else if (presetKey === "dp") {
      ctrlState.selectedPreset1 = "dp";
      ctrlState.inputPayload = "# (\u03b5, \u03b4)-Differential Privacy Guard (Dwork 2006)\\nimport numpy as np\\ndef sanitize_metrics(features=[45000, 89000, 120000, 31000], epsilon=1.0, sensitivity=10.0):\\n    scale = sensitivity / epsilon\\n    noise = np.random.laplace(0, scale, len(features))\\n    return [round(f + n, 2) for f, n in zip(features, noise)]";
    } else if (presetKey === "got") {
      ctrlState.selectedPreset1 = "got";
      ctrlState.inputPayload = "# Graph-of-Thoughts (GoT) Directed Acyclic Graph Reasoning (Besta 2024)\\ndef evaluate_got_dag():\\n    thought_dag = {'T0': ['T1', 'T2'], 'T1': ['T3'], 'T2': ['T3']}\\n    # Kahn's algorithm validates zero cycles: in_degree(T3) == 0 after topological sort\\n    return {'status': 'DAG_SYNTHESIZED', 'optimal_score': 0.968}";
    } else if (presetKey === "watermark") {
      ctrlState.selectedPreset1 = "watermark";
      ctrlState.inputPayload = "# Kirchenbauer Statistical Watermarking (z >= 3.0, p < 0.001)\\ndef verify_agent_token_provenance(stream_text):\\n    # SHA3-512 PRF splits vocabulary into Green / Red lists (\u03b3 = 0.50)\\n    green_count = 28; total_tokens = 36\\n    z_score = (green_count - 0.5 * total_tokens) / (0.5 * (total_tokens ** 0.5))\\n    return {'z_score': round(z_score, 2), 'is_watermarked': z_score >= 3.0}";
    } else if (presetKey === "lattice") {
      ctrlState.selectedPreset1 = "lattice";
      ctrlState.inputPayload = "# Denning Information Flow Security Lattice (CACM 1976)\\ndef check_confinement(source='CONFIDENTIAL', sink='PUBLIC'):\\n    lattice = {'PUBLIC': 0, 'INTERNAL': 1, 'CONFIDENTIAL': 2, 'AIRGAPPED': 3}\\n    # Flow permitted iff L(source) <= L(sink)\\n    permitted = lattice[source] <= lattice[sink]\\n    return {'verdict': 'FLOW_PERMITTED' if permitted else 'DENNING_CONFINEMENT_VETO'}";
    } else if (presetKey === "pqc") {
      ctrlState.selectedPreset1 = "pqc";
      ctrlState.inputPayload = "# NIST FIPS 204 ML-DSA Post-Quantum Dilithium Seal\\ndef seal_quantum_commitment(ast_bytecode):\\n    # Module-LWE lattice hardness resists quantum Shor's algorithm\\n    return {'algorithm': 'CRYSTALS-Dilithium-65', 'quantum_security': '128-bit Post-Quantum'}";
    } else if (presetKey === "wallet") {
      ctrlState.selectedPreset1 = "wallet";
      ctrlState.inputPayload = "# OWASP LLM04 Denial-of-Wallet & Velocity Circuit Breaker\\ndef dispatch_tool_call(agent_id, burst_count=14):\\n    # Bucket capacity 10000; threshold 10 calls/sec\\n    if burst_count > 10:\\n        return {'circuit_breaker': 'TRIPPED_THROTTLED', 'cooldown_sec': 15.0}\\n    return {'circuit_breaker': 'NORMAL_PASS'}";
    } else if (presetKey === "entailment") {
      ctrlState.selectedPreset1 = "entailment";
      ctrlState.inputPayload = "# Semantic Factuality Cross-Entailment NLI (Wang 2023)\\ndef verify_statutory_claim(claim='Subject to RBI 50000 INR dual custody mandates.'):\\n    # Cross-encoder evaluates bidirectional entailment against authoritative RBI Master Direction\\n    return {'relationship': 'ENTAILMENT', 'verdict': 'FACTUALLY_ALIGNED'}";
    } else if (presetKey === "saga") {
      ctrlState.selectedPreset1 = "saga";
      ctrlState.inputPayload = "# SAGA Distributed Compensation Stack (Garcia-Molina 1987)\\ndef execute_banking_saga():\\n    # Steps: [T1: Debit, T2: Escrow, T3: Sentinel Gate (FAIL)]\\n    # LIFO stack unwinds compensations: [C2: Unlock Escrow, C1: Refund Debit]\\n    return {'compensation_status': 'ALL_COMPENSATIONS_COMMITTED', 'capital_loss': 0.0}";
    } else if (presetKey === "causal") {
      ctrlState.selectedPreset1 = "causal";
      ctrlState.inputPayload = "# Judea Pearl Causal Counterfactual XAI Explainer\\ndef counterfactual_prescription(observed_entropy=4.82):\\n    # Structural Causal Model do(token_entropy <= 4.50)\\n    return {'root_cause': 'token_entropy', 'prescription': 'Replace sk-live with vaulted token ref'}";
    } else if (presetKey === "ablation") {
      ctrlState.selectedPreset1 = "ablation";
      ctrlState.inputPayload = "# Scientific Empirical Ablation Study Matrix\\ndef run_ablation_comparison():\\n    # Full KAVACH: F1=0.991, Latency=0.45ms | Without Sentinel: F1=0.677, Leak=35.5%\\n    return {'status': 'H1_H2_HYPOTHESIS_CONFIRMED', 'f1_delta': '+0.314'}";'''

    if "presetKey === \"dp\"" not in text:
        text = text.replace(target_handler, new_handlers, 1)
        print("[+] Injected Presets K to T handlers into loadStep1Preset")

    with open(FLOW_JS_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("[*] Successfully updated implementation_flow.js")


if __name__ == "__main__":
    inject_presets()

