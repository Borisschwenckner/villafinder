<?
require_once 'inc/config.php';

try{
    $conn = new PDO($dsn);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

 if($conn){
 //echo "Connected to the <strong>$db</strong> database successfully!";
 }
}catch (PDOException $e){
 echo $e->getMessage();
}



$request = "";
if(isset($_POST['request'])){
   $request = $_POST['request'];
}
$request = "getcitys";
// Get states
if($request == 'getcitys'){
#   $region_id = 2;
   $result = array();$data = array();

   if(isset($_POST['region_id'])){
      $region_id = $_POST['region_id'];
#      $region_id = 2;
     # echo $region_id ;

      $sql = "select * from locations, regions where region_id= regions.id and (regions.name =:region_id or locations.area= :area) and locations.active = 1 and locations.qty_active > 0 order by city";
      $statement = $conn->prepare($sql);
      $result = $statement->execute(array('region_id' => $region_id, 'area' => $region_id));
      $qty_results = $statement->rowCount();

      if ($qty_results ==0){
         $sql = "select * from locations, regions where region_id= regions.id and  locations.active = 1 and locations.qty_active > 0 order by city";
         $statement = $conn->prepare($sql);
         $result = $statement->execute();

      }


      while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {


         $id = $row['city'];
         $name = $row['city'];
         #echo $name;
         $data[] = array(
            "id" => $id,
            "name" => $name
         );
       }

    }

   echo json_encode($data);
   die;

}
