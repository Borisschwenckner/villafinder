<?php

//echo "test!1";

   function loadlang($lang) {
   $text = array();
  require  'config.php';
  //echo $host;
  $conn = new PDO($dsn);
  $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
if ($lang =='en') {
($lang1='de');
} else {

  ($lang1=$lang);
}

     $statement9 = $conn->prepare("SELECT key, text FROM lang WHERE lang = :lang");
     $statement9->bindValue(':lang', $lang1);
     $statement9->execute();
     while ($row = $statement9->fetch(PDO::FETCH_ASSOC)) {

       if ($lang =='en'){
        $text[$row['key']] = $row['key'];
      } else
      {
       $text[$row['key']] = $row['text'];
     }
      }

        //print_r ($text);
    return $text;
   }

   //$lang = LoadLang('de');
   //echo $lang['Price'];

?>
