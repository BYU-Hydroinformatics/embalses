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
            $("#volumes").append("<h3>Volumes</h3>");
            $("#elevations").append("<h3>Elevaciones</h3>");
            $("#averages").append("<h3>Promedios</h3>");
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
        data: 'setting up the simulation table',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(dates) {
            console.log(dates);
            tabulatorOutflows(dates['result']);
            $.ajax({
                url:'/apps/embalses/ajax/getSFPTflows/',
                data: $("#reservoir").val(),
                dataType: 'json',
                contentType: "application/json",
                method: 'POST',
                success: function(flows) {
                    console.log(flows);
                    // add the flows to the simulation table
                    // prompt the user to fill out the outflows, units, and times
                    // add the calculate button to the page or make it visible if its already there on the html
                    }
                })
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
