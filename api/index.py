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

from fastapi.responses import JSONResponse

try:
    from erp_api.main import app

    @app.get("/api/ping")
    def ping():
        return {"pong": True}

    @app.get("/api/health")
    def health_check():
        db_status = "unknown"
        try:
            from sqlalchemy import text
            from erp_api.models import SessionLocal
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            db.close()
            db_status = "connected"
        except Exception as dbe:
            db_status = f"error: {str(dbe)}"
        return {"status": "ok", "database": db_status}

    class CatchAllMiddleware:
        def __init__(self, app):
            self.app = app

        async def __call__(self, scope, receive, send):
            try:
                await self.app(scope, receive, send)
            except Exception as e:
                err_text = traceback.format_exc()
                res = JSONResponse(
                    status_code=500,
                    content={"asgi_error": str(e), "traceback": err_text}
                )
                await res(scope, receive, send)

    handler = CatchAllMiddleware(app)
except Exception as e:
    err_tb = traceback.format_exc()
    from fastapi import FastAPI
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
