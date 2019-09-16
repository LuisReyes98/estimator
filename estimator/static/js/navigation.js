var toggled_navigation = true;
// var item = document.getElementsByClassName("app__item--hidden");
// var item2 = document.getElementsByClassName("nav-item");
// var item3 = document.getElementsByClassName("app__nav--link");

function mostrar() {
  let content = document.getElementById("content");
  let sidebar = document.getElementById("sidebar");
  if (toggled_navigation) {

    content.classList.toggle("active");
    sidebar.classList.toggle("nav__toggled")

  } else {
    sidebar.classList.toggle("nav__toggled")
    content.classList.toggle("active");

  }
  toggled_navigation = !toggled_navigation;
  postSidebarSession();
}

async function postSidebarSession() {
  let response = await fetch('/apiv1/session/sidebar/', {
    method: 'POST',
    body: {
      'hola': 'hola'
    },
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(function (res) {
    console.log(res);
  }
  );
}
