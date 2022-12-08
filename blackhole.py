# from typing import Union
#
# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
#
# app = FastAPI()
#
RESPONSE_HTML = """
<html>
 <head>
  <title>Blackhole Server</title>
 </head>
 <body>
  <b>Blackhole Server</b>
 </body>
</html>
"""
# @app.get("/{path}", response_class=HTMLResponse)
# def read_root(request: Request):
#     print(request.headers)
#     print(request.headers['host'])
#     return HTMLResponse(content=RESPONSE_HTML, status_code=200)
#     # print(request.client.host) # testclient
#     # print(request.client.port) # 50000
#     # return {"message": "Hello World"}


from http.server import BaseHTTPRequestHandler, HTTPServer

class html(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
        
    def do_GET (self):
        print(self.headers)
        keys = self.headers.keys()
        
        for key in keys:
            print("%s: %s" % (key, self.headers.get("Host")), file=sys.stderr)
            
        print("GET", end=" ", file=sys.stderr)
        if ("Host" in keys):
            print("%s: %s" % (self.headers.get("Host"), self.path), file=sys.stderr)
        
        mime="text/html"
        if ("Accept" in keys):
            mimes = self.headers.get("Accept")
            mime = mimes.split(",")[0]
            
        encoding=None
        if ("Accept-Encoding" in keys):
            encodings = self.headers.get("Accept-Encoding")
            encoding = mimes.split(",")[0]
            
        self.send_response (200)
        self.send_header ("Content-type", mime)
        self.send_header("Content-length", 0)
        if encoding is not None:
            self.send_header("Content-Encoding", encoding)
            
        self.end_headers ()
        self.wfile.write(bytes("", "utf8"))

    

with HTTPServer (('0.0.0.0', 8080), html) as server:
    print("Serving...")
    server.serve_forever ()
