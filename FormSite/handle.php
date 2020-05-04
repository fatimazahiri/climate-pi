<?php
    $user_name = htmlspecialchars($_POST['user_name']);
    $user_email  = htmlspecialchars($_POST['user_email']);
    $user_lat = htmlspecialchars($_POST['user_lat']);
    $user_long = htmlspecialchars($_POST['user_long']);
    $user_bme = FALSE;
    $user_smp = FALSE;
    $user_si1 = FALSE;

    if ($_POST['A'] == 'BME680') {
        $user_bme = TRUE;
    }
    if ($_POST['B'] == 'SMPWM01C') {
        $user_smp = TRUE;
    }
    if ($_POST['C'] == 'Si1145') {
        $user_si1 = TRUE;
    }

    $db_host = 'localhost';
    $db_username = 'raspberrypi';
    $db_password = 'raspberry';
    $db_name = 'climatedb';

    // Create connection
    $conn = new mysqli($db_host, $db_username, $db_password);
    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    } 

    $conn -> select_db($db_name);
    
    $sql = "INSERT INTO $db_name (device_id, passkey_hash)
    VALUES ($user_name, $user_email)";

    if ($conn->query($sql) === TRUE) {
        echo "New record created successfully";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }


  //echo  $user_name, ' ', $user_email;
?>