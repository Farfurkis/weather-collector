__author__ = 'Pasha'

import dhtreader

dht_measurer_type = 22
dht_measurer_pin = 4
dht_measurer_update_interval = 60

def init(common_settings, specific_settings):
    global dht_measurer_type
    dht_measurer_type = int(specific_settings['type'])
    global dht_measurer_pin
    dht_measurer_pin = int(specific_settings['pin'])
    global dht_measurer_update_interval
    dht_measurer_update_interval = common_settings['period']

def provide_temperature_and_humidity():
    dhtreader.init()
    return dhtreader.read(dht_measurer_type, dht_measurer_pin)

def get_update_interval():
    return dht_measurer_update_interval