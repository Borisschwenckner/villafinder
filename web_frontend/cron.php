<?php

session_start();
if(!isset($_SESSION['userid'])) {
  header("location: login.php");
  exit;
}
require_once  'inc/config.php';
require('head.php');

?>
<script src="css/switch.js"></script>
<link rel="stylesheet" href="css/switch.css">

<body><center><br>


<input type="button" value="Zurück" onclick="history.back()"></input>
<input type="button" value="INSERT NEW Cron" onclick="window.location.href = 'sql.php?function=insert_new_cron';"></input>

<?php
 if(isset($_GET['register']) and $_GET['register'] == 'Update') {

  
  if ($_GET['cron'] > 0 ) {

   try {
      $statement_u = $conn->prepare("update cron set run_next_time = :run_next_time where id = :id ");
      $result = $statement_u->execute(array('id' => $_GET['cron'], 'run_next_time' => $_POST['run_next_time']));
    } catch (Exception $e) {}
    try {
      $statement_u = $conn->prepare("update cron set name = :name where id = :id ");
      $result = $statement_u->execute(array('id' => $_GET['cron'], 'name' => $_POST['name']));
    } catch (Exception $e) {}
    try {
      $statement_u = $conn->prepare("update cron set sort = :sort where id = :id ");
      $result = $statement_u->execute(array('id' => $_GET['cron'], 'sort' => $_POST['sort']));
    } catch (Exception $e) {}
 
  }}

    $sql = 'SELECT * FROM cron order by sort;';



      $statement = $conn->prepare($sql);
      $statement->execute();
      
      echo "<center><table  class='content-table' >";
      echo "<thead><tr><td align=left>Name</td>
            <td align=left>Run Next Time</td>
            <td align=left>Sort</td>
            <td align=left></td>
            </tr></thead>";

      while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {
  
     #   echo '<form action="?cron='.$row["id"].'&register=Update" method="post">';
        
        echo "<td data-label='Name'><input type='text' name='name' value='",$row['name'],"' size=40></td>";

        echo '<td><center><input type="checkbox" id="run_next_time|'.$row['id'].'" name="run_next_time" onchange="update_cron_check(this)" '.($row['run_next_time'] == 1 ? 'checked' : '').' value="1"/>&nbsp;</center></td>';
   #     echo "<td data-label='Run Next Time' ><input type='text' name='run_next_time' value='",$row['run_next_time'],"' size=10></td>";
     
    echo "<td data-label='Sort' ><input type='text' name='sort' id='sort|".$row['id']."' onchange='update_cron(this)' value='",$row['sort'],"' size=10></td>";

        #echo '<td><input type=submit value=Update></form></td>';
        echo "</tr>";
      }

      echo "</tbody></tbtable>";
      

?>
<br>
Die Cronjobs laufen um 45 von Geesthacht und um 15 aus Mallorca von 07:00 - 19:00 Uhr


 </body>
</html>
