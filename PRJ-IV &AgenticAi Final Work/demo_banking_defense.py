"""
KAVACH Autonomous Multi-Agent AI Defense Demonstration
Course: CSE3101 Agentic AI - Final Capstone Project
Lead Author: Dhruv Jain (230532), BML Munjal University
Examiners: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari

Real-World Industry Scenario:
Autonomous Security Audit & Defense of Bharat Core Banking
1. Ingress Guardrail & DPDP Act 2023 Tokenization (Sentinel)
2. Strategic DAG Planning & Task Delegation (Lead Orchestrator)
3. AST Vulnerability & Dihedral D5 Verhoeff Audit (Security Auditor)
4. Atomic Invariant Patching & Maintenance (DevOps Coder)
5. Live Pytest Execution & Empirical Sign-Off (Verifier Critic)
"""

import os
import sys
import json
import time

# Ensure parent directory is on python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from kavach_agent_core.multi_agent_swarm import KavachMultiAgentSwarm, SwarmExecutionResult
from kavach_agent_core.tools import (
    tool_read_file,
    tool_validate_aadhaar_verhoeff,
    tool_dpdp_tokenize,
    tool_ast_security_scan,
    tool_run_pytest,
)


def print_banner(text: str, color_code: str = "36"):
    border = "=" * 80
    print(f"\033[{color_code}m{border}\033[0m")
    print(f"\033[1;{color_code}m  {text}\033[0m")
    print(f"\033[{color_code}m{border}\033[0m")


def print_agent_step(agent: str, event_type: str, details: dict):
    agent_colors = {
        "Sentinel": "32",          # Green
        "Orchestrator": "35",      # Purple
        "SecurityAuditor": "33",   # Yellow/Amber
        "DevOpsCoder": "36",       # Cyan
        "VerifierCritic": "32",    # Green
        "SwarmCoordinator": "34",  # Blue
    }
    color = agent_colors.get(agent, "37")
    print(f"\n\033[1;{color}m[{agent}] ➔ {event_type}\033[0m")
    for k, v in details.items():
        v_str = str(v)
        if len(v_str) > 120:
            v_str = v_str[:120] + "... [truncated]"
        print(f"  \033[90m•\033[0m \033[1m{k}:\033[0m {v_str}")


def run_full_capstone_demonstration():
    print_banner("KAVACH AUTONOMOUS MULTI-AGENT SWARM - CSE3101 CAPSTONE DEMONSTRATION", "36")
    print("Academic Context: BML Munjal University - 7th Semester B.Tech CSE")
    print("Student Architect: Dhruv Jain (230532)")
    print("Instructors: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari\n")

    goal = (
        "Perform statutory security audit on Bharat Core Banking: "
        "protect customer records for Aadhaar 9999 9999 0019 and PAN ABCDE1234F under DPDP Act 2023, "
        "execute AST vulnerability scanning on server code, and certify system via pytest verification."
    )

    print(f"\033[1;37m[INGRESS USER GOAL]:\033[0m {goal}\n")
    print("Initializing Multi-Agent Swarm with A2A Protocol and 11 MCP Tools...")

    swarm = KavachMultiAgentSwarm()

    def stream_callback(event):
        print_agent_step(event["agent"], event["event_type"], event["details"])

    start_time = time.time()
    result: SwarmExecutionResult = swarm.execute_swarm(goal=goal, on_event_callback=stream_callback)
    duration_s = round(time.time() - start_time, 2)

    print("\n" + "=" * 80)
    print_banner(f"SWARM EXECUTION FINISHED IN {duration_s}s — STATUS: {result.status}", "32")
    
    print("\n\033[1;36m[BLACKBOARD SUMMARY]:\033[0m")
    print(f"  • Session ID:        {result.session_id}")
    print(f"  • Active Provider:   {result.active_provider}")
    print(f"  • Sanitized Goal:    {result.blackboard.sanitized_goal}")
    print(f"  • A2A Messages Sent: {len(result.blackboard.messages)}")
    print(f"  • Security Findings: {len(result.blackboard.findings)}")

    print("\n\033[1;36m[FINAL CERTIFIED REPORT]:\033[0m")
    print(result.final_report)

    # Save Audit Report
    reports_dir = os.path.join(os.path.dirname(__file__), "documentation_and_reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_path = os.path.join(reports_dir, "KAVACH_AGENTIC_SECURITY_AUDIT_REPORT.json")

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(result.dict(), f, indent=2)

    print(f"\n\033[1;32m[+] Audit artifact saved to:\033[0m {report_path}")
    print("================================================================================")
    return result


if __name__ == "__main__":
    res = run_full_capstone_demonstration()
    sys.exit(0 if res.status == "COMPLETE" else 1)
