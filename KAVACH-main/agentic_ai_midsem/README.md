# KAVACH: Phase-2 Mid-Term Evaluation Submission Package (`agentic_ai_midsem/`)
## Complete Deliverables Index for CSE3101: Agentic AI
**Course:** CSE3101 — Agentic AI (3 Credits, LDP: 2-0-2)  
**Academic Year:** 2026–27 (Batch 2023, 7th Semester B.Tech CSE)  
**Institution:** BML Munjal University (BMU), Gurugram  
**Faculty Mentors:** Dr. Soharab Hossain Shaikh (Coordinator) & Mr. Pranshu Tiwari  
**Student Team:** Dhruv Jain (230532), Hemant Goyal, Rajat Yadav  
**Repository:** `https://github.com/jaindhruv1923/KAVACH`  

---

## 1. Directory Deliverables Catalog

This directory contains the complete official deliverable package mandated for the **Phase-2 Mid-Term Capstone Evaluation** (Weightage: 30%, Rubrics C6–C10):

| Deliverable ID | File Name | Format | Description & Contents | Associated Criteria |
| :---: | :--- | :---: | :--- | :---: |
| **01** | [`01_UPDATED_PROBLEM_STATEMENT.md`](01_UPDATED_PROBLEM_STATEMENT.md) | Markdown | Updated problem statement capturing new changes: banking memo prompt injection, polyglot slopsquatting, DPDP Act zero-knowledge tokenization, and Merkle audit ledgers. | **C1, C7, C8** |
| **02** | [`02_UPDATED_PROJECT_PLAN.md`](02_UPDATED_PROJECT_PLAN.md) | Markdown | Progress vs Plan audit across 16 weeks, milestone status, slip analysis (VRAM constraints, Windows locks), and Phase-3 roadmap. | **C6, C10** |
| **03** | [`03_WORK_IN_PROGRESS_REPORT.md`](03_WORK_IN_PROGRESS_REPORT.md) | Markdown | Comprehensive Work In Progress (WIP) engineering report with explicit mapping to **CO1, CO2, CO3**, formulas, tradeoffs, and empirical metrics. | **C6 – C10** |
| **04** | [`04_CODE_AND_DEMO_GUIDE.md`](04_CODE_AND_DEMO_GUIDE.md) | Markdown | Complete code architecture map, single-command startup guides, 100% passing test commands, and 4 audited live demo scenarios. | **C8, C9** |
| **05** | [`05_1_SLIDE_COVERAGE_PROJECT_TILL_NOW_VS_CRITERIAS.md`](05_1_SLIDE_COVERAGE_PROJECT_TILL_NOW_VS_CRITERIAS.md) | Markdown | 1-Slider presentation content, comparison matrix across criteria, and accompanying 2-minute speaker script. | **C6 – C10** |
| **PPTX** | [`KAVACH_Midsem_1_Slide_Coverage_Matrix.pptx`](KAVACH_Midsem_1_Slide_Coverage_Matrix.pptx) | PowerPoint (`.pptx`) | **Native 16:9 widescreen PowerPoint presentation** containing the master 1-slider coverage matrix table and architecture summary. | **C6 – C10, C14** |
| **SLIDE PDF** | [`KAVACH_Midsem_1_Slide_Coverage_Matrix.pdf`](KAVACH_Midsem_1_Slide_Coverage_Matrix.pdf) | PDF (Landscape) | Standalone landscape slide PDF for immediate full-screen presentation projection. | **C6 – C10, C14** |
| **REPORT PDF** | [`KAVACH_MidSem_Comprehensive_Submission_Report.pdf`](KAVACH_MidSem_Comprehensive_Submission_Report.pdf) | PDF (A4 Portrait) | **Official Master Midsem Submission Report PDF** combining all 5 deliverables with BMU headers, callouts, and empirical tables. | **C1 – C10, CO1–CO3** |

---

## 2. Quick Verification Commands (Live Viva Demonstration)

```bash
# 1. Master Live E2E Integration Suite (11/11 PASSED in 4.0s):
python verification/live_e2e_integration_test.py

# 2. Focused Security Sandbox & Path Traversal Guards (5/5 PASSED in 4.1s):
python verification/focused_check.py

# 3. KAVACH Deterministic 100 Suite (100/100 PASSED in 0.38s):
pytest 01_KAVACH_Platform/tests/test_kavach_100_suite.py -q

# 4. Bharat Core Banking Highway 100 Suite (107/107 PASSED in 1.62s):
pytest 02_Banking_and_Results_Dashboard/implementation_banks/test_banking_100_suite.py -q
```

---

## 3. Web Interfaces
* **KAVACH Mission Control Command Center:** [`http://localhost:8000`](http://localhost:8000)
* **Bharat Core Banking Highway:** [`http://localhost:8000/bank`](http://localhost:8000/bank)
* **Interactive OpenAPI Swagger Docs:** [`http://localhost:8000/docs`](http://localhost:8000/docs)
