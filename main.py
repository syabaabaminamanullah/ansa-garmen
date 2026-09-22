import os
import sys
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ERP_API_DIR = os.path.join(CURRENT_DIR, "erp_api")
if ERP_API_DIR not in sys.path:
    sys.path.insert(0, ERP_API_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

try:
    os.chdir(ERP_API_DIR)
except Exception:
    pass

# Import FastAPI instance from erp_api
import erp_api.main as erp_main
app = erp_main.app

# Static assets from compiled React frontend
FRONTEND_DIST = os.path.join(CURRENT_DIR, "erp_frontend", "dist")
ASSETS_DIR = os.path.join(FRONTEND_DIST, "assets")

if os.path.exists(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="react-assets")

# SPA catch-all route to serve the React SPA (Ansa-Enterprise / Raziq Garment)
@app.get("/{full_path:path}")
async def serve_react_frontend(full_path: str):
    target = os.path.join(FRONTEND_DIST, full_path)
    if full_path and os.path.isfile(target):
        return FileResponse(target)
    
    index_path = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    return {"message": "Ansa ERP Frontend Ready"}
