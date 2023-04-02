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
?>

<html>
<?
require('head.php');
?>

<body>

       <h1>Property Types</h1>

<center><a  href="index.php">Zurück</a></center>


<?php



    $sql = 'select * from property_types order by type asc ;';
    try {
      $statement = $conn->prepare($sql);
      $statement->execute();
    //  echo "<br> " . $statement->rowCount() . " Ergebnisse";

      echo "<br><center><table class='content-table' >";
      echo "<thead><tr><th align=left>ID</th><th align=left>Type</th><th align=left>Searchterms</th></b></tr></thead>";

      while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {
        echo "<tr><td align=left>", $row['id'] ,"</td><td align=left><a href=\"property_types_edit.php?id=".$row['id']."\">".$row['type'] ."</a></td><td align=left>",$row['searchterms'],"</td></tr>";
      }
    }
    catch (PDOException $e) {
      echo "Hat nicht geklappt: " . $e->getMessage();
    }



?>


 </body>
</html>
