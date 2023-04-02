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
$id = $_GET['id'];


if(isset($_GET['register']) and $_GET['register'] == 'Updateit') {
  $image_url = $_POST['image_url'];
  $statement_u = $conn->prepare("update  properties set  bedroom = :bedroom where id = :id ");
  $result = $statement_u->execute(array('id' => $id, 'bedroom' => $_POST['bedroom']));

  $statement_u = $conn->prepare("update  properties set  bathroom = :bathroom where id = :id ");
  $result = $statement_u->execute(array('id' => $id, 'bathroom' => $_POST['bathroom']));
  
  $statement_u = $conn->prepare("update  properties set  property_type = :property_type where id = :id ");
  $result = $statement_u->execute(array('id' => $id, 'property_type' => $_POST['property_type']));

  $statement_u = $conn->prepare("update  properties set  living_size = :living_size where id = :id ");
  $result = $statement_u->execute(array('id' => $id, 'living_size' => $_POST['living_size']));
  
  $statement_u = $conn->prepare("update  properties set  price = :price where id = :id ");
  $result = $statement_u->execute(array('id' => $id, 'price' => $_POST['price']));

  $statement_u = $conn->prepare("update  properties set  image_download_state = :image_download_state where id = :id ");
  $result = $statement_u->execute(array('id' => $id, 'image_download_state' => $_POST['image_download_state']));

  $statement_u = $conn->prepare("update  properties set  image_url = :image_url where id = :id ");
  $result = $statement_u->execute(array('id' => $id, 'image_url' => $_POST['image_url']));

  $statement_u = $conn->prepare("update  properties set  state = :state where id = :id ");
  $result = $statement_u->execute(array('id' => $id, 'state' => $_POST['state']));
}


    $statement1 = $conn->prepare("SELECT *  FROM properties WHERE  id = :id ");
    $statement1->bindValue(':id', $id);
    $statement1->execute();

    while ($row = $statement1->fetch(PDO::FETCH_ASSOC)) {
      $property_type = $row['property_type'];
      $image_url = $row['image_url'];
      $bedroom = $row['bedroom'];
      $bathroom = $row['bathroom'];
      $living_size = $row['living_size'];
      $price = $row['price'];
      $image_download_state = $row['image_download_state'];
      $state = $row['state'];  

    }




?>

<form action="?id=<?echo $id;?>&register=Updateit" method="post">
<?
  echo "<br><center><table class='content-table'>";
  echo '<tr><td>id</td><td name="id" >',$id,'</td></tr>';
  echo '<tr><td>Bedroom</td><td><input type="text"  name="bedroom" value="',$bedroom,'" size=50></td></tr>';
  echo '<tr><td>Bathroom</td><td><input type="text"  name="bathroom" value="',$bathroom,'" size=50></td></tr>';
  echo '<tr><td>Price</td><td><input type="text"  name="price" value="',$price,'" size=50></td></tr>';
  echo '<tr><td>Size</td><td><input type="text"  name="living_size" value="',$living_size,'" size=50></td></tr>';
  
  echo"<tr><td>Property Type</td>";
  echo"  <td><select name='property_type' style=width:150;><option selected='selected' value=".$property_type.">".$property_type."</option>";
            echo "<option  value='Select'>Select</option>";
            $statement_account = $conn->prepare("select * from property_types order by type;");
            $statement_account->execute();
            while ($row_account = $statement_account->fetch(PDO::FETCH_ASSOC)) {
            echo '<option value="'.$row_account["type"].'">'.$row_account["type"].'</option>';
            }
  echo"<tr><td>State</td>";
  echo"  <td><select name='state' style=width:150;><option selected='selected' value=".$state.">".$state."</option>";
            echo "<option  value='active'>active</option>";
            echo "<option  value='inactive'>inactive</option>";
    
  echo '<tr><td>Image URL</td><td><textarea  type="text" rows=5 cols=70  name="image_url" value="',$image_url,'" size=500>',$image_url,'</textarea></td></tr>';
  echo '<tr><td>Image download state</td><td><input type="text"  name="image_download_state" value="',$image_download_state,'" size=50></td></tr>';
  
?>
</table>

<div class="form-group">
  <br><br>
    <input type="submit" class="btn btn-primary" value='Update'>
    <a class="btn btn-link" href="index.php"><? echo $lang_tanslate['Cancel']; ?></a>


</div>
</form>
</body>
</html>
