"""Loopback-only photo booth. No upload API; photos remain in the browser."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote
import threading
import webbrowser
from update_frames import update, ROOT
PORT=8765
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(ROOT),**kwargs)
    def do_GET(self):
        route=unquote(urlsplit(self.path).path)
        if route=='/frames.json':
            try: update()
            except Exception:
                self.send_error(500,'Could not update frames.json. Check JSON and folder permissions.');return
        allowed=route in ('/','/index.html','/frames.json','/assets/studio.js','/assets/studio.css') or route.startswith('/assets/frames/')
        target=Path(self.translate_path(self.path)).resolve()
        if not allowed or not target.is_relative_to(ROOT.resolve()) or (route!='/' and not target.is_file()):
            self.send_error(404);return
        super().do_GET()
    def end_headers(self):
        self.send_header('Cache-Control','no-store')
        super().end_headers()
def main():
    try:
        update()
        server=ThreadingHTTPServer(('127.0.0.1',PORT),Handler)
    except Exception as exc:
        print('起動できませんでした:',exc)
        print('別の起動ウィンドウがあれば、そちらを利用するか終了してください。')
        return
    url=f'http://127.0.0.1:{PORT}/'
    print('PHOTO STUDIO:',url,flush=True)
    print('使用中はこの画面を開いたままにしてください。終了は Control+C。',flush=True)
    threading.Timer(.6,lambda:webbrowser.open(url)).start()
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
if __name__=='__main__': main()
