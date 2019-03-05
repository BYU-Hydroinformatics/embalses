function getChart() {
    $.ajax({
        url:'/apps/embalses/ajax/respageinfo/',
        data: 'please make me a chart',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(result) {
            newHighchart(result);
//            $("#minlvl").text(result['minlvl']);
//            $("#maxlvl").text(result['maxlvl']);
//            $("#currentlvl").text(result['currentlvl']);
//            $("#lastreport").text(result['lastreport']);
//            $("#capacity").text)result['capacity'];
//            $("#wateravailable").text)result['wateravailable'];
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
            $("#volumes").innerHTML += results['volumes'];
            $("#levels").innerHTML += results['levels'];
            $("#averages").innerHTML += results['averages'];
            }
        })
}