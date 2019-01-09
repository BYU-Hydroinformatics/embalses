from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.permissions import has_permission

from tools import generate_app_urls, check_portal_analytics
from model import reservoirs

from tethys_sdk.gizmos import TableView

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
def instructions(request):
    """
    controller for the instructions page
    """

    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs)
    }

    return render(request, 'embalses/instructions.html', context)


@login_required()
def reservoirviewer(request, name):
    """
    controller for the reservoir specific page template. The code does 2 functions in this order:
    - This calls the gethistoricaldata method which takes a long time to read 35 years of daily data
    - Calls getdates to populate the next available forecast dates in the simulation tables
    todo: When the button is pressed to calculate future levels, do the math to figure out the water levels
    todo: how much water is left? current - min height, read from bathimetry table
    """
    import datetime
    from app import Embalses as App

    for reservoir in reservoirs:
        if reservoirs[reservoir] == name:
            name = reservoir
            App.currentpage = name

    # generate a table for simulating changes in reservoir levels
    dates = []
    for i in range(0, 7):
        timedelta = datetime.timedelta(i)
        dates.append((datetime.datetime.today() + timedelta).strftime('%B %d %Y'))
    outflows_tbl = TableView(column_names=('Dia', 'Caudal de Salida (cms)', 'Tiempo de salida (horas)'),
                             rows=[(dates[0], '0', '0'),
                                   (dates[1], '0', '0'),
                                   (dates[2], '0', '0'),
                                   (dates[3], '0', '0'),
                                   (dates[4], '0', '0'),
                                   (dates[5], '0', '0'),
                                   (dates[6], '0', '0'),
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
        'table_view': outflows_tbl,
    }

    return render(request, 'embalses/reservoir.html', context)
