import sys
import os

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

from erp_api.main import app as fastapi_app

class VercelPathMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] in ('http', 'websocket'):
            headers = dict(scope.get('headers', []))
            matched = headers.get(b'x-matched-path') or headers.get(b'x-forwarded-uri') or headers.get(b'x-original-uri')
            path = scope.get('path', '')

            raw = None
            if matched:
                decoded = matched.decode('latin1', 'ignore').split('?')[0].strip('/')
                if decoded and not decoded.endswith('.py'):
                    raw = decoded

            if not raw and path and not path.endswith('.py'):
                raw = path.strip('/')

            if raw:
                target_path = f"/{raw}" if raw.startswith('api') else f"/api/{raw}"
                scope['path'] = target_path
                scope['raw_path'] = target_path.encode('latin1')

        await self.app(scope, receive, send)

app = VercelPathMiddleware(fastapi_app)
handler = app
