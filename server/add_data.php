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


$device_str = "device_id, time";
$data_str = "'$device_id', '$time'";

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
if ($uv_index != NULL) {
    $device_str .= ", uv_index";
    $data_str .= ", '$uv_index'";
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