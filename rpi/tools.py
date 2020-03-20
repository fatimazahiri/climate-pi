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
import urllib.request
from bs4 import BeautifulSoup


def load_config(path="config.cfg"):
    """Load the GPS coordinates and I2C sensor data for the raspberry pi, returning the result as a dictionary.

    Keyword Arguments:
        path {str} -- The path to the config file. (default: {"config.cfg"})

    Returns:
        dict -- Dictionary containing the raspberry pi configuration.
    """
    try:
        cfg_file = open(path, 'r', encoding="utf-8")
        gps_coords = cfg_file.readline().strip()
        # Match the first read line with a regular expression for valid GPS coordinates
        prog = re.match("^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$",
                        gps_coords)
        if not prog:
            raise ValueError

    except IOError as e:
        print("Incorrect file path, does the config file exist?\n")
        print(e)
    except ValueError as e:
        print("Incorrect format for GPS coordinates! Are they there? Are they valid?")
    finally:
        cfg_file.close()
        return

    # If valid, split coordinates into array and store in the dict
    config = {"gps_coords": gps_coords.split(',')}

    # For each sensor, read line and add to dict
    sensor_data = cfg_file.readline()
    while sensor_data != '':
        line = sensor_data.strip().split(',')
        if len(line) > 1:
            config[line[0]] = line[1]
        elif len(line) == 1:
            config[line[0]] = None
        sensor_data = cfg_file.readline()

    cfg_file.close()
    return config


def format_array():
    pass


def send_data_to_server(url):
    pass


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
