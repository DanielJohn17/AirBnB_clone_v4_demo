$("document").ready(function () {
    let checked_amen = {};
    $(".popover input").on("change", function () {
        if ($(this).is(":checked")) {
            checked_amen[$(this).attr("data-id")] = $(this).attr("data-name");
        }
        else if ($(this).is(":not(:checked)")) {
            delete checked_amen[$(this).attr("data-id")]
        }

        const names = [];
        for (let key in checked_amen){
            names.push(checked_amen[key]);
        }
        if (names.length > 0)
            $(".amenities > h4").text(names.sort().join(', '));
        else
            $(".amenities > h4").html("&nbsp;");
    });

    $.get('http://0.0.0.0:5001/api/v1/status/', function (data, textStatus) {
        if (textStatus === 'success') {
            if (data.Status === 'OK') {
                $('#api_status').addClass('available');
            } else {
                $('#api_status').removeClass('available');
            }
        }
      });
    
});