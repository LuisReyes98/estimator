var click = true;
var item = document.getElementsByClassName("app__item--hidden");
var item2 = document.getElementsByClassName("nav-item");
var item3 = document.getElementsByClassName("app__nav--link");

function mostrar() {
  if (click) {
    document.getElementById("sidebar").style.width = "50px";
    document.getElementById("content").style.marginLeft = "50px";
    document.getElementById("nav_menu").style.borderBottom =
      "solid 1px rgba(0,0,0,0)";
    document.getElementById("arrow").style.transform = "rotate(-180deg)";

    for (let i = 0; i < item.length; i++) {
      item[i].style.marginLeft = "-17rem";
    }

    for (let i = 0; i < item2.length; i++) {
      item2[i].style.width = "50px";
    }

    for (let i = 0; i < item3.length; i++) {
      item3[i].classList.toggle("app__tooltip");
    }
    click = false;
  } else {
    document.getElementById("sidebar").style.width = "17rem";
    document.getElementById("content").style.marginLeft = "17rem";
    document.getElementById("nav_menu").style.borderBottom =
      "solid 1px #383838";
    document.getElementById("arrow").style.transform = "rotate(0deg)";

    for (let i = 0; i < item.length; i++) {
      item[i].style.marginLeft = "0";
    }

    for (let i = 0; i < item2.length; i++) {
      item2[i].style.width = "17rem";
    }

    for (let i = 0; i < item3.length; i++) {
      item3[i].classList.toggle("app__tooltip");
    }

    click = true;
  }
}
