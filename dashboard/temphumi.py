from AdafruitDHT import DHT
from elasticsearch_module import ElasticsearchModule

import sys

class Monitoring():
    def __init__(self):
        self.index_name = 'tempnhumi'
        # self.em = ElasticsearchModule(self.index_name)
        self.em = ElasticsearchModule()
        self.dht = DHT()

    def prerequisite(self, name):
        if not self.em.check_existing_index(name):
            self.em.make_index(self.index_name)
        else:
            print('Index exist already')

    def gathering(self):
        data = self.dht.transfer_data()
        self.em.insert_info(self.index_name, data)

def main(case):
    m = Monitoring()

    if case == 'p':
        m.prerequisite(m.index_name)
    elif case == 'g':
        m.gathering()
    else:
        print('Argument is not proper')

if __name__ == "__main__":
    main(sys.argv[1])