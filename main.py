from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="ANSA ERP - Raziq Garment API",
    description="Sistem Manajemen ERP & Keuangan Raziq Garment",
    version="1.0.0"
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
        "database_connected": bool(os.environ.get("DATABASE_URL")),
        "docs": "/docs"
    }

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
