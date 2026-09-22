import sys
import os

# Add erp_api directory to sys.path
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
    handler = app
except Exception as e:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    error_app = FastAPI()
    @error_app.get("/{full_path:path}")
    async def error_handler(full_path: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Vercel API Import Error",
                "message": str(e),
                "sys_path": sys.path,
                "current_dir": os.getcwd()
            }
        )
    handler = error_app
    app = error_app
