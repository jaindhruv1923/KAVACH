import importlib.util

spec = importlib.util.spec_from_file_location('agent_engine', 'live_agent_dashboard/agent_engine.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

test_cases = [
    ('your aadhar number is 123432', 'BLOCKED_AND_QUARANTINED'),
    ('SELECT * FROM users WHERE username = "admin" OR "1"="1";--', 'BLOCKED_AND_QUARANTINED'),
    ('Deploy cluster using AKIAIOSFODNN7EXAMPLE credentials', 'BLOCKED_AND_QUARANTINED'),
    ('Push release with ghp_1234567890abcdef1234567890abcdef1234', 'BLOCKED_AND_QUARANTINED'),
    ('import reqeusts\nreqeusts.get("http://bank.com")', 'BLOCKED_AND_QUARANTINED'),
    ('import yaml\nyaml.unsafe_load(data)', 'BLOCKED_AND_QUARANTINED'),
    ('Authorize transfer of 25000 INR to Rajesh Kumar. Aadhaar: 3849-2918-4729', 'SANITIZED_AND_ALLOWED')
]

all_passed = True
for text, expected in test_cases:
    res = mod.orchestrate_pipeline(mod.OrchestrationRequest(input_text=text))
    status_match = res.verdict == expected
    if not status_match:
        all_passed = False
    print(f'[{ "PASS" if status_match else "FAIL" }] "{text[:35]}..." -> Verdict: {res.verdict}')

print('\nALL SECURITY MATRIX CHECKS PASSED:', all_passed)
