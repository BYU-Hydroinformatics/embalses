function leaf_map() {
    // creating the map
    var map = L.map('map', {
        zoom: 8.25,
        minZoom: 1.25,
        boxZoom: true,
        maxBounds: L.latLngBounds(L.latLng(-100.0,-270.0), L.latLng(100.0, 270.0)),
        center: [19, -70.6],
    });

    // create the basemap layers (default basemap is world imagery)
    var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');
    var Esri_WorldTerrain = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}', {maxZoom: 13});
    var openStreetMap = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
       attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
       name: 'openStreetMap',
        }).addTo(map);

    basemaps = {
        "ESRI Imagery": Esri_WorldImagery,
        "ESRI Terrain": Esri_WorldTerrain,
        "OpenStreetMap": openStreetMap,
        };
    lyrControls = L.control.layers(basemaps).addTo(map);

    function onEachFeature(feature, layer) {
        layer.bindPopup(feature.properties.NAME);
    }

    L.geoJSON(locations, {
        onEachFeature: onEachFeature,
    }).addTo(map);
}