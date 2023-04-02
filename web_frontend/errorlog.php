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
require('head.php');


echo "<h1>Error Log</h1>";

echo '<center><input type="button" value="Zurück" onclick="history.back()">';

    $sql = "select id, site, image_url , url , (select image from sitemap where sitemap.url = properties.url) as sitemap_url , image_download_state , ref from properties where state = 'active' and image_download_state !=1";
      $statement = $conn->prepare($sql);
      $statement->execute();
      
      #echo "<br> " . $statement->rowCount() . " Ergebnisse";
      if ($statement->rowCount() > 0){
      echo "<br><table class='content-table'>";
      echo "<thead><tr><th width=150 align=left>Site</th><th align=left>Image Url</th><th align=left>Sitemap Url</th><th align=left>State</th><th align=left>REF</th></tr></thead>";

      while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {
        echo "<tr><td>", "<a href=\"".$row['url']."\"  >" . ($row['site'])  . " </a>","</td><td>", "<a href=\"".$row['image_url']."\"  >" . ($row['image_url'])  . " </a>","</td><td>", "<a href=\"".$row['sitemap_url']."\"  >" . ($row['sitemap_url'])  . " </a>","</td><td align=left>",$row['image_download_state'],"</td><td>",$row['ref'],"</td></tr>";
      }
        echo   "</table>";
    echo "</table>";}


$sql = 'select * from log where date > CURRENT_DATE and state = 3  order by id desc ;';
      $statement = $conn->prepare($sql);
      $statement->execute();

      echo "<center><table class='content-table'>";
      echo "<thead><tr><th width=170 align=left>Date</th><th width=700 align=left>Log</th></tr></thead><tbody>";

      while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {
        echo "<tr><td  align=left>",  date( "d-m-Y H:i:s", strtotime($row['date'])) ,"</td><td align=left>",$row['log'],"</td></tr>";

      }
      echo "</tbody></table>";

?>



 </body>
</html>
