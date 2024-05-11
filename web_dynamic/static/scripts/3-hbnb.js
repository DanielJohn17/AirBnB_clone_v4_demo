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
    
    $.ajax(
        {
            type: "POST",
            url: 'http://0.0.0.0:5001/api/v1/places_search',
            data: '{}',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                for (let i = 0; i < data.length; i++) {
                  let place = data[i];
                  $('.places ').append('<article><h2>' + place.name + '</h2><div class="price_by_night"><p>$' + place.price_by_night + '</p></div><div class="information"><div class="max_guest"><div class="guest_image"></div><p>' + place.max_guest + '</p></div><div class="number_rooms"><div class="bed_image"></div><p>' + place.number_rooms + '</p></div><div class="number_bathrooms"><div class="bath_image"></div><p>' + place.number_bathrooms + '</p></div></div><div class="description"><p>' + place.description + '</p></div></article>');
                }
            }
        }
    );
    
});