/////////////////////////////////////////////////////////////////// HOME PAGE
function dataOverview() {
    $.ajax({
        url:'/apps/embalses/ajax/overviewpage/',
        data: 'get some infos',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(results) {
            tabulatorResStats(results['result']);
            }
        })
}

/////////////////////////////////////////////////////////////////// HISTORICAL RESERVOIR DATA PAGE
function getChart() {
    $.ajax({
        url:'/apps/embalses/ajax/respgplot/',
        data: 'please make me a chart',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(result) {
            newHighchart(result);
            }
        });
}

function statisticalReport() {
    $.ajax({
        url:'/apps/embalses/ajax/reservoirstatistics/',
        data: 'get some stats yo',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(results) {
            console.log(results);
            $("#volumes").append("<h2>Volumes</h2>");
            $("#elevations").append("<h2>Elevaciones</h2>");
            $("#averages").append("<h2>Promedios</h2>");
            for (var key in results['volumes']) {
                $("#volumes").append("<li>" + key + ": " + results['volumes'][key] + "</li>");
            }
            for (var key in results['elevations']) {
                $("#elevations").append("<li>" + key + ": " + results['elevations'][key] + "</li>");
            }
            for (var key in results['averages']) {
                $("#averages").append("<li>" + key + ": " + results['averages'][key] + "</li>");
            }
        }
    })
}

/////////////////////////////////////////////////////////////////// SHORT TERM SIMULATIONS PAGE
function simulationTable() {
    $.ajax({
        url:'/apps/embalses/ajax/simulationTable/',
        data: $("#reservoir").val(),
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(info) {
            var outflowtable = tabulatorOutflows(info['result']);
            $("#calculatebutton").html("<button id='button' onclick='performsimulation()' class='button'>Hacer un Pronostico</button>");
            return outflowtable;
            }
        })
}

function performsimulation() {
    $("#numericalresults").html('');
    $("#warningresults").html('');
    $("#statisticalresults").html('');
    $("#calculatebutton").html("<img src='https://media.giphy.com/media/8RyJliVfFM6ac/giphy.gif' style='width: 200px'>");
    $.ajax({
        url:'/apps/embalses/ajax/performsimulation/',
        data: JSON.stringify(outflowtable.getData()),
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(simulationresults) {
            // Replace the Calculate Button
            $("#calculatebutton").html("<button id='button' onclick='performsimulation()' class='button'>Hacer un Pronostico</button>");

            // Fill the numerical results table
            $("#numericalresults").html('<h3 style="text-align: center">Resultados Numericos</h3><table id="resultstable">');
            for (var key in simulationresults['numericalresults']) {
                $("#numericalresults").append("<tr><td>" + key + "</td><td>" + simulationresults['numericalresults'][key] + "</td></tr>");
            }
            $("#numericalresults").append("</table>");

            // Fill a bullet list of warnings
            $("#warningresults").html('<h3 style="text-align: center">Avisos Sobre Pronostico</h3>');
            for (var key in simulationresults['warningresults']) {
                $("#warningresults").append("<li>" + key + ": " + simulationresults['warningresults'][key] + "</li>");
            }

            // Fill the graphic warnings
            $("#statisticalresults").html('<h3 style="text-align: center">Statisticas del Embalse</h3>');
            for (var key in simulationresults['statisticalresults']) {
                $("#statisticalresults").append("<h5>" + key + "</h5>" + "<ul>");
                for (var subkey in simulationresults['statisticalresults'][key]){
                    $("#statisticalresults").append("<li>" + subkey + ": " + simulationresults['statisticalresults'][key][subkey] + "</li>");
                }
                $("#statisticalresults").append("</ul>");
            }

            }
        })
}

/////////////////////////////////////////////////////////////////// REPORT RESERVOIR LEVELS PAGE
function updatesheet() {
    $.ajax({
        url:'/apps/embalses/ajax/updatesheet/',
        data: 'getting new data from google',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(status) {
            console.log(status);
            }
        })
}
