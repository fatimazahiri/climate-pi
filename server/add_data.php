<?php
// Copyright (C) 2020  Connor Czarnuch

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.


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

$device_id =$_POST['device_id'];
$passkey_hash =$_POST['passkey_hash'];
$time =$_POST['time'];
$temperature =$_POST['temperature'];
$humidity =$_POST['humidity'];
$pressure =$_POST['pressure'];
$gas =$_POST['gas'];
$uv_index =$_POST['uv_index'];
$pm_25 =$_POST['pm_25'];
$pm_10 =$_POST['pm_10'];

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

$rows = $mysqli -> query("SELECT * FROM device WHERE device_id = '$device_id' AND passkey_hash = '$passkey_hash'");
if ($rows->num_rows > 0) {
    echo("Passkey match, proceed to insert.");
} else {
    echo("Passkey does not match or device does not exist.");
}

$device_str = "device_id, passkey_hash, time";
$data_str = "'$device_id', '$passkey_hash', '$time'";

if ($temperature != NULL) {
    $device_str .= ", temperature";
    $data_str .= ", '$temperature'";
}
if ($humidity != NULL) {
    $device_str .= ", humidity";
    $data_str .= ", '$humidity'";
}
if ($pressure != NULL) {
    $device_str .= ", pressure";
    $data_str .= ", '$pressure'";
}
if ($gas != NULL) {
    $device_str .= ", gas";
    $data_str .= ", '$gas'";
}
if ($uv_index != NULL) {
    $device_str .= ", uv_index";
    $data_str .= ", '$uv_index'";
}
if ($pm_25 != NULL) {
    $device_str .= ", pm_25";
    $data_str .= ", '$pm_25'";
}
if ($pm_10 != NULL) {
    $device_str .= ", pm_10";
    $data_str .= ", '$pm_10'";
}

$sql = "INSERT INTO data ".
    "(" . $device_str . ")".
    "VALUES".
    "(" . $data_str  . ")";

if ($mysqli -> query($sql) == TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $mysqli -> error;
}

$mysqli ->close();
?>