__author__ = 'Pasha'

import mysql.connector
from mysql.connector import errorcode
from weather import Weather, Measurer

# TODO: rename this module into something like "mysql_datasource"

def connect():
    try:
        # TODO: move connection credentials to the application config file
        cnx = mysql.connector.connect(user='home_weather',
                                      password='oGKCMoEf7QjHOGwqCB4L',
                                      host='192.168.0.132',
                                      database='home_weather')
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with database user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exists")
        else:
            print(err)
    else:
        cnx.close()

def disconnect(connection):
    connection.close()

def get_weather_for_period(cnx, date_start, date_end, measurer_id):
    """
    Get all measurements in a specific period
        get_weather_for_period(cnx, date_start, date_end) -> list of Weather
    Keyword arguments:
        cnx -- connection used to get measurements
        date_start -- period start date
        date_end -- period end date
        measurer_id -- measurer identifier
    """
    cursor = cnx.cursor()

    query = ("SELECT temperature, humidity, measure_date FROM weather "
             "WHERE measurer_id=%s AND measure_date BETWEEN %s AND %s ORDER BY measure_date ASC")

    cursor.execute(query, (measurer_id, date_start, date_end))

    founded_measurements = []

    for (temperature, humidity, measure_date) in cursor:
        founded_measurements.append(Weather(temperature, humidity, measure_date))

    cursor.close()

    return founded_measurements

def write_weather(cnx, measurer_id, weather):
    """
    Write weather measurement to database.
    Keyword arguments:
        cnx -- connection used to write measurement
        weather -- Weather to store
        measurer_id -- measurer identifier who measured the specified weather
    """
    cursor = cnx.cursor()

    query = ("INSERT INTO weather (measurer_id, temperature, humidity)"
             "VALUES ({:d},{:.2f},{:.2f})")

    cursor.execute(query.format(measurer_id, weather.temperature, weather.humidity))
    cnx.commit()
    cursor.close()

def get_measurer_by_code(cnx, measurer_code):
    """
    Get measurer details by it's unique code.
    Keyword arguments:
        cnx -- connection used to write measurement
        measurer_code -- unique measurer code
    """
    cursor = cnx.cursor()
    query = "SELECT id, code, name, description FROM measurers ORDER BY name ASC"
    cursor.fetchone(query)
    measurer = Measurer(cursor.name, cursor.code, cursor.id, cursor.description)
    cursor.close()
    return measurer

def get_all_measurers(cnx):
    """
    Get all available temperature measurers.
    Keyword arguments:
        cnx -- connection used to write measurement
    """
    cursor = cnx.cursor()
    query = "SELECT id, code, name, description FROM measurers ORDER BY name ASC"
    cursor.execute(query)
    founded_measurers = []
    for (id, code, name, description) in cursor:
        founded_measurers.append(Measurer(name, code, id, description))
    cursor.close()
    return founded_measurers

def get_current_weather(cnx, measurer_id):
    """
    Get latest measurement for the specified measurer.
    Keyword arguments:
        cnx -- connection used to get weather
        measurer_id -- unique measurer identifier
    """
    cursor = cnx.cursor()
    query = "SELECT temperature, humidity, measure_date FROM weather WHERE measurer_id={:d} ORDER BY id DESC LIMIT 1"
    cursor.execute(query.format(measurer_id))
    row = cursor.fetchone()
    weather = Weather(row[0],row[1], row[2])
    cursor.close()
    return weather
