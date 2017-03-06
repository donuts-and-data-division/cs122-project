//Marker placement based on this tutorial:
//https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete

var markers = [];
var MARKER_PATH = 'https://developers.google.com/maps/documentation/javascript/images/marker_green';


function placeMarkers(results){
  clearMarkers();
  clearResults();
  // Create a marker for each hotel found, and
  // assign a letter of the alphabetic to each marker icon.
  for (var i = 0; i < results.length; i++) {
    var markerLetter = String.fromCharCode('A'.charCodeAt(0) + (i % 26));
    var markerIcon = MARKER_PATH + markerLetter + '.png';

 
    // Use marker animation to drop the icons incrementally on the map.
    markers[i] = new google.maps.Marker({
      position: new google.maps.LatLng(results[i].geometry.coordinates[1], results[i].geometry.coordinates[0]),
      animation: google.maps.Animation.DROP,
      icon: markerIcon
    });
    // If the user clicks a hotel marker, show the details of that hotel
    // in an info window.
    
    markers[i].placeResult = results[i];
    google.maps.event.addListener(markers[i], 'click', showInfoWindow);
    setTimeout(dropMarker(i), 0);
    addResult(results[i], i);
      }
  }

function clearMarkers() {
  for (var i = 0; i < markers.length; i++) {
    if (markers[i]) {
      markers[i].setMap(null);
    }
  }
      markers = [];
  }

function dropMarker(i) {
  return function() {
    markers[i].setMap(map);
  };}

function geolocate() {
  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function (position) {
        var geolocation = new google.maps.LatLng(
        position.coords.latitude, position.coords.longitude);

        var latitude = position.coords.latitude;
        var longitude = position.coords.longitude;
        document.getElementById("latitude").value = latitude;
        document.getElementById("longitude").value = longitude;
        autocomplete.setBounds(new google.maps.LatLngBounds(geolocation, geolocation));
  });}
    }


      function addResult(result, i) {
        var results = document.getElementById('results');
        var markernumber = String.fromCharCode('A'.charCodeAt(0) + (i % 26));
        var markerIcon = MARKER_PATH + markernumber + '.png';

        var tr = document.createElement('tr');
        tr.style.backgroundColor = (i % 2 === 0 ? '#F0F0F0' : '#FFFFFF');
        tr.onclick = function() {
          google.maps.event.trigger(markers[i], 'click');
        };

        var iconTd = document.createElement('td');
        var nameTd = document.createElement('td');
        var icon = document.createElement('img');
        icon.src = markerIcon;
        icon.setAttribute('class', 'placeIcon');
        icon.setAttribute('className', 'placeIcon');
        var name = document.createTextNode(result.properties.store_name);
        console.log(name)
        iconTd.appendChild(icon);
        nameTd.appendChild(name);
        tr.appendChild(iconTd);
        tr.appendChild(nameTd);
        results.appendChild(tr);
      }

      function showInfoWindow() {
      var marker = this;
      infoWindow.open(map, marker);
      var place = marker.placeResult.properties;
      console.log(place)
      buildIWContent(place);
      }
 
      function clearResults() {
        var results = document.getElementById('results');
        while (results.childNodes[0]) {
          results.removeChild(results.childNodes[0]);
        }
      }

    
      function buildIWContent(place) {
        document.getElementById('iw-name').textContent = place.store_name;
        document.getElementById('iw-address').textContent = place.address;  


        $('#submit_groceries').click(function() {
        var place_id = place.place_id;
        var url = '/groceries/' + place_id + '/';
        window.location.href = url;
        }); 
      }