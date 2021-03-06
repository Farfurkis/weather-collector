import time, signal, logging, threading, imp, os, configparser
import mysql_weather_provider
from weather import Weather, Measurer

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
        message = ("Loaded plugin configuration from the '" + d + "' folder"
              + ", author: " + common_settings['author']
              + ", version: " + common_settings['version']
              + ", plugin unique id: " + common_settings['id']
              + ", plugin name: " + common_settings['name']
        )
        print(message)
        logging.info(message)
        if common_settings['enabled'] == 'true':
            filepath = os.path.abspath(plugins_directory) + os.sep + d + os.sep + common_settings['init_file']
            if os.path.exists(filepath):
                res[d] = imp.load_source(mod_name, filepath)
                res[d].init(common_settings, specific_settings)
            else:
                logging.error("Weather plugin initialization failed: 'weather_ua_weather_plugin.py' was not found in "
                  + plugins_directory + os.sep + d + " folder!")
        else:
            logging.warning("Plugin '" + common_settings['name'] + "' is DISABLED and will not be loaded!")
    return res

def store_weather_periodically(measurer_id, measurement_provider, period):
    while True:
        sleep_period = float(period)
        temperature_and_humidity = measurement_provider.provide_temperature_and_humidity()
        if temperature_and_humidity is None:
            logging.warning("Actual temperature obtaining error: measure result is 'None', will retry in 10 sec...")
            sleep_period = 10
        else:
            measured_weather = Weather(temperature_and_humidity[0], temperature_and_humidity[1])
            logging.info("Measurement results from '" + measurement_provider.code()
                         + "' measurer: t=" + str(measured_weather.temperature)
                         + ", h=" + str(measured_weather.humidity))
            mysql_weather_provider.write_weather(measurer_id, measured_weather)
        time.sleep(sleep_period)

def sigterm_handler(signum, frame):
    logging.info("Terminating...")
    for thread in threads:
        if thread.isAlive():
            try:
                thread._Thread__stop()
            except:
                logging.error(str(thread.getName()) + ' could not be terminated')
    sys.exit()

def select_log_level(level_name):
    return {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
        }[level_name]

def init_logging(filename, log_level):
    numeric_level = getattr(logging, log_level.upper())
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        filename=filename,
                        level=numeric_level)


def main():
    application_configuration = loadConfiguration('measurer-configuration.ini')
    init_logging(application_configuration['general']['log_file'],application_configuration['general']['log_level'])
    mysql_configuration = application_configuration['mysql_database']
    mysql_weather_provider.init(mysql_configuration['host'],
                                mysql_configuration['username'],
                                mysql_configuration['database'],
                                mysql_configuration['password'])
    plugins = loadPlugins(application_configuration['general']['plugins_directory'])
    threads = []

    measurers = mysql_weather_provider.get_all_measurers()

    for plugin_name in plugins:
        plugin = plugins.get(plugin_name)
        measurement_period = plugin.get_update_interval()
        measurer_code = plugin.code()
        measurer_name = plugin.name()
        measurer_description = plugin.description()
        measurer_id = None
        for measurer in measurers:
            if measurer.code == measurer_code:
                measurer_id = measurer.id
                break

        if measurer_id is None:
            new_measurer = mysql_weather_provider.add_measurer(
                Measurer(measurer_name, measurer_code, None, measurer_description))
            measurer_id = new_measurer.id

        measurer_thread = threading.Thread(target=store_weather_periodically,
                                           args=(measurer_id, plugin, measurement_period)
        )
        measurer_thread.setName(plugin_name)
        measurer_thread.start()
        threads.append(measurer_thread)
    signal.signal(signal.SIGTERM, sigterm_handler)

    connection.close()
main()