import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from flask import Flask
from flask_restful import Api

from views.orders import OrdersView
app = Flask(__name__)
api = Api(app)

api.add_resource(OrdersView, '/orders')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
