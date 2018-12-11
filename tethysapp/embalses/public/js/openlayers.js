function ol_map() {
    /*basemap for the map*/
    var basemap = new ol.layer.Tile({
        source: new ol.source.BingMaps({
            key: 'eLVu8tDRPeQqmBlKAjcw~82nOqZJe2EpKmqd-kQrSmg~AocUZ43djJ-hMBHQdYDyMbT-Enfsk0mtUIGws1WeDuOvjY4EXCH-9OK3edNLDgkc',
            imagerySet: 'AerialWithLabels'
        })
    });

    /*initial view for the map. You can change the view by changing the lat,long or zoom */
    var view = new ol.View({
        center: ol.proj.transform([-70.6, 18.8], 'EPSG:4326', 'EPSG:3857'),
        minZoom: 2,
        maxZoom: 18,
        zoom: 8.3
    });


    /*getting the specific parts that will be used by the popup*/
    var container = document.getElementById('popup');
    var content = document.getElementById('popup-content');
    var closer = document.getElementById('popup-closer');

    /*information for popup*/
    var overlay = new ol.Overlay({
        element: container,
        autoPan: true,
        autoPanAnimation: {
            duration: 250
        }
    });

    /*closes popup on click*/
    //closer.onclick = function() {
    //    overlay.setPosition(undefined);
    //    closer.blur();
    //    return false;
    //};


    /*creates the map with the specified views, layers, and popups from above*/
    map = new ol.Map({
        target: 'map',
        view: view,
        layers: [basemap],
        overlays: [overlay],
    });

    /*searched for the reservoir layer on the geoserver and grabs it. This will need to be changed when installed on a different computer*/
    var wmsLayer = new ol.layer.Image({
        source: new ol.source.ImageWMS({
            url: 'http://tethys-staging.byu.edu:8181/geoserver/wms',
            params: { 'LAYERS': 'reservoirs' },
            serverType: 'geoserver',
            crossOrigin: 'Anonymous'
        })
    });
    map.addLayer(wmsLayer);


    /*when the cursor is a pointer, the following code is ran*/
    //map.on("singleclick", function(evt) {
    //
    //    var pixel = map.getEventPixel(evt.originalEvent);
    //    var hit = map.forEachLayerAtPixel(pixel, function(layer) {
    //        if (layer != layers[0] && layer != layers[1] && layer != layers[2] && layer != layers[3]) {
    //            current_layer = layer;
    //            return true;
    //        }
    //    });
    //    /*getting the necessary information to pull information from the point in the shapefile*/
    //    var view = map.getView();
    //    var viewProjection = view.getProjection();
    //    var viewResolution = view.getResolution();
    //    var wms_url = wmsLayer.getSource().getGetFeatureInfoUrl(evt.coordinate, viewResolution, viewProjection, { 'INFO_FORMAT': 'text/javascript', }); //Get the wms url for the clicked point
    //    /*if the point really is the shapfile then the code will get the information and pull out the NAME*/
    //    if (wms_url) {
    //        var parser = new ol.format.GeoJSON();
    //        $.ajax({
    //            url: wms_url,
    //            dataType: 'jsonp',
    //            jsonpCallback: 'parseResponse'
    //        }).then(function(response) {
    //            res_name = response['features'][0]['properties']['NAME']
    //            if (res_name == "Sabana Yegua") {
    //                res_name = 'S. Yegua';
    //            } else if (res_name == "Tavera-Bao") {
    //                res_name = 'Tavera';
    //            }
    //            var coord = response['features'][0]['geometry']['coordinates']
    //            var coordinate = evt.coordinate;
    //            var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
    //                coordinate, 'EPSG:3857', 'EPSG:4326'));
    //
    //            $.ajax({
    //                url: `/apps/embalses/getrecentdata/`,
    //                type: 'GET',
    //                data: { 'res': res_name },
    //                contentType: 'application/json',
    //                error: function(status) {
    //
    //                },
    //                success: function(response) {
    //                    lastdate = response['lastdate']
    //                    lastlevel = response['lastlevel']
    //                    /*this is what appears in the popup*/
    //                    content.innerHTML = '<h3>' + res_name + '</h3><br><p> Ultimo dia de ingresar = ' + lastdate + '</p><br><p> Nivel de Agua = ' + lastlevel + ' </p>';
    //                    overlay.setPosition(coordinate);
    //                }
    //            })
    //
    //        });
    //    }
    //});
    //map.on("dblclick", function(evt) {
    //    if (res_name == "S. Yegua") {
    //        res_name = 'Sabana_Yegua';
    //    }
    //    location.href = apiServer + res_name
    //    goToURL()
    //
    //});
}