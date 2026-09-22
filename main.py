import os
import sys
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

# Pastikan path modul terbaca
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from database import engine, SessionLocal, get_db, init_db, DATABASE_URL
import models

app = FastAPI(
    title="ANSA ERP - Raziq Garment",
    description="Sistem ERP Manajemen Produksi & Keuangan Raziq Garment",
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

# HTML Dashboard Template
TEMPLATE_PATH = os.path.join(CURRENT_DIR, "templates", "index.html")

def get_html_dashboard():
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>ANSA ERP - Raziq Garment Online</h1>"

@app.get("/", response_class=HTMLResponse)
def serve_home():
    return HTMLResponse(content=get_html_dashboard())

# ----------------- API ENDPOINTS -----------------

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "ANSA ERP - Raziq Garment"}

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    is_pg = "postgresql" in str(DATABASE_URL).lower()
    db_type = "Neon PostgreSQL (Cloud)" if is_pg else "SQLite (Local)"
    
    total_barang = 0
    total_jurnal = 0
    total_mitra = 0
    total_karyawan = 0
    total_kas = 0.0

    try:
        total_barang = db.query(models.Barang).count()
        total_jurnal = db.query(models.JurnalUmum).count()
        total_mitra = db.query(models.Mitra).count()
        total_karyawan = db.query(models.Karyawan).count()

        # Hitung saldo kas dari jurnal (Akun Kas 111 / 1-1000)
        kas_rows = db.execute(text("SELECT COALESCE(SUM(debit) - SUM(kredit), 0) FROM jurnal_umum WHERE kode_akun LIKE '111%' OR kode_akun LIKE '1-10%'")).fetchone()
        if kas_rows and kas_rows[0]:
            total_kas = float(kas_rows[0])
    except Exception as e:
        print(f"Stats query fallback: {e}")

    return {
        "status": "online",
        "database_connected": True,
        "db_type": db_type,
        "total_barang": total_barang,
        "total_jurnal": total_jurnal,
        "total_mitra": total_mitra,
        "total_karyawan": total_karyawan,
        "total_kas": total_kas
    }

@app.get("/api/barang")
def list_barang(db: Session = Depends(get_db)):
    try:
        items = db.query(models.Barang).order_by(models.Barang.nama_barang).all()
        return [
            {
                "id": b.id,
                "kode_sku": b.kode_sku,
                "model_code": b.model_code,
                "nama_barang": b.nama_barang,
                "kategori": b.kategori.value if hasattr(b.kategori, "value") else str(b.kategori),
                "satuan": b.satuan,
                "stok_saat_ini": b.stok_saat_ini,
                "harga_jual": b.harga_jual,
                "harga_modal": b.harga_modal
            }
            for b in items
        ]
    except Exception as e:
        return []

@app.get("/api/jurnal")
def list_jurnal(db: Session = Depends(get_db)):
    try:
        entries = db.query(models.JurnalUmum).order_by(models.JurnalUmum.id.desc()).limit(100).all()
        return [
            {
                "id": j.id,
                "tanggal": j.tanggal.isoformat() if j.tanggal else None,
                "kode_akun": j.kode_akun,
                "nama_akun": j.nama_akun,
                "keterangan": j.keterangan,
                "debit": j.debit,
                "kredit": j.kredit
            }
            for j in entries
        ]
    except Exception as e:
        return []

@app.get("/api/mitra")
def list_mitra(db: Session = Depends(get_db)):
    try:
        mitras = db.query(models.Mitra).all()
        return [
            {
                "id": m.id,
                "nama_mitra": m.nama_mitra,
                "kategori": m.kategori.value if hasattr(m.kategori, "value") else str(m.kategori),
                "no_hp": m.no_hp,
                "email": m.email,
                "alamat": m.alamat,
                "saldo_piutang": m.saldo_piutang,
                "saldo_utang": m.saldo_utang
            }
            for m in mitras
        ]
    except Exception:
        return []

@app.get("/api/karyawan")
def list_karyawan(db: Session = Depends(get_db)):
    try:
        karyawans = db.query(models.Karyawan).all()
        return [
            {
                "id": k.id,
                "nama_karyawan": k.nama_karyawan,
                "divisi": k.divisi.value if hasattr(k.divisi, "value") else str(k.divisi),
                "tipe_gaji": k.tipe_gaji.value if hasattr(k.tipe_gaji, "value") else str(k.tipe_gaji),
                "nominal_gaji": k.nominal_gaji,
                "saldo_kasbon": k.saldo_kasbon
            }
            for k in karyawans
        ]
    except Exception:
        return []

@app.get("/api/download-apk")
def download_apk():
    apk_path = os.path.join(CURRENT_DIR, "app-release.apk")
    if os.path.exists(apk_path):
        return FileResponse(apk_path, media_type="application/vnd.android.package-archive", filename="ANSA-Garment-ERP.apk")
    return {"status": "error", "message": "APK belum tersedia"}

@app.get("/api/init-db")
def setup_database():
    try:
        init_db()
        return {
            "status": "success",
            "message": "Seluruh tabel database sistem garmen berhasil dibuat!"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Catch-all route untuk browser & Vercel rewrites
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(path_name: str, request: Request):
    if path_name in ["", "api", "api/", "api/index.py", "index.py"]:
        return HTMLResponse(content=get_html_dashboard())
    return HTMLResponse(content=get_html_dashboard())
