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
require('head.php');?>

 <h1>Systemlog</h1>


<?php
echo "<center><table   border=0>";
echo '<tr><td><input type="button" value="Zurück" onclick="history.back()"></td></tr>';
echo "</table>";
      $sql = 'select * from log order by id desc limit 300 ;';
      $statement = $conn->prepare($sql);
      $statement->execute();

      echo "<center><table class='content-table'>";
      echo "<thead><tr><th width=170 align=left>Date</th><th width=300 align=left>Log</th></tr></thead><tbody>";

      while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {
        echo "<tr><td  align=left>",  date( "d-m-Y H:i:s", strtotime($row['date'])) ,"</td><td align=left>",$row['log'],"</td></tr>";

      }
      echo "</tbody></tbtable>";

?>

 </body>
</html>
