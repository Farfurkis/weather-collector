import threading

# TODO: import providers dynamically
from plugins import dht22provider, weather_ua_provider


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

dht22thread = threading.Thread(target=store_dht22_weather_periodically)
dht22thread.daemon = True
dht22thread.start()

weather_ua_thread = threading.Thread(target=store_weather_ua_weather_periodically)
weather_ua_thread.daemon = True
weather_ua_thread.start()
