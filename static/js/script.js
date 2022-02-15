// Other important pens.
// Map: https://codepen.io/themustafaomar/pen/ZEGJeZq
// Dashboard: https://codepen.io/themustafaomar/pen/jLMPKm

let dropdowns = document.querySelectorAll('.navbar .dropdown-toggler')
let dropdownIsOpen = false

// Handle dropdown menues
if (dropdowns.length) {
    // Usually I don't recommend doing this (adding many event listeners to elements have the same handler)
    // Instead use event delegation: https://javascript.info/event-delegation
    // Why: https://gomakethings.com/why-event-delegation-is-a-better-way-to-listen-for-events-in-vanilla-js
    // But since we only have two dropdowns, no problem with that. 
    dropdowns.forEach((dropdown) => {
        dropdown.addEventListener('click', (event) => {
            let target = document.querySelector(`#${event.target.dataset.dropdown}`)

            if (target) {
                if (target.classList.contains('show')) {
                    target.classList.remove('show')
                    dropdownIsOpen = false
                } else {
                    target.classList.add('show')
                    dropdownIsOpen = true
                }
            }
        })
    })
}

// Handle closing dropdowns if a user clicked the body
window.addEventListener('mouseup', (event) => {
    if (dropdownIsOpen) {
        dropdowns.forEach((dropdownButton) => {
            let dropdown = document.querySelector(`#${dropdownButton.dataset.dropdown}`)
            let targetIsDropdown = dropdown == event.target

            if (dropdownButton == event.target) {
                return
            }

            if ((!targetIsDropdown) && (!dropdown.contains(event.target))) {
                dropdown.classList.remove('show')
            }
        })
    }
})

// Open links in mobiles
function handleSmallScreens() {
    document.querySelector('.navbar-toggler')
        .addEventListener('click', () => {
            let navbarMenu = document.querySelector('.navbar-menu')

            if (navbarMenu.style.display === 'flex') {
                navbarMenu.style.display = 'none'
                return
            }

            navbarMenu.style.display = 'flex'
        })
}

handleSmallScreens()

var modal_risk = document.getElementById("risk-myModal");
var modal = document.getElementById("myModal");
// Get the button that opens the modal
var btn_risk = document.getElementById("risk-myBtn");

// Get the <span> element that closes the modal
var span_risk = document.getElementsByClassName("close-risk")[0];

// When the user clicks the button, open the modal 
btn_risk.onclick = function() {
  modal_risk.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span_risk.onclick = function() {
  modal_risk.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal_risk) {
    modal_risk.style.display = "none";
  }
  if (event.target == modal) {
        modal.style.display = "none";
    }
}
