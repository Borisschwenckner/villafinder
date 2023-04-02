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


$conn = new PDO($dsn);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
require_once('head.php');
?>
  <h1>Userlog</h1>
<center><input type="button" value="Bereinigen" onclick="window.location.href = 'sql.php?function=delete_userlog';"></input></center>

<?php
echo '<tr><td colspan=2><center><input type="button" value="Zurück" onclick="history.back()"></td><td></td></tr>';

    $sql = 'SELECT userlog.ID,userlog.DATE,users.email,userlog.log FROM userlog JOIN users ON userlog.user_id=users.ID ORDER BY userlog.ID DESC;';
    try {
      $statement = $conn->prepare($sql);
      $statement->execute();
    //  echo "<br> " . $statement->rowCount() . " Ergebnisse";

      echo "<br><table class='content-table'>";
      echo "<thead><tr><th width=200 align=left>Date</th><th align=left>Userid</th><th align=left>log</th></tr></thead>";

      while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {
        echo "<tr><td align=left>",  date( "d-m-Y H:i:s", strtotime($row['date'])) ,"</td><td align=left>",$row['email'],"</td><td align=left>",$row['log'],"</td></tr>";
      }
    }
    catch (PDOException $e) {
      echo "Hat nicht geklappt: " . $e->getMessage();
    }



?>



 </body>
</html>
