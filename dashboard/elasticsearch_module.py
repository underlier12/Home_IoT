from elasticsearch import Elasticsearch
from dateutil.relativedelta import relativedelta

import datetime
import json

class ElasticsearchModule:
    def __init__(self):
        self.es = Elasticsearch('localhost:29200')
        # self.index = index

    def check_existing_index(self, name):
        if self.es.indices.exists(index=name):
            return True
        else:
            return False

    def make_index(self, name):
        title = "mapping_" + name + ".json"
        with open(title, "r") as file:
            j_body = json.load(file)

        response = self.es.indices.create(
            index=name,
            body=j_body
        )
        print(response)

    def determine_info(self, data, target=None):
        if len(data) == 2:
            info = {
                "timestamp": datetime.datetime.now(),
                "temperature": data[0],
                "humidity": data[1]
            }
        else:
            if not target:
                record_day = \
                    datetime.datetime.now() - relativedelta(months=1)
            else:
                record_day = \
                    datetime.date(int(target[0]), int(target[1]), 1)
            info = {
                "timestamp": record_day,
                "electric": data[0],
                "water": data[1],
                "communic": data[2]
            }
        return info

    def insert_infos(self, name, info, target=None):
        info = self.determine_info(info, target)
        self.es.index(
            index=name,
            body=info
        )