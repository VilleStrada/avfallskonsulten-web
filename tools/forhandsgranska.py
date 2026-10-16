"""Lokal förhandsgranskning av docs/ som härmar GitHub Pages:
/hamta-grovsopor-stockholm  ->  docs/hamta-grovsopor-stockholm.html
okänd adress                ->  docs/404.html med status 404
Sajten visas både på http://localhost:8765/ och http://localhost:8765/avfallskonsulten-web/
Kör: python tools/forhandsgranska.py [port]
"""
import http.server, os, sys, urllib.parse
ROT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
PREFIX = "/avfallskonsulten-web"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROT, **k)
    def translate_path(self, path):
        path = urllib.parse.urlparse(path).path
        if path.startswith(PREFIX + "/") or path == PREFIX:
            path = path[len(PREFIX):] or "/"
        p = super().translate_path(path)
        if os.path.isdir(p):
            return os.path.join(p, "index.html")
        if not os.path.exists(p) and os.path.exists(p + ".html"):
            return p + ".html"
        return p
    def send_error(self, code, message=None, explain=None):
        if code == 404 and os.path.exists(os.path.join(ROT, "404.html")):
            body = open(os.path.join(ROT, "404.html"), "rb").read()
            self.send_response(404); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
            return
        super().send_error(code, message, explain)
    def log_message(self, *a):
        pass

print(f"Förhandsgranskning: http://localhost:{PORT}/  och  http://localhost:{PORT}{PREFIX}/   (Ctrl+C avslutar)")
http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
