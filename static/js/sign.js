const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('modal-container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("btn-close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// }
// ---------------------------------------------------------------------------------------------------------------
// var modal1 = document.getElementById("myModal1");
// function present(){
//   modal1.style.display = "block";
// }
// var span1 = document.getElementsByClassName("close1")[0];

// When the user clicks on <span> (x), close the modal
// span1.onclick = function() {
//   modal1.style.display = "none";
// }

// When the user clicks anywhere outside of the modal, close it
// window.onclick = function(event) {
//   if (event.target == modal1) {
//     modal1.style.display = "none";
//   }
// }
const switchForm = (form) => {
  if(form == 'register'){
      if(window.innerWidth <= 570){
        document.getElementById("sign-up").style.zIndex = "300";
        document.getElementById("sign-up").style.opacity = "1";
        document.getElementById("sign-in").style.zIndex = "-1";
        document.getElementById("sign-in").style.opacity = "0";
      }
      // loginForm.style.marginLeft = `-150%`;
      // registerFrom.style.marginLeft = `-100%`;
  } else{
      if(window.innerWidth <= 570){
        document.getElementById("sign-up").style.zIndex = "-1";
        document.getElementById("sign-up").style.opacity = "0";
        document.getElementById("sign-in").style.zIndex = "300";
        document.getElementById("sign-in").style.opacity = "1";
      }
      // loginForm.style.marginLeft = `0%`;
      // registerFrom.style.marginLeft = `50%`;
  }
}