<?php
// **PREVENTING SESSION HIJACKING**
// Prevents javascript XSS attacks aimed to steal the session ID
ini_set('session.cookie_httponly', 1);

// **PREVENTING SESSION FIXATION**
// Session ID cannot be passed through URLs
ini_set('session.use_only_cookies', 1);

// Uses a secure connection (HTTPS) if possible
ini_set('session.cookie_secure', 1);

session_start();
require_once 'inc/config.php';


$conn = new PDO($dsn);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
    $ip = $_SERVER['HTTP_CLIENT_IP'];
} elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
} else {
    $ip = $_SERVER['REMOTE_ADDR'];
}

$date= date('Y-m-d H:i:s');
$lock_minutes = 10;
$lock_minutes2 = 600;

$valid_time = date('Y-m-d H:i:s', strtotime('-'.$lock_minutes.' minutes', strtotime($date)));

$headers  = 'MIME-Version: 1.0' . "\r\n";
$headers .= 'Content-type: text/html; charset=UTF-8' . "\r\n";
$headers .= 'From: Docs <Boris@schwenckner.net>' . "\r\n";

$msg ='';

if(isset($_GET['msg'])) {
  $msg = ($_GET['msg']);
  }

  if(isset($_GET['login']) and $_GET['login'] == 1 and isset($_POST['email']) and $_POST['email'] != '') {
    $email = $_POST['email'];
    $passwort = $_POST['passwort'];
    $errorMessage1 = $email;
    $statement1 = $conn->prepare("update ipcheck set active = 0 where timestamp <= :valid_time ;");
    $statement1->bindValue(':valid_time', $valid_time);
    $statement1->execute();

    $statement = $conn->prepare("SELECT id, email, passwort, active, can_create_users, multiple_locations, links_in_new_tab FROM users WHERE email = :email");
    $result = $statement->execute(array('email' => $email));
    $user = $statement->fetch();

    $statement = $conn->prepare("SELECT * FROM ipcheck WHERE ip = :ip and active = 1");
    $result = $statement->execute(array(':ip' => $ip));
    $total_ips = $statement->rowCount();
    $statement = $conn->prepare("SELECT * FROM ipcheck WHERE ip = :ip and timestamp::date = current_date");
    $result = $statement->execute(array(':ip' => $ip));
    $total_ips2 = $statement->rowCount();

    //Überprüfung des Passworts
    if ($user !== false && password_verify($passwort, $user['passwort']) && $user['active'] == 1 && $total_ips <=4 && $total_ips2 < 10)  {
        $_SESSION['userid'] = $user['id'];
        $_SESSION['multiple_locations'] = $user['multiple_locations'];
        $_SESSION['links_in_new_tab'] = $user['links_in_new_tab'];
        
        
        header("location: index.php");
        $id = $user['id'];
        mail($email_recipient,"LOGIN ERFOLREICH Villafinder.eu " . $ip,$email,$headers);
        $statement2 = $conn->prepare("insert into userlog (user_id, log, ip) values (:id,'User logged in from $ip', :ip);");
        $statement2->bindValue(':id', $id);
        $statement2->bindValue(':ip', $ip);
        $statement2->execute();

        $statement2 = $conn->prepare("update ipcheck set active = 0 where ip = :ip ;");
        $statement2->bindValue(':ip', $ip);
        $statement2->execute();

      //  $statement2->close();

        exit;

      } else if ($total_ips >4 && $total_ips2 < 10) {
          $errorMessage = 'Login gesperrt für '.$lock_minutes.' Minuten<br>';
          header("Location:login.php?msg=$errorMessage");

      } else if ( $total_ips2 >= 10) {
            $errorMessage = 'Login gesperrt. Bitte wenden Sie sich an ihren Administator<br>';
            header("Location:login.php?msg=$errorMessage");

      } else {
        $errorMessage = 'Login incorrect<br>Anzahl Fehlversuche: ' .$total_ips+1  ;
        $email = $_POST['email'];
        $passwort = $_POST['passwort'];
        header("location: login.php");
        mail($email_recipient,"LOGIN NICHT ERFOLREICH Villafinder.eu " . $ip,$email,$headers);

        $statement2 = $conn->prepare("insert into userlog ( log) values ('Login incorrect Email: ' || :email ||' Password ' || :passwort ||' Password ' || :ip);");
        $statement2->bindValue(':email', $email);
        $statement2->bindValue(':passwort', $passwort);
        $statement2->bindValue(':ip', $ip);
        $statement2->execute();

        $statement2 = $conn->prepare("insert into ipcheck ( ip, timestamp) values (:ip, :date);");
        $statement2->bindValue(':date', $date);
        $statement2->bindValue(':ip', $ip);
        $statement2->execute();
      //  $statement2->close();
      //  echo $date;

      header("Location:login.php?msg=$errorMessage");
    }

}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!--<link rel="stylesheet" href="css/bootstrap.css"> -->
    <style type="text/css">
       body{ font: 16px sans-serif; text-align: center; color:white; }
       body { margin-left:10px; margin-right:10px; margin-top:0px; margin-bottom:0px }
       <!--
       body {
            background-image: url(img/background5.jpeg);
            background-repeat: no-repeat;
            background-position: center;
            }
            -->
      .button {
            font-family: "Lucida Grande", Geneva, Verdana, Arial, Helvetica, sans-serif;
            font-size: 13px;
            padding-bottom: 2px;
            vertical-align: middle;
            border: 1px solid transparent;
            color:black;
            }
       .page-header {
            font-family: "Lucida Grande", Geneva, Verdana, Arial, Helvetica, sans-serif;
            margin-top:50px;
            font-size: 36px;
            //font-weight: bold;
            color:black;
            }
        .login {
            font-family: "Lucida Grande", Geneva, Verdana, Arial, Helvetica, sans-serif;
            margin-top:380px;
            font-size: 13px;
            <!--font-weight: bold;-->
            color:white;
            }
            .filter-navy{
                /*<!-- https://codepen.io/sosuke/pen/Pjoqqp --> 
              /* Marineblau */
              filter: invert(12%) sepia(76%) saturate(7011%) hue-rotate(246deg) brightness(66%) contrast(131%)
              
              }
              .filter-white{
                /*<!-- https://codepen.io/sosuke/pen/Pjoqqp --> 
              /* Weiss  */
              filter: invert(100%) sepia(100%) saturate(1%) hue-rotate(158deg) brightness(108%) contrast(101%);               
              }           
   </style>
</head>
<body>
<center>
    <div class="page-header">
      <img centher src="img/Property Finder Logo.svg" class="filter-navy" width = 300>


    </div>



<form action="?login=1" method="post" class="login">

    Login:<br>
      <input type="email" size="40" maxlength="250" name="email"><br><br>

    Password:<br>
      <input type="password" size="40"  maxlength="250" name="passwort"><br><br>
      <input type="submit" value="Login" class="button" >
</form>

</center><br><br>

    <?

          echo $msg;
    ?>

</body>
</html>
