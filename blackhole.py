#!/usr/bin/env python

__author__ = "Adam Gautier"
__copyright__ = "Copyright 2022, All Rights Reserved"
__credits__ = ["Adam Gautier"]
__license__ = "None"
__version__ = "0.0.1"
__maintainer__ = "Adam Gautier"
__email__ = "adam@gautier.org"
__status__ = "Prototype"

from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse
import sys

RESPONSE_HTML = """
<html>
 <head>
  <title>Blackhole Server</title>
 </head>
 <body>
  <h1>Blackhole Server</h1>
  <hr/>
  <h2>Default Test Page</h2>
 </body>
</html>
"""

TEST_PATH="/blackhole/test"
TEST_DOMAINS=[]
HEADER_HOST="Host"

class html(BaseHTTPRequestHandler):

    def do_DEFAULT(self, verb):
        print(file=sys.stderr)
        keys = self.headers.keys()
        for key in keys:
            print("[H] %s: %s" % (key, self.headers.get(key)), file=sys.stderr)
            
        if (TEST_PATH == self.path) or (HEADER_HOST in keys and self.headers.get(HEADER_HOST) in TEST_DOMAINS):
            self.send_response (200)
            self.send_header ("Content-type", "text/html")
            self.send_header("Content-length", len(RESPONSE_HTML))
            self.end_headers ()
            self.wfile.write(bytes(RESPONSE_HTML, "utf8"))
            print("Test: %s %s" % (verb, self.path), file=sys.stderr)
            return
            
        if ("Host" in keys):
            print("Request: %s %s %s" % (verb, self.headers.get("Host"), self.path), file=sys.stderr)
        
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
        self.send_header("Connection", "close")
        self.end_headers ()
        if "HEAD" != verb:
            self.wfile.write(bytes("", "utf8"))
        

    def log_message(self, format, *args):
        pass
    
    def do_HEAD (self):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! UNHANDLED HEAD", file=sys.stderr)
        self.do_DEFAULT("HEAD")
        
    def do_POST (self):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! UNHANDLED POST", file=sys.stderr)
        self.do_DEFAULT("POST")
        
    def do_GET (self):
        self.do_DEFAULT("GET")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Blackhole Server - HTTP that returns valid but minimal null values.')
    parser.add_argument('--domains', default=None, help='Comma delimited list of fully qualified domain names that revert to testing responses')
    parser.add_argument('--host', default="0.0.0.0", help="Override the default host for the server to listen(0.0.0.0)")
    parser.add_argument('--port', default="8080", help="Override the default port for the server to listen(8080)")
    args = parser.parse_args()

    if args.domains is not None:
        TEST_DOMAINS = args.domains.split(",")
        
    with HTTPServer ((args.host, int(args.port)), html) as server:
        print("Blackhole Server listening: %s:%s" % (args.host, args.port), file=sys.stderr)
        print("Test domains:", file=sys.stderr)
        for domain in TEST_DOMAINS:
            print("- %s" % domain, file=sys.stderr)
        print("Test path: %s" % TEST_PATH, file=sys.stderr)
        print(" - - - - - - - - - - - - - - - - - - - - -", file=sys.stderr)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print(" - - - - - - - - - - - - - - - - - - - - -", file=sys.stderr)
            print("Blackhole Server shutdown", file=sys.stderr)
