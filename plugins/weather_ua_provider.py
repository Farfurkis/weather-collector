import xml.etree.ElementTree as ET
import urllib.request

weather_source_url = 'http://xml.weather.co.ua/1.2/forecast/23'

def provide_temperature_and_humidity():
    xml_stream = urllib.request.urlopen(weather_source_url)
    tree = ET.parse(xml_stream)
    root = tree.getroot()
    temperature = root.find("current/t").text
    humidity = root.find("current/h").text
    return [int(temperature), int(humidity)]