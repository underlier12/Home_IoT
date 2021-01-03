import time
import board
import adafruit_dht

class DHT():
    def __init__(self):
        self.dhtDevice = adafruit_dht.DHT11(board.D4)

    def measuring(self):
        try:
            # Print the values to the serial port
            temperature_c = self.dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = self.dhtDevice.humidity
            print(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )
            )
            return [temperature_c, humidity]

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            
        except Exception as error:
            self.dhtDevice.exit()
            raise error

    def transfer_data(self):
        data = []
        while not data:
            data = self.measuring()
            time.sleep(1)
        return data
