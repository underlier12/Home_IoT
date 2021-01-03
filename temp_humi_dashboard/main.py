from AdafruitDHT import DHT
from ElasticsearchModule import ElasticsearchModule

import sys

class Monitoring():
    def __init__(self):
        self.index_name = 'tempnhumi'
        self.em = ElasticsearchModule(self.index_name)
        self.dht = DHT()

    def prerequisite(self):
        if self.em.check_existing_index():
            self.em.make_index()
        else:
            print('index exist already')

    def gathering(self):
        for _ in range(5):
            data = self.dht.transfer_data()
            self.em.insert_info(data)

def main(case):
    m = Monitoring()

    if case == 'p':
        m.prerequisite()
    elif case == 'g':
        m.gathering()
    else:
        print('argument is not proper')

if __name__ == "__main__":
    main(sys.argv[1])