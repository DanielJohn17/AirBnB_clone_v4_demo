$("document").ready(function() {
    const obj_dict = {};
    $("button#buttons").click(function() {
        $("h1").text("Hello Daniel!");
        $("h1").css("color", "Red");
    });

    $("ul > input").on("change", function (){
        if ($(this).is(":checked")) {
            obj_dict[$(this).attr("data-id")] = $(this).attr("data-name");
        }
        else {
            delete obj_dict[$(this).attr("data-id")];
        }
        const names = Object.values(obj_dict);
        $("div.show").text(names.sort().join(', '));
    });

});