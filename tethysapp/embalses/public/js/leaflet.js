function leaf_map() {
    // creating the map
    var map = L.map('map', {
        zoom: 8.25,
        minZoom: 1.25,
        boxZoom: true,
        maxBounds: L.latLngBounds(L.latLng(-100.0,-270.0), L.latLng(100.0, 270.0)),
        center: [19, -70.6],
    });

    var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');
    var Esri_Imagery_Labels = L.esri.basemapLayer('ImageryLabels');
    basemaps = {"Basemap": L.layerGroup([Esri_WorldImagery, Esri_Imagery_Labels]).addTo(map)}

    lyrControls = L.control.layers(basemaps).addTo(map);

    function onEachFeature(feature, layer) {
        layer.bindPopup(feature.properties.NAME);
    }

    L.geoJSON(locations, {
        onEachFeature: onEachFeature,
    }).addTo(map);
}