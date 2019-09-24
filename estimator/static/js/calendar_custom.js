document.addEventListener("DOMContentLoaded", function() {
  (function calendario() {
    let calendarioTitulo = Array.from(
      document.getElementsByClassName("fc-center")
    )[0].childNodes[0].childNodes[1];

    let botonIzquierdo = Array.from(
        document.getElementsByClassName("fc-center")
      )[0].childNodes[0].childNodes[0];

      let botonDerecho = Array.from(
        document.getElementsByClassName("fc-center")
      )[0].childNodes[0].childNodes[2];

      let botonPrevYear = Array.from(
        document.getElementsByClassName("fc-left")
      )[0].childNodes[0];

      let contenedorDerecho = Array.from(
        document.getElementsByClassName("fc-right")
      )[0];

      let botonNextYear = Array.from(
        document.getElementsByClassName("fc-right")
      )[0].childNodes[1];

      let botonToday = Array.from(
        document.getElementsByClassName("fc-right")
      )[0].childNodes[0];

    calendarioTitulo.classList.add("text-uppercase");
    calendarioTitulo.classList.add("calendar-title");
    calendarioTitulo.classList.add("font-weight-bold");

    botonIzquierdo.classList.add("app__button--icon");
    botonIzquierdo.classList.add("calendar-button");
    botonIzquierdo.classList.add("mdl-button");
    botonIzquierdo.classList.add("mdl-js-button");
    botonIzquierdo.classList.add("mdl-button--icon");

    botonDerecho.classList.add("app__button--icon");
    botonDerecho.classList.add("calendar-button");
    botonDerecho.classList.add("mdl-button");
    botonDerecho.classList.add("mdl-js-button");
    botonDerecho.classList.add("mdl-button--icon");

    botonPrevYear.classList.add("app__button--icon");
    botonPrevYear.classList.add("calendar-button_year");
    botonPrevYear.classList.add("mdl-button");
    botonPrevYear.classList.add("mdl-js-button");
    botonPrevYear.classList.add("mdl-button--icon");

    contenedorDerecho.classList.add("calendar-container_fc-right");

    botonNextYear.classList.add("app__button--icon");
    botonNextYear.classList.add("calendar-button_year");
    botonNextYear.classList.add("mdl-button");
    botonNextYear.classList.add("mdl-js-button");
    botonNextYear.classList.add("mdl-button--icon");

    botonToday.classList.add("calendar-button_today");
    botonToday.classList.add("text-uppercase");
    botonToday.classList.add("small");
    botonToday.classList.add("font-weight-bold");
    // botonIzquierdo.classList.add("position-absolute")
    // calendarioTitulo.forEach(el => {
    // });
  })();
});
