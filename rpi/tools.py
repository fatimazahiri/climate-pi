#!/usr/bin/python3

# Copyright (C) 2020  Connor Czarnuch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import hashlib
import json
import os
import re
import sys
import time

import requests
from gpiozero import LED

# workaround to import from sensor directory, sorry
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir+"/sensors")

import BME680
import Si1145
import SMPWM01C

error_led = LED(17)


def load_config(path="config.json"):
    """Load the GPS coordinates and I2C sensor data for the raspberry pi, returning the result as a dictionary.

    Keyword Arguments:
        path {str} -- The path to the config file. (default: {"config.cfg"})

    Returns:
        dict -- Dictionary containing the raspberry pi configuration.
    """
    try:
        with open(path, 'r') as cfg_file:
            data = json.load(cfg_file)
            device_id = data["device_id"]
            passkey = data["passkey"]
            latitude = data["latitude"]
            longitude = data["longitude"]
            # Validate config
            device_id_check = 0 <= device_id <= 99999
            passkey_check = len(passkey) == 16 and re.match(
                r"[a-zA-Z0-9]+$", passkey)
            lat_check = -90 <= latitude <= 90
            long_check = -180 <= longitude <= 180
            if not device_id_check or not passkey_check or not lat_check or not long_check:
                raise ValueError

            # Format config entries
            device_id = ("%05d" % device_id)
            passkey_hash = hashlib.sha256(passkey.encode("UTF-8")).hexdigest()
            latitude = ("%.6f" % latitude)
            longitude = ("%.6f" % longitude)

            # If valid, split coordinates into array and store in the dict
            config = {
                "device_id": device_id,
                "passkey_hash": passkey_hash,
                "latitude": latitude,
                "longitude": longitude
            }

            # For each sensor, read line and add to dict
            sensor_data = data["sensors"]
            for sensor in sensor_data:
                config.update({sensor["name"]: sensor["address"]})

            return config

    except IOError as e:
        print("Incorrect file path, does the config file exist?\n")
        print(e)
        error_handler()
    except ValueError as e:
        print("Incorrect format for device_id or GPS coordinates! Are they there? Are they valid?")
        error_handler()


def sensor_switch(sensor, address):
    """Switch statement for all compatible sensors. Input the sensor name and I2C address, it will return an object of that sensor.

    Arguments:
        sensor {str} -- String containing the name of the sensor.
        address {int} -- Integer representing the I2C address of the sensor.

    Returns:
        sensor -- Object containing the sensor data.
    """
    sensor_dict = {
        "BME680": BME680,
        "Si1145": Si1145,
        "SMPWM01C": SMPWM01C
    }
    sensor = sensor_dict.get(sensor)
    return sensor.create(address)


def import_sensors(config):
    """Imports sensor libraries and sensor objects from a config file.

    Returns:
        list of sensor -- List containing sensor objects from config file.
    """
    sensorList = []
    for key in config.keys():
        if key in ("device_id", "passkey_hash", "latitude", "longitude"):
            continue
        else:
            addr = int(config[key], 16)
            sensorList.append(sensor_switch(key, addr))
    return sensorList


def format_dict(dictList):
    """Takes in a list of dictionaries and returns a signle dictionary will all entries.

    Arguments:
        dictList {[dict]} -- List of dictionaries.

    Returns:
        dict -- Combined dictionary.
    """
    newDict = {}
    for i in dictList:
        newDict.update(i)
    return newDict


def send_data_to_server(url, data):
    """Send post data to server at url.

    Arguments:
        url {str} -- The url to send data object to.
        data {dict} -- Dictionary containing keys and values to send to server.

    Returns:
        str -- Response code pertaining to data sent.
    """
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("Unable to send data to server ")
        error_handler()
    return response.text


def force_sync_time(unix_time):
    """Set the raspberry time to the unix time given as parameter.

    Arguments:
        unix_time {str} -- The unix time to set the raspberry pi to. Unix time is given in seconds since January 1, 1970.

    Returns:
        bool -- Returns false if the time was unable to be set.
    """
    try:
        clk_id = time.CLOCK_REALTIME
        time.clock_settime(clk_id, float(unix_time))
    except Exception as e:
        print("Unable to set clock time.")
        print(e)
        error_handler()


def error_handler():
    """LED on at error."""
    error_led.on()
    while True:
        pass
