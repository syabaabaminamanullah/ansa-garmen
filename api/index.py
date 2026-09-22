import sys
import os
import traceback

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ERP_API_DIR = os.path.join(BASE_DIR, 'erp_api')

if ERP_API_DIR not in sys.path:
    sys.path.insert(0, ERP_API_DIR)
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

try:
    os.chdir(ERP_API_DIR)
except Exception:
    pass

try:
    import main as erp_main
    app = erp_main.app

    @app.get("/api/health")
    def health_check():
        db_status = "unknown"
        try:
            from sqlalchemy import text
            from models import SessionLocal
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            db.close()
            db_status = "connected"
        except Exception as dbe:
            db_status = f"error: {str(dbe)}"
        return {"status": "ok", "database": db_status}

    @app.get("/api/diag")
    def diag():
        try:
            from sqlalchemy import inspect
            from models import engine, SessionLocal, User
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            db = SessionLocal()
            u_count = db.query(User).count()
            users = [{"username": u.username, "role": u.role} for u in db.query(User).all()]
            db.close()
            return {
                "tables_count": len(tables),
                "tables": tables,
                "user_count": u_count,
                "users": users
            }
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    handler = app
except Exception as e:
    err_tb = traceback.format_exc()
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    error_app = FastAPI()
    
    @error_app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
    async def error_handler(full_path: str = ""):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Vercel API Import Error",
                "message": str(e),
                "traceback": err_tb,
                "sys_path": sys.path,
                "current_dir": os.getcwd()
            }
        )
    handler = error_app
    app = error_app
