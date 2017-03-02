//Marker placement based on this tutorial:
      //https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete
      function placeMarkers(results){
        clearMarkers();
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
          //google.maps.event.addListener(markers[i], 'click', showInfoWindow);
         setTimeout(dropMarker(i),0)
          //addResult(results[i], i);
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
