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

$submission_id = $_POST['submission_id'];
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

mysql_connect( $db_host, $db_username, $db_password) or die(mysql_error());
mysql_select_db($db_name);

mysql_query("INSERT INTO data (
            location, time, temperature, humidity, pressure, uv_index)
            VALUES
            ($location, $time, $temperature, $humidity, $pressure, $uv_index)")
or die(mysql_error());
?>
