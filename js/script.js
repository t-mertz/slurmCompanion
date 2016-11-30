function set_value() {
    $("#value_form").css("display", "table-row");
    $(".range_form").css("display", "none");
}

function set_range() {
    $(".range_form").css("display", "table-row");
    $("#value_form").css("display", "none");
}

function add_parameter() {
    var newdiv = document.createElement("div");
    var newnode = document.createTextNode("test");
    newdiv.appendChild(newnode);

    document.getElementById("parameter-form").appendChild(newdiv);
}