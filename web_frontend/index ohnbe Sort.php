<?php
session_start();
if (!isset($_SESSION['userid'])) {
  header("location: login.php");
  exit;
}


require_once('head.php');

$links_in_new_tab =0;
$multiple_locations=$_SESSION['multiple_locations'];
$links_in_new_tab=$_SESSION['links_in_new_tab'];


if ($links_in_new_tab ==1){
  $target = 'target=_blank';
} else {
  $target = '';
}

  $active = 'Active';
  if (isset($_GET)) {
   
    $def_location = "Select";
    if (isset($_GET['location']) and $_GET["location"] != "Select" and $_GET["location"] != "")
        $def_location = $_GET["location"];

    $qty_dev_locations =0;

    if (isset($_GET['locations']) and $_GET["locations"] != "Select" and $_GET["locations"] != "Array" and $_GET["locations"] != ""){
        $qty_dev_locations = count($_GET['locations']);
      }
    $def_region = "Select";
    if (isset($_GET['region']) and $_GET["region"] != "Select" and $_GET["region"] != "")
      $def_region = $_GET["region"];

    $def_site = "Select";
    if (isset($_GET['site']) and $_GET["site"] != "" and $_GET["site"] != "Select")
      $def_site = $_GET["site"];

    $def_type = "Select";
    if (isset($_GET['type']) and $_GET["type"] != "" and $_GET["type"] != "Select")
      $def_type = $_GET["type"];

    $def_price_from = "0";
    if (isset($_GET['price_from']) and $_GET["price_from"] != "0" and $_GET["price_from"] != "")
      $def_price_from = $_GET["price_from"];

    $def_price_to = "99000000";
    if (isset($_GET['price_to']) and $_GET["price_to"] != "100000000" and $_GET["price_to"] != "")
      $def_price_to = $_GET["price_to"];

    $def_days = "0";
    if (isset($_GET['days']) and $_GET["days"] != "0" and $_GET["days"] != "")
      $def_days = $_GET["days"];

    $def_days_off = "0";
    if (isset($_GET['days_off']) and $_GET["days_off"] != "" and $_GET["days_off"] != "0")
      $def_days_off = $_GET["days_off"];

    $def_days_price = 0;
    if (isset($_GET['days_price']) and $_GET["days_price"] != 0 and $_GET["days_price"] != "")
      $def_days_price = $_GET["days_price"];

    $def_property_type = 'Select';
    if (isset($_GET['type']) and $_GET["type"] !=  "Select" and $_GET["type"] != "")
      $def_property_type = $_GET["type"];

    $def_offer_type = "Buy";
    if (isset($_GET["offer_type"]))
      $def_offer_type = $_GET["offer_type"];

    $def_active = "Active";
    if (isset($_GET["active"]))
      $def_active = $_GET["active"];

    $def_bed = "0";
    if (isset($_GET["bed"]) and $_GET["bed"] != "0")
      $def_bed = $_GET["bed"];

    $def_bath = "0";
    if (isset($_GET["bath"]) and $_GET["bath"] != "0")
      $def_bath = $_GET["bath"];

    $def_ref = "0";
    if (isset($_GET["ref"]) and $_GET["ref"] != "0")
      $def_ref = $_GET["ref"];

    $favorites_only = '';
    $todo_state = '';
    if (isset($_GET['favorites_only']))
      $favorites_only =  $_GET["favorites_only"];
    if (isset($_GET['state1']))
      $def_todo_state = $_GET["state1"];

    $statement_site = $conn->prepare("SELECT site FROM sites WHERE state = 1 order by site;");
    $statement_site->execute();
    $statement_ptype = $conn->prepare("SELECT * FROM options WHERE option_id = 2 and active = 1 order by sort;");
    $statement_ptype->execute();
    if ($def_region != '' and $def_region != 'Select') {
      $sql = "select * from locations, regions where region_id= regions.id and (regions.name =:region_id or locations.area = :area )  and locations.active = 1 and locations.qty_active > 0 order by city;";
      $statement_location = $conn->prepare($sql);
      $result = $statement_location->execute(array('region_id' => $def_region, 'area' => $def_region));
    } else {
      $sqlcity = "select distinct city , qty_active from locations where active = 1 and qty_active > 0 order by city;";
      $statement_location = $conn->prepare($sqlcity);
      $statement_location->execute();
    }



    $statement_area = $conn->prepare("select distinct area from locations where active = 1  order by area;");
    $statement_area->execute();
    $statement_region = $conn->prepare("select distinct name, id from regions where (select count(id) from locations where locations.region_id = regions.id) >0 order by name;");
    $statement_region->execute();
  ?>

    <form method="GET" action="index.php" id="searchform">
      <left><br>
        <table class="table1">

          <tr>
            <th><? echo $lang_tanslate['Price from / to:']; ?> </th>
            <td data-label='<? echo $lang_tanslate['Price from / to:']; ?>'>
              <input type="text" class=small name="price_from" value="<?php echo $def_price_from; ?>">
              <input type="text" class=small name="price_to" value="<?php echo $def_price_to; ?>" >
            </td>
          </tr>

          <tr>
            <th><? echo $lang_tanslate['Provider:']; ?> </th>
            <td data-label='<? echo $lang_tanslate['Provider:']; ?>'><select name="site" >
                <option selected="selected"><? echo "$def_site"; ?></option>
                <option value="Select">Select</option>
                <?php
                while ($row_site = $statement_site->fetch(PDO::FETCH_ASSOC)) {
                  echo '<option value="' . $row_site["site"] . '">' . $row_site["site"] . '</option>';
                }
                ?> 
            </td>
          <tr>

          <tr>
            <th><? echo $lang_tanslate['Region:']; ?> </th>
            <td><select name="region" id="region" >
                <option selected="selected"><? echo "$def_region"; ?></option>
                <option value="Select">Select</option>
                <?php
                while ($row_area = $statement_area->fetch(PDO::FETCH_ASSOC)) {
                  echo '<option value="' . $row_area["area"] . '">' . $row_area["area"] . '</option>';
                }
                while ($row_region = $statement_region->fetch(PDO::FETCH_ASSOC)) {
                  echo '<option value="' . $row_region["name"] . '">' . $row_region["name"] . '</option>';
                }
                ?>
          </tr>


          <tr>
          <!-- Start multiple Orte --!> 
            <th><? echo $lang_tanslate['Location:']; ?> </th>
            <? if ($multiple_locations == 0){  ?>  
              <td data-label=<?echo $lang_tanslate['Location:'];?> ><select id="location" name="location" ><option selected="selected"><? echo "$def_location"; ?></option>
              <option value="Select">Select</option> 
            <? } else { ?>
              <td data-label=<?echo $lang_tanslate['Location:'];?> ><select  id="location" name="locations[]" multiple="multiple" size='6'  >
            <? } ?>   
              <!-- End multiple Orte --!>    
           

                <-- #------------------------------------------------------------------------------------------------------------------------------------------------------ --!>

                  <?php
                  while ($row_location = $statement_location->fetch(PDO::FETCH_ASSOC)) {
                    if ($qty_dev_locations > 0){
                    $sel = (array_search($row_location["city"], $_GET['locations']) !== false) ? ' selected' : '';
                  } else {
                   $sel = ''; 
                  }
                    echo '<option '.$sel.' value="' . $row_location["city"] . '">' . $row_location["city"] . '</option>'; 
                  }
                  ?> </select></td>
            
            <tr>
                <th><? echo $lang_tanslate['Property:']; ?> </th>
                <td data-label=<? echo $lang_tanslate['Property:']; ?>>
                <select name="type">
                  <option  value=<? echo $def_type;?> selected="selected"><? echo $lang_tanslate[$def_type]; ?></option>
                  <?php
                  if   ($_SESSION['userid'] == 2){
                    echo '<option value=Without>'.$lang_tanslate["Without"].'</option>';
                  }
                  while ($row_ptype = $statement_ptype->fetch(PDO::FETCH_ASSOC)) {
                    echo '<option value="' . $row_ptype["value"] . '">' . $lang_tanslate[$row_ptype["value"]] . '</option>';
                  }
                  ?>
                  </select>

                </td>
            </tr>
          <tr>
            <th><? echo $lang_tanslate['State:']; ?> </th>
            <td data-label=<? echo $lang_tanslate['State:']; ?>>
            <select  name="active">
                <option <?php if ($def_active == 'Active') {
                          echo ("selected");
                        } ?> value="Active"><?php echo $lang_tanslate['Active']; ?></option>
                <option <?php if ($def_active == 'Inactive') {
                          echo ("selected");
                        } ?> value="Inactive"><?php echo $lang_tanslate['Inactive']; ?></option>
                <option <?php if ($def_active == 'All') {
                          echo ("selected");
                        } ?> value="All"><?php echo $lang_tanslate['All']; ?></option>
            </select>
            </td>
          </tr>
          
          <tr>
            <th ><? echo $lang_tanslate['Offer Type:']; ?> </th>
            <td data-label='<? echo $lang_tanslate['Offer Type:']; ?>'>
              <select id="buy"  name="offer_type">
                  <option value="Buy"><?php echo $lang_tanslate['Buy']; ?></option>
                  <option <?php if ($def_offer_type == 'Rent') {
                            echo ("selected");
                          } ?> value="Rent"><?php echo $lang_tanslate['Rent']; ?></option>
              </select>
            </td>
          </tr>


        </table>
        <table border=0 class="table2">
          <tr>
            <th><? echo $lang_tanslate['Days Online:']; ?> </th>
            <td data-label='<? echo $lang_tanslate['Days Online:']; ?>'>
            <input type="text" name="days" pattern='\d*' Value="<?php echo $def_days; ?>" ></td>
          </tr>

          <th><? echo $lang_tanslate['Days Offline:']; ?> </td>
          <td data-label='<? echo $lang_tanslate['Days Offline:']; ?>'><input type="text" name="days_off" pattern='\d*' Value="<?php echo $def_days_off; ?>" ></td>
          </tr>
          <tr>
            <th><? echo $lang_tanslate['Price Days:']; ?> </th>
            <td data-label='<? echo $lang_tanslate['Price Days:']; ?>'><input type="text" name="days_price" pattern='\d*' Value="<?php echo $def_days_price; ?>" ></td>
          </tr>
          <tr>
            <th><? echo $lang_tanslate['Reference:']; ?> </th>
            <td data-label='<? echo $lang_tanslate['Reference:']; ?>'><input type="text" name="ref" Value="<?php echo $def_ref; ?>" ></td>
          </tr>
          <td class='hidenormal' style="display:none;"><select id="lang" style=width:0; name="lang">
              <option value="<?php echo $lang; ?>"></option>
          </td>

          </tr>
          <?
          $var_checked = 'unchecked';
          if ($favorites_only == 1)
            $var_checked = 'checked';
          $statement_option = $conn->prepare("SELECT * FROM options WHERE option_id = 1 order by sort;");
          $statement_option->execute();
          if ($todo_state == '')
            $todo_state = 'Select';
          ?>
          <th><? echo $lang_tanslate['Favorites Only:']; ?></th>
          <td data-label='<? echo $lang_tanslate['Favorites Only:']; ?>'>
          <input type="checkbox"  name="favorites_only" value="1" <? echo $var_checked; ?>></td>
          </tr>
          <tr>

            <th><? echo $lang_tanslate['State:']; ?></th>
            <td data-label='<? echo $lang_tanslate['State:']; ?>'>
              <select name="state1" id="state1">
                <option selected="selected"><? echo "$lang_tanslate[$todo_state]"; ?></option>
                <?php
                while ($row_option = $statement_option->fetch(PDO::FETCH_ASSOC)) {
                  echo '<option value="' . $row_option["value"] . '">' . $lang_tanslate[$row_option["value"]] . '</option>';
                }
                ?>
            </td>
          </tr>
        </table>

        <table border=0 class="table3">

          <tr>
            <td align="right"><input type="submit" name="submit" align="right" value=<? echo $lang_tanslate['Search']; ?>>
    </form>
  <?php
    $sql = "select id, site, name, ref, price, location , url , create_date, last_scraped_date , changes_qty, living_size, bedroom, bathroom , property_type, price_update,image_url, location_search , offer_type, competitors_qty , notes_avalible, inactive_date , image_download_state , state from properties where id > :id and state !='obsolete'  "; #
    // das where id > :id  ist eine Krücke, weil ich die Userid bei den notes brauche
    $sql_notes = "select properties.id as id ,note, site, name, ref, price, location , url , create_date , last_scraped_date , changes_qty, living_size, bedroom, bathroom , property_type, price_update,image_url, location_search , offer_type, competitors_qty , notes_avalible, ext_information.id as ext_id , inactive_date , image_download_state, state from properties left join ext_information on ext_information.property_id = properties.id and  ext_information.user_id = :id where properties.id > 1 and state !='obsolete' and favorite = 1";
    $log = '';
    if (isset($_GET['favorites_only']))
      $favorites_only =  $_GET["favorites_only"];
    if ($favorites_only == 1)
      $sql = $sql_notes;

    $state1 = 'Select';
    if (isset($_GET['state1']))
      $state1 = $_GET["state1"];

    if ($state1 != 'Select' and $state1 != "" and $favorites_only == 1)
      $sql = $sql . " and todo_state =  '" . $state1 . "' ";


    if (isset($_GET['days_price']) and $_GET["days_price"] != 0 and  $_GET["days_price"] != "") {
      $sql = $sql . " and price_update > CURRENT_DATE -  " . $_GET["days_price"] .  " ";
      $log = $log . "Price Days: " . $_GET["days_price"] . ", ";
    }
    if (isset($_GET['price_from']) and  $_GET["price_from"] != "" and $_GET["price_from"] != 0) {
      $sql = $sql . " and price >= " . $_GET["price_from"] .  " ";
      $log = $log . "Price From: " . $_GET["price_from"] . ", ";
    } elseif (!isset($_GET['price_from'])) {
      $sql = $sql . "and create_date > CURRENT_DATE - 3";  //start nach Login
    }

    if (isset($_GET['price_to']) and $_GET["price_to"] != "99000000" and $_GET["price_to"] != "") {
      $sql = $sql . " and price <= " . $_GET["price_to"] .  " ";
      $log = $log . "Price To: " . $_GET["price_to"] . ", ";
    }
    $site = 'Select';
    if (isset($_GET['site']))
      $site = ($_GET["site"]);
    if ($site != 'Select' and $site != "") {
      $sql = $sql . " and site = :site ";
      $log = $log . "Site: " . $site . ", ";
      //$site = "%$site%";
    }
 
  #  <!-- Start multiple Orte --!>
  $qty_locations =0;
  if (isset($_GET['locations'])){ 
    $qty_locations =  count($_GET["locations"]);
    $location = $_GET["locations"][0];
    $location = str_replace("'", "''", $location);
    $location_search ='';
    if ($location !="" and $location !='Select' and $qty_locations ==1) {
      $sql = $sql . " and (city = '" . $location  ."')";
      $location_search = "$location";
      $log = $log . "Location: " . $location . ", ";
  
    }
  
    elseif ($location !="" and $location !='Select' and $qty_locations >1) {
      for($i = 0; $i < $qty_locations; $i++) {
          $location = $_GET["locations"][$i];
  
          $location = str_replace("'", "''", $location);
          #echo  $location ;
          $log = $log . "Location: " . $location . ", ";
          if ($i == 0){
          $sql = $sql . " and (city = '" . $location  ."'";
          }
          if ($i > 0){
          $sql = $sql . " or city = '" . $location ."'";
          }
  
          if ($i == $qty_locations -1){
            $sql = $sql . " ) ";
            }
          }}
  
  
  } elseif (isset($_GET['location'])){
    $location = $_GET["location"];
    if ($location != 'Select' ){
        $location = str_replace("'", "''", $location);
        $sql = $sql . " and (city = '" . $location  ."')";
        $log = $log . "Location: " . $location . ", ";
  }
    }

  
       #<!-- End multiple Orte --!>

 

    if (isset($_GET['region']))
      $region = ($_GET["region"]);

    if (isset($region) and $region != "" and $region != 'Select') {
      $sql = $sql . " and (region = :region  or location_search = :region) ";
      $log = $log . "Region: " . $region . ", ";
    }
    $ref = 0;
    if (isset($_GET['ref']))
      $ref =  ($_GET["ref"]);
    if ($ref != "0" and $ref != "") {
      $ref_search = "%$ref%";
      $sql = $sql . " and ref like :ref ";
      $log = $log . "Ref: " . $ref . ", ";
    }
    if (isset($_GET['type']))
      $property_type = $_GET["type"];

    if (isset($property_type) and $property_type =='Without'){
        $property_type = "";
      }  
    if (isset($property_type) and $property_type != "Select") {
      $sql = $sql . " and property_type = :property_type ";
      $log = $log . "Type: " . $property_type . ", ";
    }

    if (isset($_GET['active']))
      $active = $_GET['active'];

    if (isset($_GET['days_off']) and $_GET["days_off"] != 0 and $_GET["days_off"] != "") {
      $sql = $sql . " and inactive_date > CURRENT_DATE -  " . $_GET["days_off"] .  " ";
      $log = $log . "Days Off: " . $_GET["days_off"] . ", ";
      $active = 'Inactive';
    } elseif (isset($_GET['days']) and $_GET["days"] != 0 and $_GET["days"] != "") {
      $sql = $sql . " and create_date > CURRENT_DATE -  " . $_GET["days"] .  " ";
      $active = 'Active';
      $log = $log . "Days ONLINE: " . $_GET["days"] . ", ";
    }
    if (($active) == "Inactive") {
      $sql = $sql . " and state = 'inactive' ";
      $log = $log . "State: inactive, ";
    } elseif (($active) == "Active")
      $sql = $sql . " and state = 'active'  ";

    if (isset($_GET['offer_type']) and $_GET['offer_type'] == "Buy")
      $sql = $sql . " and offer_type = 'Buy'  ";
    elseif (isset($_GET['offer_type']) and $_GET['offer_type'] == "Rent") {
      $sql = $sql . " and offer_type = 'Rent'  ";
      $log = $log . "Offer Type: Rent, ";
    }

    if ($favorites_only == 1)
      $sql = $sql . " order by  ext_id desc limit  :limit offset :offset;";
    else
      $sql = $sql . " order by  price desc limit  :limit offset :offset;";


    $pos = strpos($sql, 'where');

    $id = $_SESSION['userid'];



    try {
      $statement = $conn->prepare($sql);

      if (isset($region) and $region != "Select" and $region != "" and (!empty($region))) {
        $statement->bindValue(':region', $region);
      }
      
      if (isset($site) and ($site != "Select") and ($site != '')) {
        $statement->bindValue(':site', $site);
      }
      if (isset($property_type) and ($property_type != "Select")) {
        $statement->bindValue(':property_type', $property_type);
      }
      if (isset($ref) and ($ref != "0") and ($ref != "")) {
        $statement->bindValue(':ref', $ref_search);
      }    //  echo ($statement);
      $statement->bindValue(':id', $id);
      $statement->bindValue(':limit', 1000);
      $statement->bindValue(':offset', 0);

      
      
      #---------------------------------------------------------------------------------------------------------
      
      #echo ($sql);
      #---------------------------------------------------------------------------------------------------------



      $statement->execute();
      $qty_results = $statement->rowCount();
      echo " " . $qty_results . " Ergebnisse</td></tr>";
      $log = $log . " Results: " . $qty_results . "";

      if (isset($_GET['price_from']) and $_GET["price_from"] != "") {
        $statement2 = $conn->prepare("insert into userlog (user_id, log) values (:id,:sql);");
        $statement2->bindValue(':id', $id);
        $statement2->bindValue(':sql', $log);
        $statement2->execute();
      }

      $totalRecords = $statement->rowCount();
      $currentPage = 2; // set the current page number
      $limit = 100; // set the total page records limit
      $pages = ceil($totalRecords / $limit); // get the totoal number of pages. Not using as yet
      if ($currentPage == 0 || $currentPage == 1) {
        $offset = 0; // change the offset to 0 if the page number is zero or one
      } else {
        $offset = ($currentPage - 1) * $limit; // get the correct offset otherwise
      }


      echo "</table><br><left><table class='table_result'>";

      while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {

        if ($row['image_download_state'] == 1) {
          $local_image_url = 'images/' . date('Y', strtotime($row['create_date'])) . '/' . $row['id'] . '_thumb_1.jpg';
        } else {
          $local_image_url = 'img/no_image.jpg';
        }
        $note_url = 'ext_info.php?id=' . $row['id'] . '&lang=' . $lang;
        $todo_state = '';
        $note = '';
        if ($row['notes_avalible'] > 0) {
          $statement_notes = $conn->prepare("select note, todo_state, favorite from ext_information where  property_id = :propertyid and user_id = :userid ;");
          $statement_notes->bindValue(':propertyid', $row['id']);
          $statement_notes->bindValue(':userid', $id);
          $statement_notes->execute();

          while ($notes = $statement_notes->fetch(PDO::FETCH_ASSOC)) {
            $todo_state = $notes['todo_state'];
            $note = $notes['note'];
          }
        }
        echo "<tr><td class=hidemobile  width=900 colspan=6><hr></td></tr>";
        echo "<tr><td class='hidenormal'   colspan=3><hr></td></tr>";
        echo "<tr><td class='hidenormal'  valign=bottom   ><a href=\"" . $row['url'] ."\" . ' ' . $target .><img src='", ($local_image_url), "'   /></td>";
        echo "<td valign=top class='hidenormal'  ><a  href='$note_url''><img src='img/note.png' width=30></a></td>";
        echo "<td valign=top class='hidenormal'   style=font-size:18px >$note</td></tr>";
        echo "<tr><td class=hidemobile  colspan=2>&nbsp;  </td></tr>";
        echo "<tr><th>" . $lang_tanslate['Provider'] . "</th><td  colspan=3 ><b>", ($row['site']) . " REF: " . ($row['ref']), "</b>";
              if   ($_SESSION['userid'] == 2){
                  echo '<a href="property_edit.php?id='.  $row['id'].'">  edit</a>';
              } 
        echo "</td>";

        echo "<td class=hidemobile  width=200  align=top rowspan=6 ><a href=\"" . $row['url'] . "\" . ' ' . $target .><img src='", ($local_image_url), " ' width=200  /></td>
              <td class=hidemobile width=150><a href='$note_url''><img src='img/note.png' width=30></a></td></tr>"; //height=200
        echo "<tr><th>" . $lang_tanslate['Name'] . "</th><td colspan=3  width=600>", "<a href=\"" . $row['url'] .  "\" . ' ' . $target . >" . ($row['name'])  . " </a>", "</td>";
        echo "<td class='hidemobile' align=left style=font-size:13px >" . $lang_tanslate[$todo_state] . "</td></tr>";

        echo "<tr><th>" . $lang_tanslate['Price'] . "</th><td  colspan=3  width=600><b>", number_format(($row['price']), 0, '.', '.'), "</b>  </td>
              <td class=hidemobile VALIGN=top rowspan=5 style=font-size:13px >$note</td></tr>";
        echo "<tr><th>" . $lang_tanslate['Location'] . "</th><td colspan=3  width=600>", ($row['location']), "</td></tr>";
        echo "<tr><th>" . $lang_tanslate['Facts'] . "</th><td colspan=3  width=600  >", $lang_tanslate['Size'] . ": ", ($row['living_size']),  " | " . $lang_tanslate['Bed'] . ":  ", ($row['bedroom']), " | " . $lang_tanslate['Bath'] . ":  ", ($row['bathroom']),  " | " . $lang_tanslate['Type'] . ":  ", ($row['property_type']), " </td></tr>";
        echo "<tr><th>" . $lang_tanslate['Date'] . "</th><td colspan=3  width=600 >", ($row['create_date']), " </td></tr>";
        if ($row['inactive_date'] != Null and $row['state'] == 'inactive') {
          echo "<tr><th>" . $lang_tanslate['Deactivated'] . "</th><td colspan=3  width=600 >", ($row['inactive_date']), " </td></tr>";
        }

        if ($row['changes_qty'] > 0) {
          $statement3 = $conn->prepare("select old_value, new_value from changelog where product_id = (:id3) order by id desc limit 1;");
          $statement3->bindValue(':id3', $row['id']);
          $statement3->execute();
          while ($changelog = $statement3->fetch(PDO::FETCH_ASSOC)) {
            echo "<tr><th colspan=1 >" . $lang_tanslate['Changes'] . "</th><td>", "<a href=\"changes.php?id=" . $row['id'] . "\">" . ($row['changes_qty'])  . "</a>", " | ",  number_format($changelog['old_value'], 0, '.', '.'), ' --> ',  number_format($changelog['new_value'], 0, '.', '.'), "</td><td></td></tr>";
          }
        }
        echo "</td></tr>";
     
        if ($row['competitors_qty'] > 0) {
          $statement_rel = $conn->prepare("select url , site from properties, relations where relations.target_id = properties.id and properties.state = 'active' and relations.source_id =  (:id2);");
          $statement_rel->bindValue(':id2', $row['id']);
          $statement_rel->execute();
          $qty_rel = $statement_rel->rowCount();
          echo "<tr><th width=150>" . $lang_tanslate['Relation'] . "</th><td width=500>";
          $rel_counter = 1;  
          while ($relations = $statement_rel->fetch(PDO::FETCH_ASSOC)) {
              echo " <a href=\"" . $relations['url'] . "\"  . ' ' . $target . >" . ($relations['site'])  . "</a>";
              $rel_counter = $rel_counter +1;
              if ($rel_counter <= $qty_rel){
                 echo ' | ';
              }
          }

        }
        
        echo "</td></tr>";
        # if   ($_SESSION['userid'] == 2){
        #  echo '<tr><td><a href="property_edit.php?id='.  $row['id'].'">edit</a></td></tr>';
        #    } 
        
      }
    } catch (PDOException $e) {
      echo "Hat nicht geklappt: " . $e->getMessage();
    }
  }
  echo "</table></center></div>";



  ?>

  <script src="inc/jquery-3.6.1.js"></script>

  <script type="text/javascript">
    $(document).ready(function() {

      // Region
      $('#region').change(function() {

        // Country id
        var region_id = $(this).val();

        // Empty the dropdown
        //$('#location').find('option').not(':first').remove();
        $('#location').find('option').remove();

        // AJAX request
        $.ajax({
          url: 'ajaxfile.php',
          type: 'post',
          data: {
            request: 'getcitys',
            region_id: region_id
          },
          dataType: 'json',
          success: function(response) {

            var len = 0;
            if (response != null) {
              len = response.length;
            }

            if (len > 0) {
              // Read data and create <option >
              //var option = "";
              var option = "<option value=Select>Select</option>";
              $("#location").append(option);
              for (var i = 0; i < len; i++) {

                var id = response[i].name;
                var location = response[i].name;

                option = "<option value='" + id + "'>" + location + "</option>";
                //var option = "<option value=HUHU>HHHH</option>";


                $("#location").append(option);
              }
            }
          }
        });
      });
    });
  </script>

</body>

</html>