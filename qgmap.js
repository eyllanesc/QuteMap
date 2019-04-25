// main var
var map;
var markers = [];
var qtWidget;
// main init function
function initialize() {
    var myOptions = {
        center: {lat: -34.397, lng: 150.644},
        zoom: 8
    };
    map = new google.maps.Map(document.getElementById('map_canvas'),
        myOptions);
    new QWebChannel(qt.webChannelTransport, function (channel) {
        qtWidget = channel.objects.qGoogleMap;
    });
    google.maps.event.addListener(map, 'dragend', function () {
        var center = map.getCenter();
        qtWidget.mapIsMoved(center.lat(), center.lng());
    });
    google.maps.event.addListener(map, 'click', function (ev) {
        qtWidget.mapIsClicked(ev.latLng.lat(), ev.latLng.lng());
    });
    google.maps.event.addListener(map, 'rightclick', function (ev) {
        qtWidget.mapIsRightClicked(ev.latLng.lat(), ev.latLng.lng());
    });
    google.maps.event.addListener(map, 'dblclick', function (ev) {
        qtWidget.mapIsDoubleClicked(ev.latLng.lat(), ev.latLng.lng());
    });
}
// custom functions
function gmap_setCenter(lat, lng) {
    map.setCenter(new google.maps.LatLng(lat, lng));
}
function gmap_getCenter() {
    return [map.getCenter().lat(), map.getCenter().lng()];
}
function gmap_setZoom(zoom) {
    map.setZoom(zoom);
}
function gmap_addMarker(key, latitude, longitude, parameters) {
    if (key in markers) {
        gmap_deleteMarker(key);
    }
    var coords = new google.maps.LatLng(latitude, longitude);
    parameters['map'] = map
    parameters['position'] = coords;
    var marker = new google.maps.Marker(parameters);
    google.maps.event.addListener(marker, 'dragend', function () {
        qtWidget.markerIsMoved(key, marker.position.lat(), marker.position.lng())
    });
    google.maps.event.addListener(marker, 'click', function () {
        qtWidget.markerIsClicked(key, marker.position.lat(), marker.position.lng())
    });
    google.maps.event.addListener(marker, 'dblclick', function () {
        qtWidget.markerIsDoubleClicked(key, marker.position.lat(), marker.position.lng())
    });
    google.maps.event.addListener(marker, 'rightclick', function () {
        qtWidget.markerIsRightClicked(key, marker.position.lat(), marker.position.lng())
    });
    markers[key] = marker;
    return key;
}
function gmap_moveMarker(key, latitude, longitude) {
    var coords = new google.maps.LatLng(latitude, longitude);
    markers[key].setPosition(coords);
}
function gmap_deleteMarker(key) {
    markers[key].setMap(null);
    delete markers[key]
}
function gmap_changeMarker(key, extras) {
    if (!(key in markers)) {
        return
    }
    markers[key].setOptions(extras);
}