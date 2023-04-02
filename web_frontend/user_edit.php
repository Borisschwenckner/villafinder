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

$id = $_SESSION['userid'];

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
<?require('head.php');?>

<body>

   <br><center>
   <input type="button" value="Zurück" onclick="window.location.href = '/';"></input>
   <? if   ($_SESSION['userid'] == 2){ ?>
   <input type="button" value="BACKUP Tables" onclick="window.location.href = 'sql.php?function=backup_tables';"></input>
    <? } ?>

<?php


$links_in_new_tab = 0;
$multiple_locations = 0;

if (isset($_POST['multiple_locations']) and $_POST['multiple_locations'] ==0){
$multiple_locations =1;
}
if (isset($_POST['links_in_new_tab']) and $_POST['links_in_new_tab'] ==0){
  $links_in_new_tab =1;
  }
  
  
if(isset($_GET['register']) and $_GET['register'] == 'Update') {
  
  $_SESSION['multiple_locations'] = $multiple_locations;
  $_SESSION['links_in_new_tab'] = $links_in_new_tab;
    
        $statement_u = $conn->prepare("update users set multiple_locations = :multiple_locations where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'multiple_locations' => $multiple_locations));
      
        $statement_u = $conn->prepare("update users set links_in_new_tab = :links_in_new_tab where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'links_in_new_tab' => $links_in_new_tab));
  
}
      $sql = 'SELECT * from users where id  = :id ;';

      $statement = $conn->prepare($sql);
      $statement->bindValue(':id', $id);
      $statement->execute();


      echo '<form action="?register=Update" method="post">';
    
      echo "<center><table class='content-table'>";
     # echo "<tr><b><td align=left>ID</td><td align=left>City</td><td align=left>Searchterms</td></b></tr>";
      echo "<tbody>";
      while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {
        $checked_multi="";
        if ($row['multiple_locations']==1) {
          $checked_multi="checked='checked'";
        }
        $checked_links ="";
        if ($row['links_in_new_tab']==1) {
          $checked_links="checked='checked'";
        }
        echo "<tr><td align=left>User</td><td align=left>",$row['email'],"</td></tr>";

        echo "<tr><th align=left>".$lang_tanslate['Multiple Locations']."</th><td><input type='checkbox' name='multiple_locations' ",$checked_multi," value='",$row['multiple_locations'],"' size=10></td></tr>";
        echo "<tr><th align=left>".$lang_tanslate['Links in new Tab']."</th><td><input type='checkbox' name='links_in_new_tab' ",$checked_links," value='",$row['links_in_new_tab'],"' size=10></td></tr>";
        




      }
      echo "</tbody>";
      echo '</table>';

      echo '<td><input type=submit value=Speichern></form></td>';




?>



 </body>
</html>
