<!DOCTYPE html>
<html>


<?php
require_once  'inc/module.inc.php';
require_once  'inc/config.php';
  $conn = new PDO($dsn);
  $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

if (!empty($_GET['lang'])) :
  $lang_tanslate = LoadLang($_GET['lang']);
  $lang = $_GET['lang'];
else :
  $lang_tanslate = LoadLang("de");
  $lang = 'de';
endif;

?>
<head>
   <title>Property Finder</title>
   <link rel="stylesheet" href="css/style.css">
   <meta name="viewport" content="width=device-width, initial-scale=0.8" />
   <meta name="mobile-web-app-capable" content="yes">
   <link rel="icon" sizes="192x192" href="icon.png">
   <link rel="apple-touch-icon" sizes="180x180" href="icon.png">
 
<header>
<nav>
          <div class="logo">

                <!-- <a href="index.php"><img src="img/Logo white.png" alt="Logo" fill="yellow" ></a> -->
                <a href="index.php"><img src="img/Property Finder Logo.svg" class="filter-white" alt="Logo" fill="yellow" ></a>
                

          </div>
          <div class="lang-menu">

              <div class="selected-lang">
                <? if  ($lang =='de')
                     echo '<img src="img/flag-of-Germany.png" width=32 height=22 />';
                   elseif  ($lang =='en')
                     echo '<img src="img/flag-of-United-Kingdom.png" width=32 height=22 "/>';
                 ?>
              </div>
              <ul>
                  <li>
                      <a href="index.php?lang=de" class="de">German</a>
                  </li>
                  <li>
                      <a href="index.php?lang=en" class="en">English</a>
                  </li>
                  <li>
                      <a href="reset_password.php?lang=<? echo $lang; ?>" >Account</a>
                  </li>
                  <li>
                        <? echo '<a href="user_edit.php" >'.$lang_tanslate['Settings'].'</a>'; ?>
                         
                  </li>  
                    
                  <li>
                    <? if   ($_SESSION['userid'] == 2){
                         echo '<a href="register.php" >New User</a>';
                         } ?>
                  </li>
                  <li>
                    <? if   ($_SESSION['userid'] == 2){
                         echo '<a href="log.php" >Log</a>';
                         } ?>
                  </li>
                  <li>
                    <? if   ($_SESSION['userid'] == 2){
                         echo '<a href="userlog.php" >Userlog</a>';
                         } ?>
                  </li>
                  <li>
                    <? if   ($_SESSION['userid'] == 2){
                         echo '<a href="locations.php" >Locations</a>';
                         } ?>
                  </li>
                  <li>
                    <? if   ($_SESSION['userid'] == 2){
                         echo '<a href="property_types.php" >Types</a>';
                         } ?>
                  </li>
                  <li>
                    <? if   ($_SESSION['userid'] == 2){
                         echo '<a href="statistik.php" >Stat</a>';
                         } ?>
                  </li>
                  <li>
                    <? if   ($_SESSION['userid'] == 2){
                         echo '<a href="sites.php" >Sites</a>';
                         } ?>
                  </li>
                  <li>
                    <? if   ($_SESSION['userid'] == 2){
                         echo '<a href="cron.php" >Cronjobs</a>';
                         } ?>
                  </li>
                  <li>
                    <? if   ($_SESSION['userid'] == 2){
                         echo '<a href="errorlog.php" >Error Log</a>';
                         } ?>
                  </li>
    
              </ul>
          </div>
          <div class="float-right">
          <a href="logout.php"><img src="img/icon logout.svg"  class="filter-white" alt="Logout" width=30></a><br>
          </div>
</nav>

</header>

</head>
<body>


