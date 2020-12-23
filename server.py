#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    
    def load_binary(self, path):
        with open(path, 'rb') as file:
            return file.read()

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        
        # Send headers
        self.send_header('Content-type','image/png')
        self.end_headers()
        
        # Write content as utf-8 data
        self.wfile.write(self.load_binary('/opt/pixel/pixel.png'))
        return

def run():
    print('starting server...')
    server_address = ('0.0.0.0', 80)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()

run()
