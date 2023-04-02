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
   <div class="page-header">
       <h1><? echo $lang_tanslate['Price Changes']; ?></h1>
   </div>




<?php
    $sql = 'select id,  field_name, old_value, new_value , TIMESTAMP from changelog where  product_id = :product_id and field_name = :field_name order by timestamp  ;';
    try {
      $product_id = $_GET["id"];

      $statement = $conn->prepare($sql);
      $statement->bindValue(':product_id', $product_id);
      $statement->bindValue(':field_name', 'price');
      $statement->execute();
    //  echo "<br> " . $statement->rowCount() . " Ergebnisse";

      echo "<br><br><br><center><table style='font-family:\"Sans Serif\", font-size:10px' >";

    while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {
    //  echo "<tr><td width=120>".$lang_tanslate['Fieldname'].":</td><td align=right><b>", ($row['field_name']) ."</b></td></tr>";
      echo "<tr><td align=left>".$lang_tanslate['Old Value'].":</td><td align=right>",number_format(($row['old_value']),0, '.', '.'  ) ,"</td></tr>";
      echo "<tr><td align=left>".$lang_tanslate['New Value'].":</td><td align=right>", number_format(($row['new_value']),0, '.', '.'  ),"</td></tr>";
      $datetime = $row['timestamp'];
      echo "<tr><td>".$lang_tanslate['Effective to'].":</td><td align=right>",  date( "d-m-Y", strtotime($datetime)) ,"</td></tr>";
      echo "<tr><td colspan=2> __________________________</td><td align='left'> </td></tr>";
      echo "<tr><td></td><td align='left'> </td></tr>";

    }
    echo '<tr><td colspan=2><center><input type="button" value="Zurück" onclick="history.back()"></td><td></td></tr>';

    }
    catch (PDOException $e) {
      echo "Hat nicht geklappt: " . $e->getMessage();
    }



?>



 </body>
</html>
