path = 'agentic_ai_midsem_work/KAVACH-main/02_Banking_and_Results_Dashboard/implementation_banks/server.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '@app.get("/api/accounts")'
replacement = """@app.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "Bharat Core Banking Highway Engine",
        "port": 8050,
        "dual_custody_escrow_active": True,
        "saga_orchestrator_active": True
    }


@app.get("/api/bank/accounts")
@app.get("/api/accounts")"""

if target in text:
    new_text = text.replace(target, replacement, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Successfully patched server.py with /health and /api/bank/accounts")
else:
    print("Target already updated or not found")

