__author__ = 'Pasha'

import dhtreader

type = 22
pin = 4

def provide_temperature_and_humidity():
    dhtreader.init()
    return dhtreader.read(type, pin)