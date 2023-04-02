<?php

$host='sql12.your-server.de';
$db = 'properies';
$username = 'schweng_2';
$password = 'v9gyQ62fetFM2jDU';

$dsn = "pgsql:host=$host;port=5432;dbname=$db;user=$username;password=$password;sslmode='verify-full';sslrootcert='inc/psqlca.pem'";

#$email = 'boris_temp@schwenckner.net';
$email_recipient = 'boris_temp@schwenckner.net';

$con = pg_connect("host=$host dbname=$db user=$username password=$password");

if (!$con) {
   die('Connection failed.');
}

?>
