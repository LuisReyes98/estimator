function verificarExpiracion() {
    let switchB = document.getElementById("id_can_expire");
    let collapse = document.getElementById("id_can_expire_collapse");

    if (switchB.checked) {
        collapse.classList.add("show")
    } else {
        collapse.classList.remove("show")
    }

}
verificarExpiracion();