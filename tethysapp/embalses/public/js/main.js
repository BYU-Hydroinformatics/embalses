// Getting the csrf token
var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(document).ready(function() {
    // The code figures out which page you're on depending on the divs on the page and calls the right functions

    ///////////////////////////////////////////// HOME PAGE
    if ($('#map').length) {
        leaf_map();
        dataOverview();
    }

    ///////////////////////////////////////////// REPORTING PAGE
    if ($('#reporting_controls').length) {
        $('#synchronize').click(function() {
            updatesheet();
        })
    }

    ///////////////////////////////////////////// RESERVOIR SUMMARY PAGE
    if ($('#hist_data_chart').length) {
        tempHistoricalChart();
        tempStorageChart();
        getHistoricalChart();
        statisticalReport();
        getStorageCapacity();
    }

    ///////////////////////////////////////////// FUTURE SIMULATION PAGE
    if ($('#outflowTable').length) {
        $('#reservoir').change(function() {
            $("#outflowTable").html("<h1 style='text-align: center'>Carcicando tabla de datos...</h1>");
            $("#calculatebutton").html('');
            $("#numericalresults").html('');
            $("#warningresults").html('');
            $("#statisticalresults").html('');
            simulationTable();
        })
    }


});