function initMapping() {
    getCommuteTimes();
    getNearestShops();
}

/* Returns the postcode for the current house */
function getPostcode() {
    return $('.houseAddress').data('postcode');
}

/* Retrieves the time taken to commute to the destination
 * via 4 different methods and inserts it into the page. */
function getCommuteTimes() {
    const origin = getPostcode(),
        destination = 'SW7 2AZ',
        modes = ['walking', 'bicycling', 'transit', 'driving'];

    modes.forEach(function (mode) {
        const service = new google.maps.DistanceMatrixService();
        service.getDistanceMatrix({
            origins: [origin],
            destinations: [destination],
            travelMode: mode.toUpperCase()
        }, (response, status) => insertCommuteTimes(mode, response));
    });
}

function getNearestShops() {
    geocodeAddress(getPostcode(), insertNearestShops);
}

/* Takes an address, converts it to LatLng and passes it to callback */
function geocodeAddress(address, callback) {
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address': address}, function (results, status) {
        if (status === 'OK') {
            const location = results[0].geometry.location,
                  coords = {lat: location.lat(), lng: location.lng()};
            callback(coords);
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

function insertNearestShops(location) {
    const service = new google.maps.places.PlacesService(document.querySelector('.mapsHook'));
    service.nearbySearch({
        location: new google.maps.LatLng(location),
        radius: 1000,
        type: ['store']
    }, function(response) {
        window.rsp = response;
        for (let i = 0; i < response.length; i++) {
            let place = response[i];
            if (place.types.includes('grocery_or_supermarket')) {
                const shop = $("<li/>").addClass('shop'),
                      icon = $("<i class='far fa-store'></i>"),
                      shopName = $("<span/>").addClass('shopName').html(place.name);
                shop.appendTo('.shops');
                icon.appendTo(shop);
                shopName.appendTo(shop);
            }
        }
    });
}

/* Parses commute time response and injects it into the DOM */
function insertCommuteTimes(mode, response) {
    const time = response.rows[0].elements[0].duration.text;
    $('.route.' + mode + ' .timeValue').html(time);
}

(function ($) {

    /* Converts text rating values into visual stars using BarRating.js */
    function createVisualStars() {
        const starFields = $('.createStars');
        starFields.each(function (i, field) {
            /* Wrap the star field in a jQuery object */
            field = $(field);

            /* Retrieve the number of stars the field contains
            *  and generate HTML for the select field needed to
            *  display visual stars */
            const value = parseInt(field.html()),
                select = $('<select/>').addClass('starRating');

            /* If the value couldn't be parsed, the field wasn't filled
             * out in the review, so don't display this review point. */
            if (isNaN(value)) {
                field.parent('.reviewPoint').remove();
                return;
            }

            /* Append <option> tags with values 1-5 to the select field */
            for (let i = 1; i <= 5; i++) {
                const option = $("<option/>").html(i);

                /* Mark the option that matches the number of stars
                 * we want to display as "selected" */
                if (i === value) {
                    option.attr('selected', 'true');
                }

                select.append(option);
            }

            /* Insert the select tag and remove the original text field */
            select.insertAfter(field);
            field.remove();

            /* Initialise the bar rating plugin to display stars
             * for the select field */
            select.barrating({
                theme: 'fontawesome-stars',
                readonly: true
            })
        })
    }

    /* Initialise slick gallery */
    $('.galleryWrapper').slick();

    createVisualStars();
})(jQuery);