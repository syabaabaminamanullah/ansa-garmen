from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
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

def check_db():
    has_env = bool(os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL"))
    if not has_env:
        return False, "Environment variable DATABASE_URL / POSTGRES_URL not found"
    try:
        from database import engine
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "Connected to Neon PostgreSQL"
    except Exception as e:
        return False, str(e)

@app.get("/")
def root():
    db_ok, db_msg = check_db()
    return {
        "status": "online",
        "app": "ANSA ERP - Raziq Garment",
        "version": "1.0.0",
        "database_connected": db_ok,
        "database_info": db_msg,
        "docs": "/docs",
        "init_database_url": "/api/init-db"
    }

@app.get("/api")
def api_root():
    return root()

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/init-db")
def setup_database():
    try:
        from database import init_db
        init_db()
        return {
            "status": "success",
            "message": "Seluruh tabel database sistem garmen (Barang, Mitra, Karyawan, Penjualan, Pembelian, Jurnal, COA, dll) berhasil dibuat di Neon PostgreSQL!"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(path_name: str, request: Request):
    if path_name in ["", "api", "api/", "api/index.py", "index.py"]:
        return root()
    return {
        "status": "online",
        "app": "ANSA ERP - Raziq Garment",
        "path": path_name
    }
