__author__ = 'Pasha'

import mysql.connector
from mysql.connector import errorcode
from mysql.connector import conversion
from weather import Weather, Measurer
import logging

# TODO: rename this module into something like "mysql_datasource"

cnx = None

def init(host, username, database, password):
    global cnx
    cnx = __connect__(host, username, database, password)

def __connect__(host, username, database, password):
    try:
        connection = mysql.connector.connect(username,password,host,database)
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error("Database communication error: access denied.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.error("Database communication error: database not exists.")
        else:
            logging.error("Database communication error: unknown error #" + err.errno)
    else:
        connection.close()

def disconnect():
    cnx.close()

def get_weather_for_period(date_start, date_end, measurer_id):
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

def write_weather(measurer_id, weather):
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

def get_measurer_by_code(measurer_code):
    """
    Get measurer details by it's unique code.
    Keyword arguments:
        cnx -- connection used to write measurement
        measurer_code -- unique measurer code
    """
    cursor = cnx.cursor()
    query = "SELECT id, code, name, description FROM measurers WHERE code='{:s}'"
    cursor.execute(query.format(conversion.MySQLConverter().escape(measurer_code)))
    row = cursor.fetchone()
    # TODO: check that row is not None, throw error otherwise (HTTP response with appropriate code)
    measurer = Measurer(row[2], row[1], row[0], row[3])
    cursor.close()
    return measurer

def get_all_measurers():
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

def add_measurer(measurer):
    """
    Add new measurer to database.
    Keyword arguments:
        cnx -- connection used to write measurement
        measurer -- Measurer to store
    """
    cursor = cnx.cursor()
    query = "INSERT INTO measurers (code, name, description) VALUES (%s, %s, %s)"
    cursor.execute(query, (measurer.code, measurer.name, measurer.description))
    measurer.id = cursor.lastrowid
    cnx.commit()
    cursor.close()
    return measurer

def get_current_weather(measurer_id):
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
