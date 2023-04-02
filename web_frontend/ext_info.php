<?php
session_start();
if(!isset($_SESSION['userid'])) {
  header("location: login.php");
  exit;
}
require_once 'inc/config.php';
include 'inc/module.inc.php';

$conn = new PDO($dsn);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
?>
<html>
<?
require('head.php');

$note_id =0;
if (!isset($product_id)) {
$product_id = $_GET['id'];
}
$userid = $_SESSION['userid'];

$statement1 = $conn->prepare("SELECT ext_information.id as id, note, todo_state, favorite FROM ext_information WHERE  user_id = :userid and property_id = :product_id");
$statement1->bindValue(':product_id', $product_id);
$statement1->bindValue(':userid', $userid);
$statement1->execute();
while ($row = $statement1->fetch(PDO::FETCH_ASSOC)) {
  $note = $row['note'];
  $note_id = $row['id'];
  $favorite = $row['favorite'];
  $state = $row['todo_state'];
}

$statement_pro = $conn->prepare("SELECT id, name, image_url, site, ref, url, create_date FROM  properties WHERE properties.id  = :product_id");
$statement_pro->bindValue(':product_id', $product_id);
$statement_pro->execute();
while ($row_property = $statement_pro->fetch(PDO::FETCH_ASSOC)) {
  $property_name = $row_property['name'];
  $site = $row_property['site'];
  $ref = $row_property['ref'];
  $url = $row_property['url'];
  $local_image_url='https://villafinder.eu/images/'. date('Y', strtotime($row_property['create_date'])). '/'.$row_property['id']. '_thumb_1.jpg';
}

  if ($note_id == 0):
      $value1='Insert';
  elseif ($note_id > 0):
      $value1='Update';
  endif;

if (isset($_GET['register'])){
if($_GET['register'] == 'Insert') {
  $note = $_POST['note'];
  $favorite = $_POST['favorite'];
  $state = $_POST['state1'];
  $statement = $conn->prepare("INSERT INTO ext_information (user_id, property_id, note, todo_state, favorite) VALUES (:userid, :propertyid, :note, :state, :favorite )");
  $result = $statement->execute(array('userid' => $userid, 'propertyid' => $product_id, 'note' => $note , 'favorite' => $favorite, 'state' => $state));
  $statement2 = $conn->prepare("update properties set notes_avalible = 1 where id =  :propertyid ");
  $result = $statement2->execute(array('propertyid' => $product_id));
echo "<script>window.close();</script>";
}

if($_GET['register'] == 'Update') {
  $note = $_POST['note'];
  $favorite = $_POST['favorite'];
  $state = $_POST['state1'];
  $statement_u = $conn->prepare("update ext_information set note = :note, todo_state= :state, favorite= :favorite where user_id = :userid and property_id = :propertyid");
  $result = $statement_u->execute(array('userid' => $userid, 'propertyid' => $product_id, 'note' => $note , 'favorite' => $favorite, 'state' => $state));
echo "<script>window.close();</script>";
}
}

//if (!is_numeric($state_id)) $state_id =0;
$statement_option = $conn->prepare("SELECT * FROM options WHERE option_id = 1 order by sort;");
$statement_option->execute();

?>


<br>
<?
  echo "<table border=0 class='table_note' >";
  echo "<tr><th>$property_name</th></tr>";
  echo "<tr><td>$site $ref</td></tr>";
  echo "<tr><td><a href=\"".$url."\"><img src=".$local_image_url." width=200  /></td></tr>";
?>

    <form action="?id=<?echo $product_id;?>&register=<? echo $value1; ?>" method="post">
    <tr><td><? echo $lang_tanslate['Favorite:'];?><input type="checkbox" id="favorite" name="favorite" value="1" Checked></td></tr>

    <tr><td>
    <label for="state1"><? echo $lang_tanslate['State:'];?></label><select name="state1" id="state1"><option selected="selected"><? echo "$lang_tanslate[$state]"; ?></option>
    <?php
      while ($row_option = $statement_option->fetch(PDO::FETCH_ASSOC)) {
        echo '<option value="'.$row_option["value"].'">'.$lang_tanslate[$row_option["value"]].'</option>';
         }
?>
</select>
</tr></td>

<tr><td><textarea name="note" cols="100" rows="20"/><? echo $note; ?></textarea>

</tr></td> <tr><td>
    <center><input type="submit" value=<? echo $lang_tanslate[$value1]; ?>>
    <a class="btn btn-link" href="index.php"><? echo $lang_tanslate['Cancel']; ?></a>


</form>
<tr><td>
</table>


</body>
</html>
