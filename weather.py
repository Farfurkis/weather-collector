__author__ = 'Pasha'
from datetime import datetime
import json

class Weather:

    def __init__(self, temperature, humidity, datetime = datetime.today()):
        self.temperature = temperature
        self.humidity = humidity
        self.datetime = datetime

    def to_json(self):
        return json.dumps(
            {
                'temperature': str(self.temperature),
                'humidity': str(self.humidity),
                'datetime': self.datetime.isoformat()
            },
            sort_keys=False,
            indent=4,
            separators=(',', ': '))

class Measurer:

    def __init__(self, name, code, id, description):
        self.name = name
        self.code = code
        self.id = id
        self.description = description