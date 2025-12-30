from pathlib import Path
from urllib.parse import urlparse
from ._libxiangqi import Board as _Board
from ._libxiangqi import IllegalMove as IllegalMove


class Board:
  def __init__(self):
    self._b = _Board()

  def make_move(self, *x):
    self._b.make_move(*x)

  @property
  def turn(self):
    return self._b.turn()

  def __repr__(self) -> str:
    return self._b.ascii()

  def serve(self, port: int = 9999):
    from http.server import BaseHTTPRequestHandler
    from socketserver import TCPServer
    import json
    import os

    STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

    class TCPServerWithReuse(TCPServer):
      allow_reuse_address = True

      def __init__(self, server_address, RequestHandlerClass):
        print(f"started server on http://127.0.0.1:{server_address[1]}")
        super().__init__(server_address, RequestHandlerClass)

    class Handler(BaseHTTPRequestHandler):
      def send_data(self, data: bytes, content_type: str = "application/json", status_code: int = 200):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        return self.wfile.write(data)

      def do_GET(self):
        url = urlparse(self.path)
        match url.path:
          case "/" | "/index.html":
            with open(os.path.join(STATIC_DIR, "index.html"), "rb") as f:
              ret = f.read()
            self.send_data(ret, "text/html", 200)

          case path if path.startswith(("/assets/", "/js/", "/img/")) and "/.." not in path:
            try:
              with open(os.path.join(STATIC_DIR, self.path.strip("/")), "rb") as f:
                ret = f.read()
              if url.path.endswith(".js"):
                content_type = "application/javascript"
              if url.path.endswith(".css"):
                content_type = "text/css"
              if url.path.endswith(".svg"):
                content_type = "image/svg+xml"
              status_code = 200
            except FileNotFoundError:
              status_code = 404
            self.send_data(ret, content_type, status_code)

          case _:
            self.send_response(404)
            self.end_headers()

      def do_POST(self):
        url = urlparse(self.path)
        match url.path:
          case "/move":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
              move_data = json.loads(body.decode())
              print(f"Move received: {move_data}")

              response = {"status": "ok", "valid": True}
              ret = json.dumps(response).encode()
              self.send_data(ret, "application/json", 200)
            except Exception as e:
              print(f"Error processing move: {e}")
              response = {"status": "error", "message": str(e)}
              ret = json.dumps(response).encode()
              self.send_data(ret, "application/json", 400)

          case _:
            self.send_response(404)
            self.end_headers()

    server = TCPServerWithReuse(("", port), Handler)
    try:
      server.serve_forever(poll_interval=0.1)
    except KeyboardInterrupt:
      print("libxiangqi server shutdown...")
