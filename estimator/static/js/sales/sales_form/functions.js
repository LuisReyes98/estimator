function objectsToRawMaterials(entryObj) {
    let result = Array(entryObj.length);
    entryObj.forEach(function (el, index) {
        result[index] = new RawMaterial(
            el.pk,
            el.name,
            el.amount, // amount
            el.measurement_unit,
            el.isBoughtInDollars, //isBoughtInDollars
            el.cost_dollar, //cost_dollar
            el.cost_local //cost_local
        );
    });
    return result;
}

function selectedMaterials(entryObj) {
    let result = Array(entryObj.length);
    entryObj.forEach(function (el, index) {
        result[index] = el.pk.toString();
    });
    return result;
}