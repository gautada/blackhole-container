from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

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
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    print(request.headers)
    return HTMLResponse(content=RESPONSE_HTML, status_code=200)
    # print(request.client.host) # testclient
    # print(request.client.port) # 50000
    # return {"message": "Hello World"}


