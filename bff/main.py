import os
import sys
from urllib.parse import urljoin

import requests

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from flask import Flask, request
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

def gateway(path, url_reporting):
    target_url = url_reporting
    target_url = urljoin(target_url, path)
    query_params = request.query_string.decode('utf-8')
    if query_params:
        target_url = urljoin(target_url, '?' + query_params)
    print(target_url)
    req = requests.request(
        method=request.method,
        url=target_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    headers = [(key, value) for (key, value) in req.headers.items()
               if key not in ['Content-Length', 'Transfer-Encoding', 'Content-Encoding', 'Connection']]
    response = app.make_response((req.content, req.status_code, headers))
    return response

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET'])
def bff_report(path):
    url_reporting = os.environ.get("REPORTING_URL", "http://localhost/")
    return gateway(path, url_reporting)





@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['POST'])
def bff_orders(path):
    url_reporting = os.environ.get("ORDER_URL", "http://localhost:81/")
    return gateway(path, url_reporting)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
