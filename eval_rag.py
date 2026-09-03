import os
import sys
import json
import time

print(f"DEBUG: sys.executable: {sys.executable}")
print(f"DEBUG: sys.path: {sys.path}")

backend_path = r"C:\Users\dhruv\OneDrive\Desktop\PRJ-IV\Kavach_AllPhases\Complete_Merged_Project\backend"
sys.path.append(backend_path)

try:
    from app.rag.ingest import ingest_repository
    print("DEBUG: app.rag.ingest imported successfully")
except Exception as e:
    print(f"DEBUG: Import Error (ingest): {e}")

try:
    from app.rag.embed_store import index_chunks, search
    print("DEBUG: app.rag.embed_store imported successfully")
except Exception as e:
    print(f"DEBUG: Import Error (embed_store): {e}")

