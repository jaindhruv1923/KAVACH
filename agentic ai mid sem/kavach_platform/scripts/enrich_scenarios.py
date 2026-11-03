import os
import json
from traces_data import traces_data

# Read existing scenarios.json
try:
    with open('agentic_ai_midsem_work/KAVACH-main/scripts/scenarios.json', 'r', encoding='utf-16') as f:
        scenarios = json.load(f)
except Exception:
    with open('agentic_ai_midsem_work/KAVACH-main/scripts/scenarios.json', 'r', encoding='utf-8') as f:
        scenarios = json.load(f)

# Attach trace arrays to all beats
for sc_key, sc_val in scenarios.items():
    if sc_key in traces_data:
        for b_num_str, beat_obj in sc_val['beats'].items():
            b_num = int(b_num_str)
            if b_num in traces_data[sc_key]:
                beat_obj['trace'] = traces_data[sc_key][b_num]

print("Attached traces to all scenarios and beats successfully.")

# Save enriched scenarios to json
with open('agentic_ai_midsem_work/KAVACH-main/scripts/enriched_scenarios.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios, f, indent=2)

print("Saved enriched_scenarios.json")

