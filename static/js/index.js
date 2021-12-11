var mytime;

function therow() {
  if (localStorage.getItem("hasCodeRunBefore") === null) {
    mytime = setTimeout(showPage_wel, 0000);
    document.getElementById("myDivload-home").style.display = "block";
    document.getElementById('mymarquee-home').start();
    alertify.alert('', '<center><h1>Welcome</h1></center><br><center><h2 style="color:blue;">To The</h2><center><br><h2 style="color:red;">Project Covid</h2>');
    localStorage.setItem("hasCodeRunBefore", true);
    }
    else{
      // document.getElementById("welcome").style.display = "none";
      document.getElementById("myDivload-home").style.display = "block";
      document.getElementById('mymarquee-home').start();
      // alertify.alert('', '<center><h1>Welcome</h1></center><br><center><h2 style="color:blue;">To The</h2><center><br><h2 style="color:red;">Project Covid</h2>');
    }
    // document.getElementById("welcome").style.display="block";
  }
function showPage_wel() {
    // document.getElementById("welcome").style.display = "none";
    document.getElementById("myDivload-home").style.display = "block";
    document.getElementById('mymarquee-home').start();
    // alertify.alert('', '<center><h1>Welcome</h1></center><br><center><h2 style="color:blue;">To The</h2><center><br><h2 style="color:red;">Project Covid</h2>');
  // document.getElementById("alerting").style.display="block";
}
var logoutTimer = setTimeout(function() { sessionStorage.clear(); }, (60 * 60 * 1000));

// function therow() {
//   alertify.alert('', '<center><h1>Welcome</h1></center><br><center><h2 style="color:blue;">To The</h2><center><br><h2 style="color:red;">Project Covid</h2>');
// }
// var myVar1;

// function myFunction1() {
//   document.getElementById("myDivload1").style.display = "none";
//   document.getElementById("loader1").style.display = "flex";
//   document.getElementById("loader1").style.justifyContent = "center";
//   document.getElementById("loader1").style.alignItems = "center";
//   document.getElementById("loader1").style.margin = "0";
//   document.getElementById("loader1").style.minHeight = "100vh";   
//   myVar1 = setTimeout(showPage, 3000);
// }

// function showPage() {
//   document.getElementById("loader1").style.display = "none";
//   document.getElementById("myDivload1").style.display = "block";
//   // document.getElementById('mymarquee').start();
// }

var myHour = new Date();
myHour.setHours(myDate.getHours() + 1); //one hour from now
data.push(myHour);
localStorage.setItem('storedData', JSON.stringify(data))

function checkExpiration (){ 
    //check if past expiration date
        var values = JSON.parse(localStorage.getItem('storedData'));
    //check "my hour" index here
    if (values[1] < new Date()) {
        localStorage.removeItem("storedData")
    }
}

function myFunction1() {
    var myinterval = 15*60*1000; // 15 min interval
    setInterval(function(){ checkExpiration(); }, myinterval );
}

myFunction1();