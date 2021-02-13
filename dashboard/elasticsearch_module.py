from elasticsearch import Elasticsearch
from datetime import datetime

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

    def determine_info(self, data):
        if len(data) == 2:
            info = {
                "timestamp": datetime.now(),
                "temperature": data[0],
                "humidity": data[1]
            }
        else:
            info = {
                "timestamp": datetime.now(),
                "electric": data[0],
                "water": data[1],
                "communic": data[2]
            }
        return info

    def insert_infos(self, name, info):
        info = self.determine_info(info)
        self.es.index(
            index=name,
            body=info
        )