function getChart() {
    $.ajax({
        url:'/apps/embalses/ajax/respageinfo/',
        data: 'please make me a chart',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(result) {
            newHighchart(result);
            }
        });
}


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
                    }
                })
            }
        })
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
            for (entry in results['volumes']) {
                console.log(entry);
                console.log(results['volumes'][entry]);
                $("#volumes").innerHTML += "<li>" + entry + ": " + results['volumes'][entry] + "</li>";
            }
            for (entry in results['levels']) {
                console.log(entry);
                console.log(results['elevations'][entry]);
                $("#elevations").innerHTML += "<li>" + entry + ": " + results['elevations'][entry] + "</li>";
            }
            for (entry in results['averages']) {
                console.log(entry);
                console.log(results['averages'][entry]);
                $("#averages").innerHTML += "<li>" + entry + ": " + results['averages'][entry] + "</li>";
            }
        }
    })
}