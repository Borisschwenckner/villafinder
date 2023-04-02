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
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

 if($conn){
 //echo "Connected to the <strong>$db</strong> database successfully!";
 }
}catch (PDOException $e){
 echo $e->getMessage();
}

$userid = $_SESSION['userid'];

// Define variables and initialize with empty values
$new_password = $confirm_password = "";
$new_password_err = $confirm_password_err = "";

// Processing form data when form is submitted
if($_SERVER["REQUEST_METHOD"] == "POST"){

    // Validate new password
    if(empty(trim($_POST["new_password"]))){
        $new_password_err = $lang_tanslate["Please enter the new password."];
    } elseif(strlen(trim($_POST["new_password"])) < 6){
        $new_password_err = "Password must have atleast 6 characters.";
    } else{
        $new_password = trim($_POST["new_password"]);
    }

    // Validate confirm password
    if(empty(trim($_POST["confirm_password"]))){
        $confirm_password_err = "Please confirm the password.";
    } else{
        $confirm_password = trim($_POST["confirm_password"]);
        if(empty($new_password_err) && ($new_password != $confirm_password)){
            $confirm_password_err = "Password did not match.";
        }
    }

    // Check input errors before updating the database
    if(empty($new_password_err) && empty($confirm_password_err)){
        $param_password = password_hash($new_password, PASSWORD_DEFAULT);
        $param_id = $_SESSION["id"];

        $statement = $conn->prepare("update users set passwort=:passwort where id = :id ");
        $result = $statement->execute(array('id' => $userid, 'passwort' => $param_password));

        if($result) {
            echo 'Passwort erfolgreich geändert<br>. <a href="login.php">Zum Login</a>';
            header("location: login.php");
            $showFormular = false;
        } else {
            echo 'Leider ist ein Fehler aufgetreten<br>';
        }

    }


}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Reset Password</title>
    <link rel="stylesheet" href="css/form.css">
    <style type="text/css">
        body{ font: 14px sans-serif; text-align: center;}

    </style>
    <?require('head.php');?>

</head>
<body><center>
    <div class="wrapper">
        <h2><? echo $lang_tanslate["Reset Password"]; ?></h2>
        <p><? echo $lang_tanslate["Please fill out this form to reset your password."]; ?></p>
        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
            <div class="form-group <?php echo (!empty($new_password_err)) ? 'has-error' : ''; ?>">
                <label><? echo $lang_tanslate["New Password"]; ?></label>
                <input type="password" name="new_password" class="form-control" value="<?php echo $new_password; ?>">
                <span class="help-block"><?php echo $new_password_err; ?></span>
            </div>
            <div class="form-group <?php echo (!empty($confirm_password_err)) ? 'has-error' : ''; ?>">
                <label><? echo $lang_tanslate["Confirm Password"]; ?></label>
                <input type="password" name="confirm_password" class="form-control">
                <span class="help-block"><?php echo $confirm_password_err; ?></span>
            </div>
            <div class="form-group">
                <input type="submit" class="btn btn-primary" value="<? echo $lang_tanslate["Submit"]; ?>">
                <a class="btn btn-link" href="index.php"><? echo $lang_tanslate["Cancel"]; ?></a>
            </div>
        </form>
    </div>
</body>
</html>
