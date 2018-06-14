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
        destination = $(".data").data("profilepostcode"),
        modes = ['walking', 'bicycling', 'transit', 'driving'];

    /* User hasn't saved a postcode to their profile */
    if (destination === "None") {
        console.log("No postcode");
        return;
    }

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
    }, function (response) {
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
    console.log(response);
    const time = response.rows[0].elements[0].duration.text;
    $('.route.' + mode + ' .timeValue').html(time);
}

/* Hijacks the commute postcode form's submit event to update
 * the backend without a refresh. Also triggers commute time
 * calculations once the postcode has been saved. */
function initPostcodeForm() {
    const form = $('.postcodeForm');
    form.submit(function () {
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function () {
                const postcode = form.find('#id_postcode').val();
                /* Set the postcode mentioned on the page to the new value */
                $('.commuteTime .postcode').html(postcode);
                /* Update the data attribute used by the commute time function */
                $('.data').data('profilepostcode', postcode);
                /* Enable visual styles for when postcode isn't null */
                form.parent().removeClass('noPostcode');
                /* Recalculate and display commute times for new postcode */
                getCommuteTimes();
            },
            error: function (data) {
                console.log(data);
            }
        });
        return false;
    });
}

/* Hijack on-click behaviour for the save house link
 * in House view */
function initSavedHouseActions() {

    /* When the save/unsave link is clicked */
    $(".savedHouseAction").click(function () {
        const action = $(this),
              saved = action.data('issaved') === 'True';
        let url = action.data('saveurl');

        /* Pick the correct URL based on if the house
         * is currently saved or not */
        if (saved) {
            url = action.data('unsaveurl');
        }

        $.ajax({
            type: "GET",
            url: url,
            success: function () {
                if (saved) {
                    /* House was saved before, and we've just removed it. */
                    action.data('issaved', 'False');
                    action.html('Save House');
                } else {
                    /* House was not saved before, we've just saved it. */
                    action.data('issaved', 'True');
                    action.html('Remove Saved House');
                }
            },
            error: function (data) {
                console.log(data);
            }
        });
        return false;
    });
}

(function ($) {

    /* Initialise slick gallery */
    $('.galleryWrapper').slick();

    createVisualStars();
    initPostcodeForm();
    initSavedHouseActions();

    /* After a key is typed in the postcode box try and valdate */
    $('.postcodeForm').keyup(function (event) {
        validatePostcode()
    });

})(jQuery);