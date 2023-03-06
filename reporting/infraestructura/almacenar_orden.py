import csv
import json
import os
from datetime import datetime

from google.protobuf.json_format import MessageToDict, MessageToJson


def create_report(order):
    print(order)
    version = os.environ.get('OLD_VERSION')
    if version:
        create_json(order)
    else:
        create_csv(order)


def create_csv(order):
    datos = MessageToDict(order)
    with open('./reporting/reports/result_{}.csv'.format(datos['id']), 'w') as file:
        writer = csv.writer(file)
        writer.writerow([datos['id'], datos['clientId'], datos['address'], datos['status'], datetime.fromtimestamp(datos['createdAt']), datos['service']])
    file.close()


def create_json(order):
    datos = MessageToJson(order)
    with open('./reporting/reports/result_{}.json'.format(datos['id']), 'w') as f:
        json.dump(datos, f)
