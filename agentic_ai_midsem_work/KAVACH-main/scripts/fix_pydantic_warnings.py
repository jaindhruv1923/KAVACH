import re

path = 'agentic_ai_midsem_work/KAVACH-main/02_Banking_and_Results_Dashboard/implementation_banks/server.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace example=... inside Field(...)
new_content = re.sub(r'example=("[^"]*"|\d+(?:\.\d+)?|None)', r'json_schema_extra={"example": \1}', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Successfully modernized Pydantic schemas in server.py')
