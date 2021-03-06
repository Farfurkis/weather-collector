import xml.etree.ElementTree as ET
import urllib.request

weather_source_url = 'http://xml.weather.co.ua/1.2/forecast/23'
weather_ua_update_interval = 3600
weather_ua_plugin_code = None
weather_ua_plugin_name = None
weather_ua_plugin_description = None

def init(common_settings, specific_settings):
    # TODO: avoid using locals!
    global weather_source_url
    weather_source_url= specific_settings['url']
    global weather_ua_update_interval
    weather_ua_update_interval= common_settings['period']
    global weather_ua_plugin_code
    weather_ua_plugin_code = common_settings['id']
    global weather_ua_plugin_name
    weather_ua_plugin_name = common_settings['name']
    global weather_ua_plugin_description
    weather_ua_plugin_description = common_settings['description']

def provide_temperature_and_humidity():
    xml_stream = urllib.request.urlopen(weather_source_url)
    tree = ET.parse(xml_stream)
    root = tree.getroot()
    temperature = root.find("current/t").text
    humidity = root.find("current/h").text
    return [int(temperature), int(humidity)]

def get_update_interval():
    return weather_ua_update_interval

def code():
    return weather_ua_plugin_code

def name():
    return weather_ua_plugin_name

def description():
    return weather_ua_plugin_description