import os
import sys

from flask import send_file, request
# Flask
from flask_restful import Resource

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


class ReportsView(Resource):

    def get(self):
        report_id = request.args.get('id')
        version = os.environ.get('OLD_VERSION')
        if version:
            return send_file('reports/result_{}.json'.format(report_id))
        else:
            return send_file('reports/result_{}.csv'.format(report_id))


