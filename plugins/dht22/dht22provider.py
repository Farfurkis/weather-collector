__author__ = 'Pasha'

import dhtreader

dht_measurer_type = 22
dht_measurer_pin = 4
dht_measurer_update_interval = 60
dht_plugin_code = None
dht_plugin_name = None
dht_plugin_description = None

def init(common_settings, specific_settings):
    global dht_measurer_type
    dht_measurer_type = int(specific_settings['type'])
    global dht_measurer_pin
    dht_measurer_pin = int(specific_settings['pin'])
    global dht_measurer_update_interval
    dht_measurer_update_interval = common_settings['period']
    global dht_plugin_code
    dht_plugin_code = common_settings['id']
    global dht_plugin_name
    dht_plugin_name = common_settings['name']
    global dht_plugin_description
    dht_plugin_description = common_settings['description']

def provide_temperature_and_humidity():
    dhtreader.init()
    return dhtreader.read(dht_measurer_type, dht_measurer_pin)

def get_update_interval():
    return dht_measurer_update_interval

def code():
    return dht_plugin_code

def name():
    return dht_plugin_name

def description():
    return dht_plugin_description