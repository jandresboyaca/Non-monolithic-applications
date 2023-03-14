import os

from flask import Flask
from flask_restful import Api

from views.reports import ReportsView

app = Flask(__name__)
api = Api(app)

api.add_resource(ReportsView, '/report')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
