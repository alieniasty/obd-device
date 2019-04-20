import json
import requests
import multiprocessing
from time import gmtime, strftime

# ./ngrok http -host-header=localhost 50450
class Api:  
    _token = None

    def __init__(self):
        multiprocessing.Lock()
        with open('config.json') as configFile:
            self.config = json.load(configFile)

    def login(self):  
        if Api._token != None:
            return

        url = f"{self.config['baseApiUrl']}auth/login"

        body = {}
        body['Username'] = f"{self.config['username']}"
        body['Password'] = f"{self.config['password']}"

        payload = json.dumps(body)
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        Api._token = response.text
    
    def send_telemetry(self, telemetry):
        url = f"{self.config['baseApiUrl']}telemetry"

        body = {}
        body['deviceId'] = f"{self.config['deviceId']}"
        body['pidType'] = telemetry._pidType
        body['pidValue'] = telemetry._pidValue
        body['unit'] = telemetry._unit
        body['timestamp'] = telemetry._timestamp

        payload = json.dumps(body)
        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {Api._token}",
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)




   

