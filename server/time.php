<html>

<head>
    <title>Beasley Server Time</title>
</head>

<body>
    <?php
        $current_time = time();
        $next_time = $current_time + (5 * 60);
        # Display Unix time and time in 5 minutes.
        echo $current_time ."\n";
        echo $next_time;
    ?>
</body>

</html>