// function dark_day() {
//    var element = document.body;
//    element.classList.toggle("dark-mode");
// }
// document.cookie = "isDark=true";
// function get_alert() {
//     alertify.alert('Way To Risk Predictor', '<body style="z-index:99999;"><center><h1>Welcome</h1></center><br><center><h2 style="color:blue;">To The</h2><center><br><h2 style="color:red;">Project Covid</h2></body>', function(){ alertify.success('Ok'); });
// }
// function get_alert(){
//     alert("Please Click On Icon  ↗  To Get UI in New Window");
//     // document.getElementById("alerting").style.display="block";
//     }

var myVar;

function myFunction() {
  myVar = setTimeout(showPage, 3000);
}

function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("myDivload").style.display = "block";
  document.getElementById('mymarquee').start();
}