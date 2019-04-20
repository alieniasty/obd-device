import json
import requests
from telemetry import Telemetry
import time
from random import randint


class Helper:

    def __init__(self):
        with open('config.json') as configFile:
            self.config = json.load(configFile)
            self._apiUrl = f"{self.config['baseApiUrl']}health"

    def api_service_is_on(self, timeout=1):
        try:
            response = requests.get(self._apiUrl, timeout=timeout)
            if response.status_code == 200:
                return True
        except:
            return False

    def calculateFuelConsumption(self, speed, maf, timestamp):
        mpg = (14.7 * 6.17 * 454 * speed * 0.621371) / (3600 * maf)  # DRIVER’S EFFICIENCY ANALYZER
        litersPer100km = 282.5/mpg
        return Telemetry("CONSUMPTION", litersPer100km, "liters_per_100_kilometers", timestamp)

    def getNumberFromString(self, responseValue):
        if not responseValue and not isinstance(responseValue, str):
            return 0
        out_number = []
        for ele in responseValue:
            if (ele == '.' and '.' not in out_number and ele != ' ') or ele.isdigit():
                out_number.append(ele)
            elif out_number:
                break
        return float(''.join(out_number))
