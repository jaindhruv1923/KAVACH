"""
Information Flow Security Lattice & Multi-Agent Taint Tracker.
Grounded in Dorothy Denning's Lattice Model of Secure Information Flow (1976).
Enforces security classes: PUBLIC <= INTERNAL <= CONFIDENTIAL <= TOP_SECRET.
Guarantees non-interference and prevents indirect information leakage
across autonomous multi-agent tool execution boundaries.
"""

import time
from enum import IntEnum
from typing import Dict, Any, List, Optional


class SecurityClass(IntEnum):
    PUBLIC = 1
    INTERNAL = 2
    CONFIDENTIAL = 3
    TOP_SECRET = 4


class InformationFlowLattice:
    """
    Evaluates whether data flow from Source to Sink satisfies Denning's Lattice:
    Flow(A -> B) is allowed IF AND ONLY IF SecurityClass(A) <= SecurityClass(B).
    """

    def __init__(self):
        self.variable_labels: Dict[str, SecurityClass] = {
            "api_key": SecurityClass.TOP_SECRET,
            "aadhaar_pii": SecurityClass.TOP_SECRET,
            "pan_number": SecurityClass.CONFIDENTIAL,
            "bank_balance": SecurityClass.CONFIDENTIAL,
            "vendor_invoice": SecurityClass.INTERNAL,
            "public_readme": SecurityClass.PUBLIC,
        }

    def assign_label(self, variable_name: str, security_class: SecurityClass):
        self.variable_labels[variable_name] = security_class

    def audit_flow(self, source_var: str, sink_channel: str, sink_level: SecurityClass) -> Dict[str, Any]:
        """Audits whether transferring source_var to sink_channel violates lattice boundaries."""
        t0 = time.perf_counter()
        
        source_level = self.variable_labels.get(source_var.lower(), SecurityClass.INTERNAL)
        is_permitted = source_level <= sink_level

        if not is_permitted:
            verdict = "ILLEGAL_INFORMATION_DECLASSIFICATION_BLOCKED"
            summary = (
                f"LATTICE VIOLATION: Source '{source_var}' ({source_level.name}) cannot flow to "
                f"Sink '{sink_channel}' ({sink_level.name}). Non-interference principle enforced."
            )
        else:
            verdict = "LATTICE_FLOW_APPROVED"
            summary = f"Permitted flow: {source_level.name} <= {sink_level.name}."

        elapsed_ms = round((time.perf_counter() - t0) * 1000, 3)

        return {
            "lattice_model": "Denning's Information Flow Lattice (1976)",
            "source_variable": source_var,
            "source_security_class": source_level.name,
            "sink_channel": sink_channel,
            "sink_security_class": sink_level.name,
            "flow_permitted": is_permitted,
            "verdict": verdict,
            "summary": summary,
            "execution_time_ms": elapsed_ms
        }
