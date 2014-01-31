weather-collector
=================

A simple python application which collects temperature and humidity measurements statistics and can provide it via JSON API or simple web page.

Requirements
============

* Python 3.3.x with the follow modules:
  * Flask 0.10 (http://flask.pocoo.org/)
  * MySQL (http://dev.mysql.com/downloads/connector/python/)
* MySQL database as a storage

Plugins requirements
====================

dht_22
------

* DHT11 or DHT22 sensor connected to your Raspberry Pi

Useful links:
* DHT-11 sensor datasheet (http://www.micro4you.com/files/sensor/DHT11.pdf)
* DHT-22 (https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf)
* Adafruit sensor driver (https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_DHT_Driver_Python)
* The same driver modified to be compatible with Python 3 (https://github.com/Farfurkis/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_DHT_Driver_Python)

weather_ua
----------

* http access to the Weather.ua (http://www.weather.ua/) web site
