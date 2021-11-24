var mytime;

function therow() {
    mytime = setTimeout(showPage_wel, 7000);
    // document.getElementById("welcome").style.display="block";
  }

function showPage_wel() {
  document.getElementById("welcome").style.display = "none";
  document.getElementById("myDivload-home").style.display = "block";
  document.getElementById('mymarquee-home').start();
  alertify.alert('Team Infy SOARS Presents', '<center><h1>Welcome</h1></center><br><center><h2 style="color:blue;">To The</h2><center><br><h2 style="color:red;">Project Covid</h2>', function(){ alertify.success('Ok'); });
  // document.getElementById("alerting").style.display="block";
}