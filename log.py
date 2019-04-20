import json

class Logger():

    def send_telemetry(self, telemetry):
        body = {}
        body['pidType'] = telemetry._pidType
        body['pidValue'] = telemetry._pidValue
        body['unit'] = telemetry._unit
        body['timestamp'] = telemetry._timestamp

        payload = json.dumps(body)

        print(payload)