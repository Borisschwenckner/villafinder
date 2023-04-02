function update_cron_check(btn) {

//alert('huhu');

var name1 = btn.id;
//var value = document.querySelector('.btn').value;
// var value1 = btn.value;
//alert(value1);

//  alert(name1);

value=0
if (btn.checked == 1)  {
//alert(name);
value=1;

}
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET","sql.php?function=cron&payload="+name1+'|'+value,true);
  xmlhttp.send();


}


function update_cron(btn) {

  //alert('huhu');
  
  var name1 = btn.id;
  //alert(name1);
  
  var value1 = btn.value;
  //alert(value1);
  
  //  alert(name1);
  
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET","sql.php?function=cron&payload="+name1+'|'+value1,true);
    xmlhttp.send();
  
  
  }