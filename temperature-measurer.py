import threading
import imp
import os
import configparser
import mysql_weather_provider
import time
from weather import Weather

def loadConfiguration(path_to_configuration_file):
    config = configparser.ConfigParser()
    config.read(os.path.abspath(path_to_configuration_file))
    return config

def loadPlugins(plugins_directory):
    res = {}
    lst = os.listdir(plugins_directory)
    dir = []
    for d in lst:
        s = os.path.abspath(plugins_directory) + os.sep + d
        if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
            dir.append(d)
        # load the modules
    for d in dir:
        mod_name = "plugins." + d
        # load plugin configuration
        plugin_configuration = loadConfiguration(plugins_directory + os.sep + d + os.sep + "configuration.ini")
        common_settings = plugin_configuration['common_settings']
        specific_settings = plugin_configuration['specific_settings']
        description = plugin_configuration['description']
        print("Loaded plugin configuration from the '" + d + "' folder"
              + ", author: " + description['author']
              + ", version: " + description['version']
              + ", plugin unique id: " + description['id']
              + ", plugin name: " + description['name']
        )
        if common_settings['enabled'] == 'true':
            filepath = os.path.abspath(plugins_directory) + os.sep + d + os.sep + common_settings['init_file']
            if os.path.exists(filepath):
                res[d] = imp.load_source(mod_name, filepath)
                res[d].init(common_settings, specific_settings)
            else:
                print("Weather plugin initialization failed: 'weather_ua_weather_plugin.py' was not found in "
                  + plugins_directory + os.sep + d + " folder!")
        else:
            print("Plugin '" + description['name'] + "' is DISABLED and will not be loaded!")
    return res

def store_weather_periodically(measurer_id, measurement_provider, period):
    # TODO: rework "db_connection" into some abstract data storage
    db_connection = mysql_weather_provider.connect()
    while True:
        temperature_and_humidity = measurement_provider.provide_temperature_and_humidity()
        if temperature_and_humidity is None:
            print("Actual temperature obtaining error: measure result is 'None'")
        else:
            measured_weather = Weather(temperature_and_humidity[0], temperature_and_humidity[1])
            mysql_weather_provider.write_weather(db_connection, measurer_id, measured_weather)
        time.sleep(period)

application_configuration = loadConfiguration('measurer-configuration.ini')
plugins = loadPlugins(application_configuration['general']['plugins_directory'])
i=2 # TODO: obtain real plugin "id" and use it instead of this counter
for plugin_name in plugins:
    plugin = plugins.get(plugin_name)
    measurement_period = plugin.get_update_interval()
    measurer_thread = threading.Thread(target=store_weather_periodically,
                                   args=(i, plugin, measurement_period)
    )
    measurer_thread.daemon = True
    measurer_thread.start()
    i += 1

# TODO: investigate why the script exits just after the initialization?

#
# def store_dht22_weather_periodically():
#     db_connection = mysql_weather_provider.connect()
#     while True:
#         temperature_and_humidity = dht22provider.provide_temperature_and_humidity()
#         if temperature_and_humidity is None:
#             print("Actual temperature obtaining error: measure result is 'None'")
#         else:
#             dht22_measured_weather = Weather(temperature_and_humidity[0], temperature_and_humidity[1])
#             mysql_weather_provider.write_weather(db_connection, 2, dht22_measured_weather)
#         time.sleep(60)
#
# def store_weather_ua_weather_periodically():
#     db_connection = mysql_weather_provider.connect()
#     while True:
#         temperature_and_humidity = weather_ua_provider.provide_temperature_and_humidity()
#         if temperature_and_humidity is None:
#             print("Actual temperature obtaining error: measure result is 'None'")
#         else:
#             weather_ua_measured_weather = Weather(temperature_and_humidity[0], temperature_and_humidity[1])
#             mysql_weather_provider.write_weather(db_connection, 3, weather_ua_measured_weather)
#         time.sleep(10)

# dht22thread = threading.Thread(target=store_dht22_weather_periodically)
# dht22thread.daemon = True
# dht22thread.start()
#
# weather_ua_thread = threading.Thread(target=store_weather_ua_weather_periodically)
# weather_ua_thread.daemon = True
# weather_ua_thread.start()
