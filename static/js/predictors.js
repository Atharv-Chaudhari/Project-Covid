function sympred() {
    document.getElementById("formFour").style.display = "block";
    document.getElementById("active-it1").style.color = "white";
    document.getElementById("active-it3").style.color = "white";
    document.getElementById("active-it1").style.backgroundColor = "#43f943";
    document.getElementById("active-it2").style.color = "lime";
    document.getElementById("active-it4").style.color = "lime";
    document.getElementById("active-it2").style.backgroundColor = "white";
    document.getElementById("formSeven").style.display = "none";
    document.getElementById("hide_pred2").style.display = "none";
    document.getElementById("switch-it").checked=false;
    nhamnham();
}
function imgpred() {
    document.getElementById("formFour").style.display = "none";
    document.getElementById("active-it2").style.color = "white";
    document.getElementById("active-it4").style.color = "white";
    document.getElementById("active-it2").style.backgroundColor = "#43f943";
    document.getElementById("active-it1").style.color = "lime";
    document.getElementById("active-it1").style.backgroundColor = "white";
    document.getElementById("active-it3").style.color = "lime";
    document.getElementById("formSeven").style.display = "block";
    document.getElementById("hide_pred").style.display = "none";
    document.getElementById("switch-it").checked=true;
}
function nhamnham() {
    if (document.getElementById("switch-it").checked) {
        document.getElementById("formFour").style.display = "none";
        document.getElementById("formSeven").style.display = "block";
        document.getElementById("hide_pred").style.display = "none";
    } else {
        document.getElementById("formFour").style.display = "block";
        document.getElementById("formSeven").style.display = "none";
        document.getElementById("hide_pred2").style.display = "none";
    }
}
function changeityar() {
    var decider = document.getElementById('checkitman');
    if (decider.checked) {
        document.getElementById("hideitman1").style.display = "none";
        document.getElementById("hideitman2").style.display = "none";
        document.getElementById("hide_pred2").style.display = "none";
        document.getElementById("hide_pred3").style.display = "block";
        document.getElementById("hideitman3").style.display = "flex";
        document.getElementById("hideitman4").style.display = "flex";
    } else {
        document.getElementById("hideitman1").style.display = "flex";
        document.getElementById("hideitman2").style.display = "flex";
        document.getElementById("hide_pred2").style.display = "block";
        document.getElementById("hide_pred3").style.display = "none";
        document.getElementById("hideitman3").style.display = "none";
        document.getElementById("hideitman4").style.display = "none";
    }
}