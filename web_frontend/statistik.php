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

echo" <h1>Statistik</h1>";

echo '<tr><td colspan=2><center><input type="button" value="Zurück" onclick="history.back()"></td><td></td></tr>';
$sum_total =0;
$sum_active =0;
$sum_todayon = 0;
$sum_todayoff =0;
$sum_newthisyear=0;
$sum_exclusive = 0;
$sql = "
SELECT
	site,
	COUNT ( ID ) AS qty_properties,
	( SELECT COUNT ( ID ) AS qty_properties FROM properties pro WHERE pro.site = properties.site AND state = 'active' GROUP BY site ) AS active,
	( SELECT min(create_date) FROM properties pro WHERE pro.site = properties.site  GROUP BY site )::date AS first_scrap,
  ( SELECT max(create_date) FROM properties pro WHERE pro.site = properties.site  GROUP BY site )::date AS last_scrap,
	( SELECT COUNT ( ID ) AS qty_properties FROM properties pro WHERE pro.site = properties.site AND create_date = CURRENT_DATE AND state = 'active' GROUP BY site ) AS today ,
	( SELECT COUNT ( ID ) AS qty_properties FROM properties pro WHERE pro.site = properties.site AND inactive_date = CURRENT_DATE AND state = 'inactive' GROUP BY site ) AS today_inactive,
  ( SELECT COUNT ( ID ) AS qty_properties FROM properties pro WHERE pro.site = properties.site AND create_date > (date_part('year', current_date)::text||'-01-01')::date GROUP BY site ) AS new_this_year,
	( SELECT COUNT ( ID ) AS qty_properties FROM properties pro WHERE pro.site = properties.site AND state = 'active' and id not in (select source_id from relations) GROUP BY site ) AS exclusive
	
FROM
	properties
GROUP BY
	site
  order by site;";
    try {
      $statement = $conn->prepare($sql);
      $statement->execute();
    //  echo "<br> " . $statement->rowCount() . " Ergebnisse";


      echo "<br><center><table class='content-table'>";
      echo "<thead><tr><th align=left>Site</th><th align=right>QTY Total</th><th align=right>QTY Active</th><th align=right>QTY Exclusive</th><th align=right>%</th><th align=left>Started</th><th align=left>Last New Object</th><th align=right>Today New</th><th align=right>Today Off</th><th align=right>New this year</th></tr></thead>";
      $sum_qty =0;
      while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {

        $sum_total = $sum_total + $row['qty_properties'];
        $sum_active = $sum_active + $row['active'];
        $sum_todayon = $sum_todayon + $row['today'];
        $sum_todayoff = $sum_todayoff + $row['today_inactive'];
        $sum_newthisyear = $sum_newthisyear + $row['new_this_year'];
        $sum_qty = $sum_qty +1;
        $sum_exclusive = $sum_exclusive + $row['exclusive'] ;
        $percent=  (int)(($row['exclusive'] / $row['active'])*100);



        echo "<tr><b><td align=left>",$row['site'],"</td><td align=right>",$row['qty_properties'],"</td><td align=right>",$row['active'],"</td><td align=right>",$row['exclusive'],"</td><td align=right>",$percent,"</td><td width=100 align=left>",  date( "d-m-Y", strtotime($row['first_scrap'])) ,"</td><td width=100 align=left>",  date( "d-m-Y", strtotime($row['last_scrap'])) ,"</td><td align=right>",$row['today'],"</td><td align=right>",$row['today_inactive'],"</td><td align=right>",$row['new_this_year'],"</td></b></tr>";
      }
      echo "<thead><tr><b><td align=left><b>TOTAL ",$sum_qty,"</td><td align=right><b>",$sum_total,"</td><td align=right><b>",$sum_active,"</td><td align=right><b>",$sum_exclusive,"</td><td></td><td></td><td width=150 align=left><b></td><td align=right>",$sum_todayon,"</td><td align=right><b>",$sum_todayoff,"</td><td align=right><b>",$sum_newthisyear,"</td></b></tr></thead>";

    }
    catch (PDOException $e) {
      echo "Hat nicht geklappt: " . $e->getMessage();
    }



?>



 </body>
</html>
