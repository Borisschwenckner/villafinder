<?php
session_start();
if (!isset($_SESSION['userid'])) {
  header("location: login.php");
  exit;
}
require_once 'inc/config.php';
include 'inc/module.inc.php';

$conn = new PDO($dsn);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

require_once('head.php');
?>
<style>#container {width:100%; text-align:left;}</style>
<?php

$locationid = $_GET['id'];

if(isset($_GET['register']) and $_GET['register'] == 'Update') {
  $searchterms = $_POST['searchterms'];
  if ($searchterms != '' and $searchterms != Null){
  $statement_u = $conn->prepare("update property_types set update_date = current_date, searchterms = :searchterms where id = :locationid ");
  $result = $statement_u->execute(array('locationid' => $locationid, 'searchterms' => $searchterms));
}}
 
    $statement1 = $conn->prepare("SELECT *  FROM property_types WHERE  id = :locationid ");
    $statement1->bindValue(':locationid', $locationid);
    $statement1->execute();

    while ($row = $statement1->fetch(PDO::FETCH_ASSOC)) {
      $type = $row['type'];
      $searchterms = $row['searchterms'];
    }




?>





<form action="?id=<?echo $locationid;?>&register=Update" method="post">
<?
  echo "<br><center><table class='content-table'>";
  echo '<tr><td>id</td><td name="locationid" >',$locationid,'</td></tr>';
  echo '<tr><td>City</td><td><input type="text" id="type" name="type" value="',$type,'" size=50></td></tr>';
  echo '<tr><td>Searchterms</td><td><textarea  type="text" rows=30 cols=70 id="searchterms" name="searchterms" value="',$searchterms,'" size=500>',$searchterms,'</textarea></td></tr>';

?>
</table>

<div class="form-group">
  <br><br>
    <input type="submit" class="btn btn-primary" value='Update'>
    <a class="btn btn-link" href="property_types.php"><? echo $lang_tanslate['Cancel']; ?></a>


</div>
</form>
</body>
</html>
