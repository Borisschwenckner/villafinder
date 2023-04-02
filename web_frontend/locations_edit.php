<?php
session_start();
if (!isset($_SESSION['userid'])) {
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


$conn = new PDO($dsn);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

require_once('head.php');
?>
<style>#container {width:100%; text-align:left;}</style>
<?php

$locationid = $_GET['id'];



if(isset($_GET['register']) and $_GET['register'] == 'Updateit') {
  $searchterms = $_POST['searchterms'];
  $city = $_POST['city'];
  $area = $_POST['area'];
  $region_id = $_POST['region_id'];
  if ($searchterms != '' and $searchterms != Null){
  $statement_u = $conn->prepare("update locations set update_date = current_date, searchterms = :searchterms , city = :city, area = :area, region_id = :region_id where id = :locationid ");
  $result = $statement_u->execute(array('locationid' => $locationid, 'searchterms' => $searchterms, 'city' => $city, 'area' => $area, 'region_id' => $region_id));

 }
}


    $statement1 = $conn->prepare("SELECT *  FROM locations WHERE  id = :locationid ");
    $statement1->bindValue(':locationid', $locationid);
    $statement1->execute();

    while ($row = $statement1->fetch(PDO::FETCH_ASSOC)) {
      $city = $row['city'];
      $area = $row['area'];
      $region_id = $row['region_id'];
      $searchterms = $row['searchterms'];
    }
    

    $stmt = $conn->prepare("SELECT name FROM regions WHERE id = ? ");
    $stmt->execute([$region_id]);
    $row3= $stmt->fetch(PDO::FETCH_ASSOC);
    $region_name = $row3['name'];

?>





<form action="?id=<?echo $locationid;?>&register=Updateit" method="post">
<?
  echo "<br><center><table class='content-table'>";
  echo '<tr><td>id</td><td name="locationid" >',$locationid,'</td></tr>';
  echo '<tr><td>City</td><td><input type="text" id="city" name="city" value="',$city,'" size=50></td></tr>';
  echo '<tr><td>Searchterms</td><td><textarea  type="text" rows=10 cols=70 id="searchterms" name="searchterms" value="',$searchterms,'" size=500>',$searchterms,'</textarea></td></tr>';
  #echo '<tr><td>Area</td><td><input type="text" id="area" name="area" value="',$area,'" size=50></td></tr>';
  echo "<tr><td>Area</td><td><select name='area'><option selected='selected' value='".$area ."'>".$area."</option>";
      $statement_area = $conn->prepare("select distinct area from locations where active = 1  order by area;");
      $statement_area->execute();
      while ($row_area = $statement_area->fetch(PDO::FETCH_ASSOC)) {
          echo '<option value="'.$row_area["area"].'">'.$row_area["area"].'</option>';
          }
      echo "</select></td></tr>'";

  echo "<tr><td>Community</td><td><select name='region_id'><option selected='selected' value=".$region_id .">".$region_name."</option>";
        $statement_regions = $conn->prepare("select id, name from regions order by name;");
        $statement_regions->execute();
        while ($row_regions = $statement_regions->fetch(PDO::FETCH_ASSOC)) {
            echo '<option value="'.$row_regions["id"].'">'.$row_regions["name"].'</option>';
            }
        echo "</select></td></tr>'";


?>
</table>

<div class="form-group">
  <br><br>
    <input type="submit" class="btn btn-primary" value=<? echo $lang_tanslate['Update']; ?>>
    <a class="btn btn-link" href="locations.php"><? echo $lang_tanslate['Cancel']; ?></a>


</div>
</form>
</body>
</html>
