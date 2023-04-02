<?php
session_start();
if(!isset($_SESSION['userid'])) {
  header("location: login.php");
  exit;
}

require_once 'inc/config.php';
include 'inc/module.inc.php';

if(!empty($_GET['lang'])):
   $lang_tanslate = LoadLang($_GET['lang']);
   $lang = $_GET['lang'];
else:
   $lang_tanslate = LoadLang("de");
   $lang = 'de';
endif;


try{
 $conn = new PDO($dsn);
 if($conn){
 //echo "Connected to the <strong>$db</strong> database successfully!";
 }
}catch (PDOException $e){
 // report error message
 echo $e->getMessage();
}

?>
<!DOCTYPE html>
<html>

<head>
  <title>Registrierung</title>
  <meta charset="UTF-8">
  <title>Reset Password</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="css/form.css">
  <style type="text/css">
      body{ font: 14px sans-serif; text-align: center;}
      .wrapper{ width: 350px; padding: 20px; }
  </style>
    <?require('head.php');?>
</head>
<body>

<?php
$showFormular = true; //Variable ob das Registrierungsformular anezeigt werden soll
$userid = $_SESSION['userid'];

$statement = $conn->prepare("SELECT * FROM users WHERE id = :userid");
$result = $statement->execute(array('userid' => $userid));
$user = $statement->fetch();
$hasright = ($user["3"]);
if($hasright != 1) {
  $showFormular = false;
  $error = true;
  echo ('<center><br>You are not authorized to create users. <br><br><a href="index.php">Back</a>');

}

if(isset($_GET['register'])) {
    $error = false;
    $email = $_POST['email'];
    $passwort = $_POST['passwort'];
    $passwort2 = $_POST['passwort2'];

    if(!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo 'Please enter a valid email address<br>';
        $error = true;
    }
    if(strlen($passwort) == 0) {
        echo 'Please enter a Password<br>';
        $error = true;
    }
    if($passwort != $passwort2) {
        echo 'The passwords do not match<br>';
        $error = true;
    }

    //Überprüfe, dass die E-Mail-Adresse noch nicht registriert wurde
    if(!$error) {
        $statement = $conn->prepare("SELECT * FROM users WHERE email = :email");
        $result = $statement->execute(array('email' => $email));
        $user = $statement->fetch();

        if($user !== false) {
            echo 'E-Mail Adress already exists<br>';
            $error = true;
        }
    }

    //Keine Fehler, wir können den Nutzer registrieren
    if(!$error) {
        $passwort_hash = password_hash($passwort, PASSWORD_DEFAULT);

        $statement = $conn->prepare("INSERT INTO users (email, passwort) VALUES (:email, :passwort)");
        $result = $statement->execute(array('email' => $email, 'passwort' => $passwort_hash));

        if($result) {
            echo '<br>User successfully registered. <br><br> <a href="index.php">Back</a>';
            $showFormular = false;
        } else {
            echo 'Uppps.... An Error occured<br>';
        }
    }
}

if($showFormular) {
?><center>
<div class="wrapper">
    <h2>Register new User</h2>
    <p>Please fill out this form.</p>
<form action="?register=1" method="post">
E-Mail:<br>
<input type="email" size="40" maxlength="250" name="email"><br><br>

Password:<br>
<input type="password" size="40"  maxlength="250" name="passwort"><br>

Repeat password:<br>
<input type="password" size="40" maxlength="250" name="passwort2"><br><br>

<div class="form-group">
    <input type="submit" class="btn btn-primary" value="Submit">
    <a class="btn btn-link" href="index.php">Cancel</a>
</div>

</form>
<div>
<?php
} //Ende von if($showFormular)
?>

</body>
</html>
