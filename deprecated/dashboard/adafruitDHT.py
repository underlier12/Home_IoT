import time
import board
import adafruit_dht
import argparse

from datetime import datetime
from elasticsearch_module import ElasticsearchModule

class DHT():
    def __init__(self):
        self.dhtDevice = adafruit_dht.DHT22(board.D4)

    def measuring(self):
        try:
            # Print the values to the serial port
            temperature_c = self.dhtDevice.temperature
            # temperature_f = temperature_c * (9 / 5) + 32
            humidity = self.dhtDevice.humidity
            return [temperature_c, humidity]

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            
        except Exception as error:
            self.dhtDevice.exit()
            raise error

    def transfer_data(self):
        for _ in range(5):
            data = self.measuring()
            if data:
                return data
            else:
                time.sleep(1)

def main():
    dht = DHT()
    em = ElasticsearchModule()
    INDEX_NAME = 'tempnhumi'

    data = dht.transfer_data()
    if data:
        em.insert_infos(INDEX_NAME, data)
    else:
        print('Data is not measured')

if __name__ == "__main__":
    main()