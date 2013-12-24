import threading
import imp
import os

# TODO: import plugins dynamically
# from plugins import dht22provider, weather_ua_provider

def loadPlugins():
    res = {}
    # check subfolders
    lst = os.listdir("plugins")
    dir = []
    for d in lst:
        s = os.path.abspath("plugins") + os.sep + d
        if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
            dir.append(d)
        # load the modules
    for d in dir:
        # if os.path.splitext(d)[1] == '.py':
        mod_name = "plugins." + d
        # res[d] = __import__("plugins." + d, fromlist = ["*"])
        filepath = os.path.abspath("plugins") + os.sep + d + os.sep + "weather_plugin.py"
        if os.path.exists(filepath):
            res[d] = imp.load_source(mod_name, filepath)
        else:
            print("Weather plugin initialization failed: 'weather_plugin.py' was not found in plugins" + os.sep + d + " folder!")
    return res

loadPlugins()

def store_dht22_weather_periodically():
    db_connection = mysql_weather_provider.connect()
    while True:
        temperature_and_humidity = dht22provider.provide_temperature_and_humidity()
        if temperature_and_humidity is None:
            print("Actual temperature obtaining error: measure result is 'None'")
        else:
            dht22_measured_weather = Weather(temperature_and_humidity[0], temperature_and_humidity[1])
            mysql_weather_provider.write_weather(db_connection, 2, dht22_measured_weather)
        time.sleep(60)

def store_weather_ua_weather_periodically():
    db_connection = mysql_weather_provider.connect()
    while True:
        temperature_and_humidity = weather_ua_provider.provide_temperature_and_humidity()
        if temperature_and_humidity is None:
            print("Actual temperature obtaining error: measure result is 'None'")
        else:
            weather_ua_measured_weather = Weather(temperature_and_humidity[0], temperature_and_humidity[1])
            mysql_weather_provider.write_weather(db_connection, 3, weather_ua_measured_weather)
        time.sleep(10)

# dht22thread = threading.Thread(target=store_dht22_weather_periodically)
# dht22thread.daemon = True
# dht22thread.start()
#
# weather_ua_thread = threading.Thread(target=store_weather_ua_weather_periodically)
# weather_ua_thread.daemon = True
# weather_ua_thread.start()
