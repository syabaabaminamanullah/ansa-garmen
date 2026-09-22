from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="ANSA ERP - Raziq Garment API",
    description="Sistem Manajemen ERP & Keuangan Raziq Garment",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "online",
        "app": "ANSA ERP - Raziq Garment",
        "version": "1.0.0",
        "database_connected": bool(os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL") or os.environ.get("STORAGE_URL")),
        "docs": "/docs"
    }

@app.get("/api")
def api_root():
    return root()

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(path_name: str, request: Request):
    if path_name in ["", "api", "api/", "api/index.py", "index.py"]:
        return root()
    return {
        "status": "online",
        "app": "ANSA ERP - Raziq Garment",
        "path": path_name,
        "url": str(request.url)
    }
