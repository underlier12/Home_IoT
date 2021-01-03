from elasticsearch import Elasticsearch
from datetime import datetime

import json

class ElasticsearchModule:
    def __init__(self, index):
        self.es = Elasticsearch('localhost:29200')
        self.index = index

    def check_existing_index(self):
        if self.es.indices.exists(index=self.index):
            return True
        else:
            return False

    def make_index(self):
        with open("mapping.json", "r") as file:
            j_body = json.load(file)

        response = self.es.indices.create(
            index=self.index,
            # body=j_body
            body=j_body
        )
        print(response)

    def insert_info(self, list):
        info = {
            "timestamp": datetime.now(),
            "temperature": list[0],
            "humidity": list[1]
        }
        response = self.es.index(
            index=self.index,
            body=info
        )
        # print(response)
