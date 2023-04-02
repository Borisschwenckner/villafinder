<?php

session_start();
if(!isset($_SESSION['userid'])) {
  header("location: login.php");
  exit;
}
$id = $_SESSION['userid'];
//echo ($id);

require_once 'inc/config.php';
try{
    $conn = new PDO($dsn);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

 if($conn){
 //echo "Connected to the <strong>$db</strong> database successfully!";
 }
}catch (PDOException $e){
 echo $e->getMessage();
}


//echo "Logout erfolgreich";
header("location: login.php");
session_destroy();

$statement2 = $conn->prepare("insert into userlog (user_id, log) values (:id,'User logged out');");
$statement2->bindValue(':id', $id);
$statement2->execute();
#$statement2->close();




exit;

?>
