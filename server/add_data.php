<?php
// This function will run within each post array including multi-dimensional arrays
function ExtendedAddslash(&$params)
{
    foreach ($params as &$var) {
        // check if $var is an array. If yes, it will start another ExtendedAddslash() function to loop to each key inside.
        is_array($var) ? ExtendedAddslash($var) : $var=addslashes($var);
        unset($var);
    }
}

// Initialize ExtendedAddslash() function for every $_POST variable
ExtendedAddslash($_POST);

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


$device_id =$_POST['device_id'];
$location =$_POST['location'][0] .", ". $_POST['location'][1];
$time =$_POST['time'];
$temperature =$_POST['temperature'];
$humidity =$_POST['humidity'];
$pressure =$_POST['pressure'];
$uv_index =$_POST['uv_index'];

$db_host = 'localhost';
$db_username = 'raspberrypi';
$db_password = 'raspberry';
$db_name = 'climatedb';

$mysqli = new mysqli($db_host, $db_username, $db_password);

if($mysqli -> connect_errno) {
    echo "Failed to connect to MySQL: " . $mysqli -> connect_error;
    exit();
}

$mysqli -> select_db($db_name);

$sql = "INSERT INTO data ".
    "(device_id, time, temperature, humidity, pressure, uv_index)".
    "VALUES".
    "('$device_id', '$time', '$temperature', '$humidity', '$pressure', '$uv_index')";

if ($mysqli -> query($sql) == TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $mysqli -> error;
}

$mysqli ->close();
?>