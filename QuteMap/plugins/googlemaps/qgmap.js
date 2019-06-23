// main var
var map;
var markers = [];
var handler;
// main init function
function initialize() {
	var location = {{center}}
	var myOptions = {
		center: {lat: location[0], lng: location[1]},
		zoom: {{zoom}}
	};
	map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);
	
	new QWebChannel(qt.webChannelTransport, function (channel) {
		handler = channel.objects.qutemap_handler;
		init();
	});
	
	// console.log("add center_changed listener")
	map.addListener('center_changed', function() {
		var center = new google.maps.LatLng(map.getCenter().lat(), map.getCenter().lng(),  false);
		handler.updateCenterFromMap(center.lat(), center.lng());
	});
	// console.log("add zoom_changed listener")
	map.addListener('zoom_changed', function(){
		handler.updateZoomFromMap(map.getZoom())
	});
}


function init(){
	var center = map.getCenter();
	handler.updateCenterFromMap(center.lat(), center.lng());
	handler.updateZoomFromMap(map.getZoom());
}

// map
function setCenter(latitude, longitude){
	console.log(`setCenter: ${latitude}, ${longitude}`);
	var coords = new google.maps.LatLng(latitude, longitude);
	map.setCenter(coords);
}

function setZoom(zoom){
	// console.log(`setZoom: ${zoom}`);
	map.setZoom(zoom);
}

// markers
function addMarker(name, latitude, longitude, parameters){
	var coords = new google.maps.LatLng(latitude, longitude);
	parameters['map'] = map;
	parameters['position'] = coords;
	var marker = new google.maps.Marker(parameters);
	google.maps.event.addListener(marker, 'position_changed', function() {
		var position = marker.getPosition()
		handler.updateMarkerPosition(name, position.lat(), position.lng())
	});
	markers[name] = marker;
}

function moveMarker(name, latitude, longitude){
	if (name in markers) {
		var coords = new google.maps.LatLng(latitude, longitude);
		markers[name].setPosition(coords);
	}
}

function changeMarkerParameters(name, parameters){
	if (!(name in markers)) {
		return
	}
	markers[name].setOptions(parameters);
}