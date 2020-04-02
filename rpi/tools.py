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

import re
import time
import importlib
import urllib.request
import requests
from bs4 import BeautifulSoup

import os,sys,inspect
# workaround to import from sensor directory, sorry
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir+"/sensors")

# import BME680
import Si1145
import SMPWM01C


def load_config(path="config.cfg"):
    """Load the GPS coordinates and I2C sensor data for the raspberry pi, returning the result as a dictionary.

    Keyword Arguments:
        path {str} -- The path to the config file. (default: {"config.cfg"})

    Returns:
        dict -- Dictionary containing the raspberry pi configuration.
    """
    try:
        cfg_file = open(path, 'r', encoding="utf-8")
        device_id = cfg_file.readline().strip()
        gps_coords = cfg_file.readline().strip()
        # Match the first read line with a regular expression for valid GPS coordinates
        prog = re.match("^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$",
                        gps_coords)
        if not prog:
            raise ValueError

    except IOError as e:
        print("Incorrect file path, does the config file exist?\n")
        print(e)
        cfg_file.close()
        return
    except ValueError as e:
        print("Incorrect format for GPS coordinates! Are they there? Are they valid?")
        cfg_file.close()
        return
        

    # If valid, split coordinates into array and store in the dict
    config = [["device_id", device_id], ["gps_coords", gps_coords]]

    # For each sensor, read line and add to dict
    sensor_data = cfg_file.readline()
    while sensor_data != '':
        line = sensor_data.strip().split(',')
        if len(line) > 1:
            config.append([line[0], line[1]])
        sensor_data = cfg_file.readline()

    cfg_file.close()
    return config


def sensor_switch(sensor, address):
    """Switch statement for all compatible sensors. Input the sensor name and I2C address, it will return an object of that sensor.
    
    Arguments:
        sensor {str} -- String containing the name of the sensor.
        address {int} -- Integer representing the I2C address of the sensor.
    
    Returns:
        Object -- Object containing the sensor data.
    """
    sensor_dict = {
        # "BME680": BME680.create(address),
        "Si1145": Si1145.create(address),
        "SMPWM01C": SMPWM01C.create(address)
    }
    return sensor_dict.get(sensor)


def import_sensors(config):
    """Imports sensor libraries and sensor objects from a config file.
    
    Returns:
        [list, list] -- Two lists of modules and sensor objects.
    """
    sensorList = []
    for i, item in enumerate(config):
        if i in (0, 1):
            continue
        elif item[0][0] == "#":
            continue
        else:
            addr = int(item[1], 16)
            sensorList.append(sensor_switch(item[0], addr))
    return sensorList


def format_dict(dictList):
    """Takes in a list of dictionaries and returns a signle dictionary will all entries.
    
    Arguments:
        dictList {[dict]} -- List of dictionaries.
    
    Returns:
        dict -- Super dictionary.
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
        str -- Response code pertaining to data send.
    """
    response = requests.post(url, data=data)
    return response


def get_data_from_server(url):
    """Retrieves lines of text from a simple php or html file.
    
    Arguments:
        url {str} -- The required server url to download from.
    
    Returns:
        arr[str] -- Array containing text from website.
    """
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    # get text
    text = soup.get_text()
    text = text.split('\n')
    newText = []
    for line in text:
        if line != '':
            newText.append(line.strip())
    return newText


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
        return False
