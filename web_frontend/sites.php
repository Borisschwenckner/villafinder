<?php

session_start();
if(!isset($_SESSION['userid'])) {
  header("location: login.php");
  exit;
}
require_once  'inc/config.php';
include 'inc/module.inc.php';

$conn = new PDO($dsn);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

require('head.php');

echo '<center><br><input type="button" value="Zurück" onclick="history.back()"></input>';

      $sql = 'SELECT * from sites order by site;';
      $statement = $conn->prepare($sql);
      $statement->execute();

      echo "<br><center><table  class='content-table' >";
      echo "<thead><tr><td align=left>Site</td><td align=left>Last Scraped</td><td align=left>QTY Sitemap</td><td align=left>Active</td><td align=left>Create Propertys</td></tr></thead><tbody>";

      while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {
        echo "<tr><td align=left><a href=\"sites_edit.php?id=".$row['id']."\">".$row['site'] ."</a></td><td align=left>",$row['last_scraped'],"</td><td align=left>",$row['sitemap_items_qty'],"</td><td align=left>",$row['state'],"</td><td align=left>",$row['create_property_from_sitemap'],"</td></tr>";
        }
      echo"</tbody></table>";


?>



 </body>
</html>
