"""Launch browser QA on a fresh temporary DB; never uses marketplace/data.
Run: python3 marketplace/qa/run-disposable.py
Requires Node, Playwright and Chrome (see browser-check.mjs overrides).
"""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='marketplace-browser-qa-') as directory:
    # Port 0 selects a free port; import server code without executing its CLI.
    sys.path.insert(0,str(root))
    from app import Store,Handler,ThreadingHTTPServer
    import threading
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    server.store=Store(Path(directory)/'qa.sqlite3')
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        result=subprocess.run(['node',str(root/'qa/browser-check.mjs')],env={**os.environ,
            'MARKETPLACE_URL':f'http://127.0.0.1:{server.server_port}','MARKETPLACE_QA_DISPOSABLE':'1'})
    finally:
        server.shutdown();server.server_close();thread.join()
    raise SystemExit(result.returncode)
