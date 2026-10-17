import uvicorn
import os
import sys

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[*] Starting FloodLens AI Server on http://127.0.0.1:{port}")
    print(f"[*] Live telemetry & GIS Map available at: http://127.0.0.1:{port}/")
    print(f"[*] OpenAPI Swagger documentation at: http://127.0.0.1:{port}/docs")
    uvicorn.run("backend.app:app", host="0.0.0.0", port=port, reload=False)
