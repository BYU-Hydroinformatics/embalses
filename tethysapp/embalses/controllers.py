from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.permissions import has_permission

from tools import generate_app_urls, check_portal_analytics, gethistoricaldata
from forecasts import gettabledates, forecastdata
from model import operations, reservoirs

from tethys_sdk.gizmos import TimeSeries, TableView

check_portal_analytics()
reservoirs = reservoirs()

@login_required()
def home(request):
    """
    controller for the home page
    """
    # The map on this page is handled entirely using leaflet and javascript
    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs)
    }

    return render(request, 'embalses/home.html', context)


@login_required()
def reportar(request):
    """
    controller for the reporting page
    """

    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs)
    }

    return render(request, 'embalses/reportar.html', context)


@login_required()
def reservoirviewer(request, name):
    """
    controller for the reservoir specific page template. The code does 2 functions in this order:
    - This calls the gethistoricaldata method which takes a long time to read 35 years of daily data
    - Calls gettabledates to populate the next available forecast dates in the simulation tables
    todo: When the button is pressed to calculate future levels, do the math to figure out the water levels
    todo: how much water is left? current - min height, read from bathimetry table
    """
    for reservoir in reservoirs:
        if reservoirs[reservoir] == name:
            name = reservoir

    # Show the historical times series plot
    # Get the historical data and 2 coordinate pairs for lines of min/max water levels
    info = operations()[name]
    hist_data = gethistoricaldata(name)
    for i in range(len(hist_data)):
        hist_data[i][1] -= info['ymin']         # change the values from elevations to depths
    minlvl = [ [hist_data[0][0], info['minlvl'] - info['ymin']], [hist_data[-1][0], info['minlvl'] - info['ymin']] ]
    maxlvl = [ [hist_data[0][0], info['maxlvl'] - info['ymin']], [hist_data[-1][0], info['maxlvl'] - info['ymin']] ]
    timeseries = TimeSeries(
        height='500px',
        width='500px',
        engine='highcharts',
        title=name,
        y_axis_title='Niveles de agua',
        y_axis_units='Metros',
        series=[
            {'name': 'Nivel Historico', 'data': hist_data},
            {'name': 'Nivel Minimo de Operacion', 'data': minlvl, 'type': 'line', 'color': '#660066'},
            {'name': 'Nivel Maximo de Operacion', 'data': maxlvl, 'type': 'line', 'color': '#FF0000'}
        ],
        y_min=0
    )

    # based on the comids in the list, generate a table for simulating changes in reservoir levels
    # uses the gettabledates method to get the dates of the next available forecast days
    comid = info['comids']
    tabledates = gettabledates(comid)
    outflows_tbl = TableView(column_names=('Dia', 'Caudal de Salida (cms)', 'Tiempo de salida (horas)'),
                             rows=[(tabledates[0], '0', '0'),
                                   (tabledates[1], '0', '0'),
                                   (tabledates[2], '0', '0'),
                                   (tabledates[3], '0', '0'),
                                   (tabledates[4], '0', '0'),
                                   (tabledates[5], '0', '0'),
                                   (tabledates[6], '0', '0'),
                                   ],
                             hover=True,
                             striped=True,
                             bordered=True,
                             condensed=True,
                             editable_columns=(False, 'Outflow', 'Time'),
                             row_ids=['day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7'],
                             classes="outflowtable"
                             )

    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs),
        'name': name,
        'timeseries_plot': timeseries,
        'table_view': outflows_tbl,
    }

    return render(request, 'embalses/reservoir.html', context)
