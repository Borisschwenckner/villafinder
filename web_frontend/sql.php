<?php
session_start();
if(!isset($_SESSION['userid'])) {
  header("location: login.php");
  exit;
}
require_once 'inc/config.php';


$conn = new PDO($dsn);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);



$function = $_GET['function'];

#echo 'Hallo';
#echo $function;

        if ($function == 'duplicate_site'){
          $id = $_GET['id'];
          #$pos_id = $_GET['pos_id'];
          #echo 'Hallo';

          $sql = 'INSERT INTO sites (site,last_scraped,sitemap_url,sitemap_url_suffix,sitemap_selectors,scraped_delete,sitemap_objects_per_page,STATE,testmode,mail_customer,sitemap_selector_price,sitemap_selector_location,sitemap_selector_ref,sitemap_selector_bedroom,sitemap_selector_bathroom,sitemap_selector_size,sitemap_selector_groundsize,sitemap_selector_items,sitemap_selector_name,sitemap_selector_image,sitemap_selector_link,sitemap_selector_type,create_property_from_sitemap,
            details_selector_price,details_selector_location,details_selector_ref,details_selector_bedroom,details_selector_bathroom,details_selector_size,details_selector_groundsize,details_selector_body_seperator,details_selector_name,details_selector_image,details_selector_offertype,test_url)

            SELECT site,last_scraped,sitemap_url,sitemap_url_suffix,sitemap_selectors,scraped_delete,sitemap_objects_per_page,STATE,testmode,mail_customer,sitemap_selector_price,sitemap_selector_location,sitemap_selector_ref,sitemap_selector_bedroom,sitemap_selector_bathroom,sitemap_selector_size,sitemap_selector_groundsize,sitemap_selector_items,sitemap_selector_name,sitemap_selector_image,sitemap_selector_link,sitemap_selector_type,create_property_from_sitemap,
            details_selector_price,details_selector_location,details_selector_ref,details_selector_bedroom,details_selector_bathroom,details_selector_size,details_selector_groundsize,details_selector_body_seperator,details_selector_name,details_selector_image,details_selector_offertype,test_url
            FROM sites WHERE ID=:id;
            ';


          $statement = $conn->prepare($sql);
          $result = $statement->execute(array('id' => $id));


          header("location: sites_edit.php?id=$id");
        }


        if ($function == 'backup_tables'){

          $sql = 'drop table if exists backup_sites;';
          $statement = $conn->prepare($sql);
          $statement->execute();
          $sql = 'create table backup_sites as (select * from sites);';
          $statement = $conn->prepare($sql);
          $statement->execute();
          
          $sql = 'drop table if exists backup_locations;';
          $statement = $conn->prepare($sql);
          $statement->execute();
          $sql = 'create table backup_locations as (select * from locations);';
          $statement = $conn->prepare($sql);
          $statement->execute();

          $sql = 'drop table if exists backup_changelog;';
          $statement = $conn->prepare($sql);
          $statement->execute();
          $sql = 'create table backup_changelog as (select * from changelog);';
          $statement = $conn->prepare($sql);
          $statement->execute();

          $sql = 'drop table if exists backup_property_types;';
          $statement = $conn->prepare($sql);
          $statement->execute();
          $sql = 'create table backup_property_types as (select * from property_types);';
          $statement = $conn->prepare($sql);
          $statement->execute();
          
          $sql = 'drop table if exists backup_users;';
          $statement = $conn->prepare($sql);
          $statement->execute();
          $sql = 'create table backup_users as (select * from users);';
          $statement = $conn->prepare($sql);
          $statement->execute();

          $sql = 'drop table if exists backup_ext_information;';
          $statement = $conn->prepare($sql);
          $statement->execute();
          $sql = 'create table backup_ext_information as (select * from ext_information);';
          $statement = $conn->prepare($sql);
          $statement->execute();


          header("location: user_edit.php");
        }


        

        if ($function == 'delete_userlog'){
          $sql2 = 'delete from userlog where user_id = 2;';
          $statement = $conn->prepare($sql2);
          $statement->execute();


          header("location: userlog.php");
        }



        if ($function == 'insert_new_cron'){
          $sql2 = "insert into cron (name) values ('NEW');";
          $statement = $conn->prepare($sql2);
          $statement->execute();

          header("location: cron.php"); 
        }
        

        if ($function == 'cron'){
          $payload = $_GET['payload'];
          #echo ($payload);
          #echo ('huhuhuhu');
          $field1 = explode('|',$payload)[0];
          $id = explode('|',$payload)[1];
          $value = explode('|',$payload)[2];
          
          $sql2 = "update cron set ".$field1." = :value where id = :id;";
          $statement = $conn->prepare($sql2);
          $result = $statement->execute(array( 'value' => $value,'id' => $id ));
 

          header("location: cron.php");
        }

    #    $sql_test ='(SELECT
    #                  	string_agg(column_name, ',') col
    #                  FROM
    #                  	information_schema.columns
    #                  WHERE
    #                  	table_schema = 'public'
    #                  	AND table_name = 'sites'
    #                  	and "column_name" != 'id'
#
#                      	)';

?>
