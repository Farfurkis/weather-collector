import threading
import imp
import os
import configparser
import mysql_weather_provider
import time
import signal
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
        time.sleep(float(period))

def sigterm_handler(signum, frame):
    print("Terminating...")
    for thread in threads:
        if thread.isAlive():
            try:
                thread._Thread__stop()
            except:
                print(str(thread.getName()) + ' could not be terminated')
    sys.exit()

def main():
    application_configuration = loadConfiguration('measurer-configuration.ini')
    plugins = loadPlugins(application_configuration['general']['plugins_directory'])
    threads = []
    i=2 # TODO: obtain real plugin "id" and use it instead of this counter
    for plugin_name in plugins:
        plugin = plugins.get(plugin_name)
        measurement_period = plugin.get_update_interval()
        measurer_thread = threading.Thread(target=store_weather_periodically,
                                       args=(i, plugin, measurement_period)
        )
        measurer_thread.setName(plugin_name)
        measurer_thread.start()
        threads.append(measurer_thread)
        i += 1
    signal.signal(signal.SIGTERM, sigterm_handler)

main()