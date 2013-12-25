__author__ = 'Pasha'

import mysql.connector
from mysql.connector import errorcode
from weather import Weather

# TODO: rename this module into something like "mysql_datasource"

def connect():
    try:
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
