function objectsToRawMaterials(entryObj) {
    let result = Array(entryObj.length);
    entryObj.forEach(function (el, index) {
        result[index] = new RawMaterial(
            el.pk,
            el.raw_material_pk,
            el.name,
            el.amount, // amount
            el.measurement_unit,
            el.bought_in_dollars, //bought_in_dollars
            el.cost_dollar, //cost_dollar
            el.cost_local, //cost_local
            el.provider,
            el.providers_list,
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