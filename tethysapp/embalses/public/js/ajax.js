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
        data: 'feed me ur info',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(results) {
            console.log(results);
            tabulatorOutflows(results['result']);
            }
        })
}
