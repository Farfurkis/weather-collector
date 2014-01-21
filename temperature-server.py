from flask import Flask, render_template, make_response
from weather import Weather
import time
from functools import wraps
import mysql_weather_provider

#app = Flask(__name__)
# Flask debugging problem fix: http://librelist.com/browser//flask/2013/9/18/problem-debugging-flask-under-python-3-3/
app = Flask(__name__, instance_path=r'c:\Program Files\Python33\Lib\site-packages\flask')

def add_response_headers(headers={}):
    """This decorator adds the headers passed in to the response"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator

def html_response(f):
    return add_response_headers({'Content-Type': 'text/html;charset=utf-8'})(f)

def json_response(f):
    return add_response_headers({'Content-Type': 'application/json;charset=utf-8'})(f)



@app.route('/')
@html_response
def welcome():
    current_weather = Weather(15, 75)
    return render_template('main.html', temperature=current_weather.temperature, humidity=current_weather.humidity)

def measurers_to_json(measurers):
    result = '{"measurers":['
    for item in measurers:
        result += (item.to_json() + ',')
    result = result[:-1]
    result += ']}'
    return result

@app.route('/measurers')
@json_response
def all_measurers():
    """
    Get measurers list.
    """
    connection = mysql_weather_provider.connect()
    measurements = mysql_weather_provider.get_all_measurers(connection)
    mysql_weather_provider.disconnect(connection)
    return measurers_to_json(measurements)

@app.route('/temperature/current')
@json_response
def current_temperature():
    """
    Get last measured temperature.
    """
    current_weather = Weather(15, 75)
    return current_weather.to_json()

def weather_measurements_to_json(measurements):
    result = '{"measurements":['
    for item in measurements:
        result += (item.to_json() + ',')
    result = result[:-1]
    result += ']}'
    return result

@app.route('/temperature/period/<details_level>/<date_time_from>/<date_time_to>/<measurer_id>')
@json_response
def period_temperature(details_level, date_time_from, date_time_to, measurer_id):
    """
    Get measured temperature for a specific period
         details_level - group results and calculate average temperature for each period, possible values:
            'ten_minutes' - the 6 results for a hour will be returned: 0-10, 10-20, ... , 50-60
            'fifteen_minutes' - the 4 results for a hour will be returned: 0-15, 15-30, 30-45 and 45-60
            'half_a_hour' - the two results for a hour will be returned: 0-30 and 30-60
            'hour' - average hourly temperature will be returned
            'three_hours' - average temperature for each 3h will be returned
            'daily' - average daily temperature will be returned

    """
    # 22-06-2012T12:10:20
    pattern = '%d-%m-%YT%H:%M:%S'
    date_from = time.strptime(date_time_from, pattern)
    date_to = time.strptime(date_time_to, pattern)
    connection = mysql_weather_provider.connect()
    measurements = mysql_weather_provider.get_weather_for_period(connection, date_from, date_to, measurer_id)
    mysql_weather_provider.disconnect(connection)
    return weather_measurements_to_json(measurements)

@app.route('/write_weather/<temperature>/<humidity>')
def write_weather(temperature, humidity):
    """
    Store test measurement to database.
    """
    connection = mysql_weather_provider.connect()
    weather = Weather(float(temperature), float(humidity))
    # 0 - Test measurer
    mysql_weather_provider.write_weather(connection, 0, weather)
    mysql_weather_provider.disconnect(connection)
    return "Weather written!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
