import sys
import os
from urllib.parse import parse_qs, urlencode

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
            raw = None

            if matched:
                decoded = matched.decode('latin1', 'ignore').split('?')[0].strip('/')
                if decoded and not decoded.endswith('.py'):
                    raw = decoded

            # Vercel rewrites :path* into query parameter 'path'
            query_bytes = scope.get('query_string', b'')
            if query_bytes:
                query_str = query_bytes.decode('latin1', 'ignore')
                params = parse_qs(query_str, keep_blank_values=True)
                if 'path' in params:
                    val = params.pop('path')[0].strip('/')
                    if val and not val.endswith('.py'):
                        raw = val
                    scope['query_string'] = urlencode(params, doseq=True).encode('latin1')
                elif '__path__' in params:
                    val = params.pop('__path__')[0].strip('/')
                    if val and not val.endswith('.py'):
                        raw = val
                    scope['query_string'] = urlencode(params, doseq=True).encode('latin1')

            current_path = scope.get('path', '')
            if not raw and current_path and not current_path.endswith('.py'):
                raw = current_path.strip('/')

            if raw:
                target_path = f"/{raw}" if raw.startswith('api') else f"/api/{raw}"
                scope['path'] = target_path
                scope['raw_path'] = target_path.encode('latin1')

        await self.app(scope, receive, send)

app = VercelPathMiddleware(fastapi_app)
handler = app
