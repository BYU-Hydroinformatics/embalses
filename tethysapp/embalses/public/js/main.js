// Getting the csrf token
let csrftoken = Cookies.get('csrftoken');
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
    if ($('#map').length) {
        leaf_map();
//        dataOverview();
    }
    if ($('#hist_data_chart').length) {
        placeholderchart();
        getChart();
    }



});