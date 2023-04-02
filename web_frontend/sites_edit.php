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

$id = $_GET['id'];

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
   <input type="button" value="Zurück" onclick="history.back()"</input>

<?php


if($_GET['register'] == 'Update') {
  $id = $_GET['id'];

  if ($id > 0 ) {

    try {
        $statement_u = $conn->prepare("update sites set site = :site where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'site' => $_POST['site']));
      } catch (Exception $e) {}

    try {
        $statement_u = $conn->prepare("update sites set last_scraped = :last_scraped where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'last_scraped' => $_POST['last_scraped']));
      } catch (Exception $e) {}

    try {
        $statement_u = $conn->prepare("update sites set sitemap_url = :sitemap_url where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_url' => $_POST['sitemap_url']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_url_suffix = :sitemap_url_suffix where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_url_suffix' => $_POST['sitemap_url_suffix']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_selectors = :sitemap_selectors where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selectors' => $_POST['sitemap_selectors']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_objects_per_page = :sitemap_objects_per_page where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_objects_per_page' => $_POST['sitemap_objects_per_page']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_items_qty = :sitemap_items_qty where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_items_qty' => $_POST['sitemap_items_qty']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set email = :email where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'email' => $_POST['email']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set last_email = :last_email where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'last_email' => $_POST['last_email']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set state = :state where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'state' => $_POST['state']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set testmode = :testmode where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'testmode' => $_POST['testmode']));
      } catch (Exception $e) {}
      try {
        $statement_u = $conn->prepare("update sites set scraping_started = :scraping_started where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'scraping_started' => $_POST['scraping_started']));
      } catch (Exception $e) {}
      try {
        $statement_u = $conn->prepare("update sites set warn_days = :warn_days where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'warn_days' => $_POST['warn_days']));
      } catch (Exception $e) {}

      

    try {
        $statement_u = $conn->prepare("update sites set test_url = :test_url where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'test_url' => $_POST['test_url']));
      } catch (Exception $e) {}


    try {
        $statement_u = $conn->prepare("update sites set mail_customer = :mail_customer where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'mail_customer' => $_POST['mail_customer']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_selector_items = :sitemap_selector_items where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selector_items' => $_POST['sitemap_selector_items']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_selector_price = :sitemap_selector_price where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selector_price' => $_POST['sitemap_selector_price']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_selector_location = :sitemap_selector_location where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selector_location' => $_POST['sitemap_selector_location']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_selector_ref = :sitemap_selector_ref where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selector_ref' => $_POST['sitemap_selector_ref']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_selector_bedroom = :sitemap_selector_bedroom where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selector_bedroom' => $_POST['sitemap_selector_bedroom']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_selector_bathroom = :sitemap_selector_bathroom where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selector_bathroom' => $_POST['sitemap_selector_bathroom']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_selector_size = :sitemap_selector_size where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selector_size' => $_POST['sitemap_selector_size']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_selector_groundsize = :sitemap_selector_groundsize where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selector_groundsize' => $_POST['sitemap_selector_groundsize']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_selector_name = :sitemap_selector_name where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selector_name' => $_POST['sitemap_selector_name']));
      } catch (Exception $e) {}
      try {
        $statement_u = $conn->prepare("update sites set sitemap_selector_name2 = :sitemap_selector_name2 where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selector_name2' => $_POST['sitemap_selector_name2']));
      } catch (Exception $e) {}    try {
        $statement_u = $conn->prepare("update sites set sitemap_selector_image = :sitemap_selector_image where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selector_image' => $_POST['sitemap_selector_image']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_selector_link = :sitemap_selector_link where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selector_link' => $_POST['sitemap_selector_link']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set sitemap_selector_type = :sitemap_selector_type where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'sitemap_selector_type' => $_POST['sitemap_selector_type']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set create_property_from_sitemap = :create_property_from_sitemap where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'create_property_from_sitemap' => $_POST['create_property_from_sitemap']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set details_selector_price = :details_selector_price where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'details_selector_price' => $_POST['details_selector_price']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set details_selector_location = :details_selector_location where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'details_selector_location' => $_POST['details_selector_location']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set details_selector_ref = :details_selector_ref where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'details_selector_ref' => $_POST['details_selector_ref']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set details_selector_bedroom = :details_selector_bedroom where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'details_selector_bedroom' => $_POST['details_selector_bedroom']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set details_selector_bathroom = :details_selector_bathroom where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'details_selector_bathroom' => $_POST['details_selector_bathroom']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set details_selector_size = :details_selector_size where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'details_selector_size' => $_POST['details_selector_size']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set details_selector_groundsize = :details_selector_groundsize where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'details_selector_groundsize' => $_POST['details_selector_groundsize']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set details_selector_body_seperator = :details_selector_body_seperator where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'details_selector_body_seperator' => $_POST['details_selector_body_seperator']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set details_selector_name = :details_selector_name where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'details_selector_name' => $_POST['details_selector_name']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set details_selector_image = :details_selector_image where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'details_selector_image' => $_POST['details_selector_image']));
      } catch (Exception $e) {}
    try {
        $statement_u = $conn->prepare("update sites set details_selector_offertype = :details_selector_offertype where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'details_selector_offertype' => $_POST['details_selector_offertype']));
      } catch (Exception $e) {}
      try {
        $statement_u = $conn->prepare("update sites set details_selector_type = :details_selector_type where id = :id ");
        $result = $statement_u->execute(array('id' => $id, 'details_selector_type' => $_POST['details_selector_type']));
      } catch (Exception $e) {}




  }
}

      $sql = 'SELECT * from sites where id  = :id ;';

      $statement = $conn->prepare($sql);
      $statement->bindValue(':id', $id);
      $statement->execute();


      echo '<form action="?id='.$id.'&register=Update" method="post">';
      ?><input type="button" value="DUPLICATE THIS SITE" onclick="window.location.href = 'sql.php?function=duplicate_site&id=<?php echo $id;?>';"></input> <?

      echo "<br><center><table class='content-table'>";
      //echo "<tr><b><td align=left>ID</td><td align=left>City</td><td align=left>Searchterms</td></b></tr>";
      echo "<tbody>";
      while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {
        echo "<tr><th align=left>ID</th><td><input type='text' style='width: 400px;' name='id' value='",$row['id'],"' ></td></tr>";
        echo "<tr><th align=left>Site</th><td><input type='text' style='width: 400px;' name='site' value='",$row['site'],"' size=200></tr>";
        echo "<tr><th align=left>Last Scraped</th><td><input type='text' style='width: 400px;' name='last_scraped' value='",$row['last_scraped'],"' size=100></td></tr>";
        echo "<tr><th align=left>Sitemap URL</th><td><input type='text' style='width: 400px;' name='sitemap_url' value='",$row['sitemap_url'],"' size=200></td></tr>";
        echo "<tr><th align=left>Sitemap URL Suffix </th><td><input type='text' style='width: 400px;' name='sitemap_url_suffix' value='",$row['sitemap_url_suffix'],"' size=100></td></tr>";
        echo "<tr><th align=left>Selector Links</th><td><input type='text' style='width: 400px;' name='sitemap_selectors' value='",htmlspecialchars($row['sitemap_selectors']),"' size=100></td></tr>";
        echo "<tr><th align=left>Sitemap_objects_per_page</th><td><input type='text' style='width: 400px;' name='sitemap_objects_per_page' value='",$row['sitemap_objects_per_page'],"' size=100></td></tr>";
        echo "<tr><th align=left>Sitemap_items_qty</th><td><input type='text' style='width: 400px;' name='sitemap_items_qty' value='",$row['sitemap_items_qty'],"' size=100></td></tr>";
        echo "<tr><th align=left>State(0=Off 1=Active)</th><td><input type='text' style='width: 400px;' name='state' value='",$row['state'],"' size=100></td></tr>";
        echo '<tr><th align=left>create_property_from_sitemap (1=Sitemap, 2=Detail)</th><td><input type="text" style="width: 400px;" name="create_property_from_sitemap" value="',htmlspecialchars($row['create_property_from_sitemap']),'" size=100></td></tr>';
        echo "<tr><th align=left>Email</th><td><input type='text' style='width: 400px;' name='email' value='",$row['email'],"' size=100></td></tr>";
        echo "<tr><th align=left>Last_email</th><td><input type='text' style='width: 400px;' name='last_email' value='",$row['last_email'],"' size=100></td></tr>";
        echo "<tr><th align=left>Testmode (0=Off,1=Test,2=All)</th><td><input type='text' style='width: 400px;' name='testmode' value='",$row['testmode'],"' size=100></td></tr>";
        echo "<tr><th align=left>Scraping Started</th><td><input type='text' style='width: 400px;' name='scraping_started' value='",$row['scraping_started'],"' size=100></td></tr>";
        echo "<tr><th align=left>Warn Days</th><td><input type='text' style='width: 400px;' name='warn_days' value='",$row['warn_days'],"' size=100></td></tr>";
        echo "<tr><th align=left>Test URL</th><td><input type='text' style='width: 400px;' name='test_url' value='",$row['test_url'],"' size=100></td></tr>";
        echo "<tr><th align=left>mail_customer</th><td><input type='text' style='width: 400px;' name='mail_customer' value='",$row['mail_customer'],"' size=100></td></tr>";

        echo "<tr><td>___________________________________________________</td><td>___________________________________________________</td></tr>";
        echo '<tr><th align=left>sitemap_selector_items</th><td><input type="text" style="width: 400px;" name="sitemap_selector_items" value="',htmlspecialchars($row['sitemap_selector_items']),'" size=100></td></tr>';
        echo '<tr><th align=left>sitemap_selector_name</th><td><input type="text" style="width: 400px;" name="sitemap_selector_name" value="',htmlspecialchars($row['sitemap_selector_name']),'" size=100></td></tr>';
        echo '<tr><th align=left>sitemap_selector_name2</th><td><input type="text" style="width: 400px;" name="sitemap_selector_name2" value="',htmlspecialchars($row['sitemap_selector_name2']),'" size=100></td></tr>';
        echo '<tr><th align=left>sitemap_selector_ref</th><td><input type="text" style="width: 400px;" name="sitemap_selector_ref" value="',htmlspecialchars($row['sitemap_selector_ref']),'" size=100></td></tr>';
        echo '<tr><th align=left>sitemap_selector_price</th><td><input type="text" style="width: 400px;" name="sitemap_selector_price" value="',htmlspecialchars($row['sitemap_selector_price']),'" size=100></td></tr>';
        echo '<tr><th align=left>sitemap_selector_location</th><td><input type="text" style="width: 400px;" name="sitemap_selector_location" value="',htmlspecialchars($row['sitemap_selector_location']),'" size=100></td></tr>';
        echo '<tr><th align=left>sitemap_selector_bedroom</th><td><input type="text" style="width: 400px;" name="sitemap_selector_bedroom" value="',htmlspecialchars($row['sitemap_selector_bedroom']),'" size=100></td></tr>';
        echo '<tr><th align=left>sitemap_selector_bathroom</th><td><input type="text" style="width: 400px;" name="sitemap_selector_bathroom" value="',htmlspecialchars($row['sitemap_selector_bathroom']),'" size=100></td></tr>';
        echo '<tr><th align=left>sitemap_selector_size</th><td><input type="text" style="width: 400px;" name="sitemap_selector_size" value="',htmlspecialchars($row['sitemap_selector_size']),'" size=100></td></tr>';
        echo '<tr><th align=left>sitemap_selector_groundsize</th><td><input type="text" style="width: 400px;" name="sitemap_selector_groundsize" value="',htmlspecialchars($row['sitemap_selector_groundsize']),'" size=100></td></tr>';
        echo '<tr><th align=left>sitemap_selector_image</th><td><input type="text" style="width: 400px;" name="sitemap_selector_image" value="',htmlspecialchars($row['sitemap_selector_image']),'" size=100></td></tr>';
        echo '<tr><th align=left>sitemap_selector_link</th><td><input type="text" style="width: 400px;" name="sitemap_selector_link" value="',htmlspecialchars($row['sitemap_selector_link']),'" size=100></td></tr>';
        echo '<tr><th align=left>sitemap_selector_type</th><td><input type="text" style="width: 400px;" name="sitemap_selector_type" value="',htmlspecialchars($row['sitemap_selector_type']),'" size=100></td></tr>';

        echo "<tr><td>___________________________________________________</td><td>___________________________________________________</td></tr>";
        echo '<tr><th align=left>details_selector_body_seperator</th><td><input type="text" style="width: 400px;" name="details_selector_body_seperator" value="',htmlspecialchars($row['details_selector_body_seperator']),'" size=100></td></tr>';
        echo '<tr><th align=left>details_selector_name</th><td><input type="text" style="width: 400px;" name="details_selector_name" value="',htmlspecialchars($row['details_selector_name']),'" size=100></td></tr>';
        echo '<tr><th align=left>details_selector_ref</th><td><input type="text" style="width: 400px;" name="details_selector_ref" value="',htmlspecialchars($row['details_selector_ref']),'" size=100></td></tr>';
        echo '<tr><th align=left>details_selector_price</th><td><input type="text" style="width: 400px;" name="details_selector_price" value="',htmlspecialchars($row['details_selector_price']),'" size=100></td></tr>';
        echo '<tr><th align=left>details_selector_location</th><td><input type="text" style="width: 400px;" name="details_selector_location" value="',htmlspecialchars($row['details_selector_location']),'" size=100></td></tr>';
        echo '<tr><th align=left>details_selector_bedroom</th><td><input type="text" style="width: 400px;" name="details_selector_bedroom" value="',htmlspecialchars($row['details_selector_bedroom']),'" size=100></td></tr>';
        echo '<tr><th align=left>details_selector_bathroom</th><td><input type="text" style="width: 400px;" name="details_selector_bathroom" value="',htmlspecialchars($row['details_selector_bathroom']),'" size=100></td></tr>';
        echo '<tr><th align=left>details_selector_size</th><td><input type="text" style="width: 400px;" name="details_selector_size" value="',htmlspecialchars($row['details_selector_size']),'" size=100></td></tr>';
        echo '<tr><th align=left>details_selector_groundsize</th><td><input type="text" style="width: 400px;" name="details_selector_groundsize" value="',htmlspecialchars($row['details_selector_groundsize']),'" size=100></td></tr>';
        echo '<tr><th align=left>details_selector_image</th><td><input type="text" style="width: 400px;" name="details_selector_image" value="',htmlspecialchars($row['details_selector_image']),'" size=100></td></tr>';
        echo '<tr><th align=left>details_selector_offertype</th><td><input type="text" style="width: 400px;" name="details_selector_offertype" value="',htmlspecialchars($row['details_selector_offertype']),'" size=100></td></tr>';
        echo '<tr><th align=left>details_selector_type</th><td><input type="text" style="width: 400px;" name="details_selector_type" value="',htmlspecialchars($row['details_selector_type']),'" size=100></td></tr>';
        







      }
      echo "<tbody>";
      echo '</table><br><br>';

      echo '<td><input type=submit value=Update></form></td>';




?>



 </body>
</html>
