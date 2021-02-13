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

    def insert_info(self, name, list):
        info = {
            "timestamp": datetime.now(),
            "temperature": list[0],
            "humidity": list[1]
        }
        self.es.index(
            index=name,
            body=info
        )
        # print(response)

    def insert_infos(self, name, info):
        self.es.index(
            index=name,
            body=info
        )