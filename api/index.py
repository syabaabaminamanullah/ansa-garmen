import sys
import os
import json
import traceback

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ERP_API_DIR = os.path.join(BASE_DIR, 'erp_api')

if ERP_API_DIR not in sys.path:
    sys.path.insert(0, ERP_API_DIR)
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

_real_app = None
_init_error = None

def get_real_app():
    global _real_app, _init_error
    if _real_app is not None:
        return _real_app, None
    if _init_error is not None:
        return None, _init_error
    try:
        os.chdir(ERP_API_DIR)
        from erp_api.main import app as fastapi_app
        _real_app = fastapi_app
        return _real_app, None
    except Exception as e:
        _init_error = traceback.format_exc()
        return None, _init_error

async def app(scope, receive, send):
    if scope['type'] == 'lifespan':
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                await send({'type': 'lifespan.shutdown.complete'})
                return

    if scope['type'] != 'http':
        return

    # Restore original client path from x-matched-path header if present
    headers_dict = dict(scope.get('headers', []))
    matched_path = headers_dict.get(b'x-matched-path')
    if matched_path:
        decoded_matched = matched_path.decode('latin1')
        if decoded_matched and not decoded_matched.endswith('.py'):
            scope['path'] = decoded_matched
            scope['raw_path'] = matched_path

    path = scope.get('path', '')

    if path == '/api/debug-info':
        headers = {k.decode('latin1'): v.decode('latin1') for k, v in scope.get('headers', [])}
        body = json.dumps({
            "scope_path": path,
            "headers": headers
        }).encode('utf-8')
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'application/json'], [b'content-length', str(len(body)).encode('utf-8')]]
        })
        await send({'type': 'http.response.body', 'body': body})
        return

    real_app, err = get_real_app()
    if err:
        body = json.dumps({
            "error": "Real App Import Error",
            "traceback": err,
            "path": path
        }).encode('utf-8')
        await send({
            'type': 'http.response.start',
            'status': 500,
            'headers': [[b'content-type', b'application/json'], [b'content-length', str(len(body)).encode('utf-8')]]
        })
        await send({'type': 'http.response.body', 'body': body})
        return

    try:
        await real_app(scope, receive, send)
    except Exception as exc:
        err_body = json.dumps({
            "error": "FastAPI Execution Exception",
            "exception": str(exc),
            "traceback": traceback.format_exc(),
            "path": path
        }).encode('utf-8')
        await send({
            'type': 'http.response.start',
            'status': 500,
            'headers': [[b'content-type', b'application/json'], [b'content-length', str(len(err_body)).encode('utf-8')]]
        })
        await send({'type': 'http.response.body', 'body': err_body})

handler = app
