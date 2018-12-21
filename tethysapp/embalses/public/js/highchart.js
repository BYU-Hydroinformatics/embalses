// Global Highcharts options
Highcharts.setOptions({
    lang: {
        downloadCSV: "Download CSV",
        downloadJPEG: "Download JPEG image",
        downloadPDF: "Download PDF document",
        downloadPNG: "Download PNG image",
        downloadSVG: "Download SVG vector image",
        downloadXLS: "Download XLS",
        loading: "Cargando Datos",
        noData: "Cargando Datos"
    },
});

function placeholderchart() {
    // Place holder chart
    chart = Highcharts.chart('hist_data_chart', {
        title: {
            align: "center",
            text: "Datos Historicos",
        },
        xAxis: {
            type: 'datetime',
            title: {text: "Tiempo"},
        },
        yAxis: {
            title: {text: 'Niveles de agua (metros)'}
        },
        series: [{
            data: [],
        }],
        chart: {
            animation: true,
            zoomType: 'x',
            borderColor: '#000000',
            borderWidth: 2,
            type: 'area',
        },
        noData: {
            style: {
                fontWeight: 'bold',
                fontSize: '15px',
                color: '#303030'
            }
        },
    });
}

function newHighchart(data) {
    chart = Highcharts.chart('hist_data_chart', {
        title: {
            align: "center",
            text: 'Datos Historicos',
        },
        xAxis: {
            type: 'datetime',
            title: {text: "Tiempo"},
        },
        yAxis: {
            title: {text: 'Niveles de agua (metros)'},
            min: 0,
        },
        series: [{
            data: data['values'],
            type: "area",
            name: 'Niveles',
            tooltip: {
                xDateFormat: '%Y-%m-%d',
            },
        }],
        chart: {
            animation: true,
            zoomType: 'x',
            borderColor: '#000000',
            borderWidth: 2,
            type: 'area',

        },

    });
}

function getChart() {
    $.ajax({
        url:'/apps/embalses/ajax/chartdata/',
        data: 'please make me a chart',
        dataType: 'json',
        contentType: "application/json",
        method: 'POST',
        success: function(result) {
            newHighchart(result);
            },
        });
}