import time
import json
import multiprocessing
from random import randint
from api import Api
from log import Logger
from helper import Helper
from constants import PidTypes
from constants import Units
from multiprocessing import Queue
from telemetry import Telemetry

class Main:

    def __init__(self):
        self._telemetryQueue = Queue()
        self._logQueue = Queue()
        self._api = Api()
        self._log = Logger()
        self._helper = Helper()

    def apiWorker(self):
        self._api.login()
        while not self._telemetryQueue.empty():
            self._api.send_telemetry(self._telemetryQueue.get())            

    def logWorker(self):
        while not self._logQueue.empty():
            self._log.send_telemetry(self._logQueue.get())

    def main(self):
        multiprocessing.Semaphore(2) 
        _worker = None
        _connectionFailureCount = 0
        _connected = False   

        commandDictionary = {
            PidTypes.SPEED: obd.commands.SPEED,
            PidTypes.FUEL_LEVEL: obd.commands.FUEL_LEVEL,
            PidTypes.RPM: obd.commands.RPM,
            PidTypes.MAF: obd.commands.MAF,
            PidTypes.RUN_TIME: obd.commands.RUN_TIME
        }

        while _connected == False:
            if (_connectionFailureCount > 0):
                time.sleep(randint(0, (2 ** _connectionFailureCount) - 1))
            try:
                ports = obd.scan_serial()
                connection = obd.OBD(ports[0])
                _connected = True
            except:
                _connectionFailureCount += 1

        while True and _connected == True:

            if self._helper.api_service_is_on() == True:
                _worker = multiprocessing.Process(target=self.apiWorker, args=())
            else:
                _worker = multiprocessing.Process(target=self.logWorker, args=())       
            
            _worker.start()

            speedForFuelConsumption = None
            mafForFuelConsumption = None
            timestampForFuelConsumption = None

            for key in commandDictionary:
                response = connection.query(commandDictionary[key], force=True)

                if response.value != None:
                    
                    digitResponse = self._helper.getNumberFromString(str(response.value))
                    if key == 1:
                        speedForFuelConsumption = digitResponse
                    if key == 4:
                        mafForFuelConsumption = digitResponse
                        timestampForFuelConsumption = response.time
                    
                    telemetry = Telemetry(key.name, digitResponse, Units(key.value).name, response.time)
                    self._telemetryQueue.put(telemetry)
                    self._logQueue.put(telemetry)

            if speedForFuelConsumption != None and mafForFuelConsumption != None and timestampForFuelConsumption != None:
                fuelConsumptionTelemetry = self._helper.calculateFuelConsumption(speedForFuelConsumption, mafForFuelConsumption, timestampForFuelConsumption)
                self._telemetryQueue.put(fuelConsumptionTelemetry)
                self._logQueue.put(fuelConsumptionTelemetry)

    def test(self):
        multiprocessing.Semaphore(1) 
        _worker = multiprocessing.Process(target=self.apiWorker, args=())                  
            
        with open("testSet.json") as file:
            telemetries = json.load(file)

        for telemetry in telemetries:
            self._telemetryQueue.put(Telemetry(telemetry['pidType'], telemetry['pidValue'], telemetry['unit'], telemetry['timestamp']))
        
        _worker.start()

if __name__ == "__main__":
    Main().test()
