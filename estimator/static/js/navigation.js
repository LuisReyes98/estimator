function mostrar() {
  let content = document.getElementById("content");
  let sidebar = document.getElementById("sidebar");

  if (sidebar_extended) {
    content.classList.remove("active");
    sidebar.classList.remove("nav__toggled");

  }else{
    content.classList.add("active");
    sidebar.classList.add("nav__toggled");
  }

  postSidebarSession(sidebar_extended);
  sidebar_extended = !sidebar_extended;
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function postSidebarSession(value) {
  let response = await fetch('/apiv1/session/sidebar_extended/', {
    method: 'POST',
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Accept": "application/json",
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'value': value,
    }),
  }).then()
  .catch(error => {});
}
mostrar();