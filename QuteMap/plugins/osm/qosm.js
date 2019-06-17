// main var
var map;
var markers = [];
var handler;
// main init function
function initialize() {
	map = L.map('mapid');
    map.on('load', function(){
        console.log("loading");
    });
    map.setView([0, 0], 1);
	L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);

	new QWebChannel(qt.webChannelTransport, function (channel) {
        handler = channel.objects.map_handler;
        init();
    });
    map.on('move', function () {
        var center = map.getCenter();
        handler.updateCenterFromMap(center.lat, center.lng);
    });
    map.on('zoom', function () {
        handler.updateZoomFromMap(map.getZoom());
    });
}

function init(){
    var center = map.getCenter();
    handler.updateCenterFromMap(center.lat, center.lng);
    handler.updateZoomFromMap(map.getZoom());
}

// map
function setCenter(latitude, longitude){
    console.log(`setCenter: ${latitude}, ${longitude}`);
    map.setView([latitude, longitude]);
}

function setZoom(zoom){
    // console.log(`setZoom: ${zoom}`);
    map.setZoom(zoom);
}