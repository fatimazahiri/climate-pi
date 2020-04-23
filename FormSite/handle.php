<?php
  // The global $_POST variable allows you to access the data sent with the POST method by name
  $user_name = htmlspecialchars($_POST['user_name']);
  $user_email  = htmlspecialchars($_POST['user_email']);

  echo  $user_name, ' ', $user_email;
?>