# -*- coding: UTF-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required()
def reservoirpageplot(request):
    """
    Called when the reservoir stats page is opened, formats get_historicaldata for a highcharts plot
    """
    from .model import operations, get_historicaldata
    from .app import Embalses as App

    name = App.currentpage
    info = operations()[name]
    responsedata = {}

    # GET THE DATA FOR THE CHART--------------------------------------------------------------------------
    historical = get_historicaldata(name)['values']

    for i in range(len(historical)):
        historical[i][1] -= info['ymin']         # change the values from elevations to depths
    responsedata['values'] = historical

    min = info['minlvl'] - info['ymin']         # lines for the min/max levels
    max = info['maxlvl'] - info['ymin']
    firstday = historical[0][0]
    lastday = historical[len(historical)-1][0]
    responsedata['minimum'] = [[firstday, min], [lastday, min]]
    responsedata['maximum'] = [[firstday, max], [lastday, max]]

    return JsonResponse(responsedata)


@login_required()
def overviewpage(request):
    """
    called when the home page with the map is loaded. gets overview data about total volume, current levels, etc
    """
    from .tools import make_overviewtable
    return JsonResponse(make_overviewtable())


@login_required()
def simulationtable(request):
    """
    called when the simulation page starts to get used
    """
    from .tools import make_simulationtable
    from .model import reservoirs
    from .app import Embalses as App

    # convert to the right name syntax so you can get the COM ids from the database
    selected_reservoir = request.body.decode("utf-8")
    reservoirs = reservoirs()
    for reservoir in reservoirs:
        if reservoirs[reservoir] == selected_reservoir:
            selected_reservoir = reservoir
            break
    App.currentpage = selected_reservoir
    return JsonResponse(make_simulationtable(selected_reservoir))


@login_required()
def getsfptflows(request):
    """
    called when the simulation page starts to get used
    """
    from .model import reservoirs
    from .tools import get_sfptflows

    # convert to the right name syntax so you can get the COM ids from the database
    selected_reservoir = request.body.decode("utf-8")
    reservoirs = reservoirs()
    for reservoir in reservoirs:
        if reservoirs[reservoir] == selected_reservoir:
            selected_reservoir = reservoir
            break
    return JsonResponse(get_sfptflows(selected_reservoir))


@login_required()
def reservoirstatistics(request):
    """
    called when the simulation page starts to get used
    """
    from .model import get_reservoirvolumes, get_reservoirelevations, get_historicalaverages
    from .app import Embalses as App

    reservoir = App.currentpage
    data = {}
    data['volumes'] = get_reservoirvolumes(reservoir)
    data['elevations'] = get_reservoirelevations(reservoir)
    data['averages'] = get_historicalaverages(reservoir)

    return JsonResponse(data)


@login_required()
def updatesheet(request):
    """
    called when the simulation page starts to get used
    """
    from .model import updatefromGoogleSheets
    updatefromGoogleSheets()
    return JsonResponse({'update': True})


@login_required()
def performsimulation(request):
    """
    called when you press the button to perform the reservoir simulation
    Things this will return
    - the pre simulation volume, elevation
    - the post simulation volume, elevation
    - the total amount of volume difference
    - the meters of difference in elevation
    - how many days you can use water at this average rate before running out
    - the total amount of consumption
    - the total amount of inflow
    """
    from .model import get_elevationbyvolume, get_lastelevations, get_reservoirvolumes, get_reservoirelevations
    from .app import Embalses as App
    import ast

    warnings = {
        'maxlevel': [],             # a list of the days when the reservoir will be above max capacity
        'minlevel': [],             # a list of the days when the reservoir will be below min capacity
        'estimatedloss': '',        # how much will be lost when the reservoir goes over capacity if spillway used
    }
    total_inflow = 0
    total_outflow = 0

    tabledata = ast.literal_eval(request.body.decode('UTF-8'))  # data is a list of dictionaries for each row
    for i in range(len(tabledata)):
        # calculate the sum of the inflows and outflows
        total_inflow += tabledata[i]['inflow']
        total_outflow += (float(tabledata[i]['release']) * float(tabledata[i]['time']))
    # adjust for time conversions from cubic meters per second to cubic meters
    total_inflow = total_inflow * 3600 * 24
    total_outflow = total_outflow * 3600

    # calculate the total difference
    volume_change = round(total_inflow - total_outflow, 2)
    # warnings.append(whichever error you got)

    alllastvolumes = get_reservoirvolumes(App.currentpage)
    lastelevation = get_lastelevations()[App.currentpage]
    newvolume = alllastvolumes['Actual'] + volume_change / 1000000
    newelevation = get_elevationbyvolume(App.currentpage, newvolume)
    elevationchange = newelevation - lastelevation

    response = {
        'numericalresults': {
            'Volumen Actual (MMC)': alllastvolumes['Actual'],
            'Volumen Entrada (M^3)': round(total_inflow, 2),
            'Volumen Salida (M^3)': round(total_outflow, 2),
            'Volumen Nuevo (Simulado MMC)': newvolume,
            'Cambio de Volumen (M^3)': volume_change,
            'Elevacion Actual (M)': lastelevation,
            'Elevacion Nueva (Simulada M)': newelevation,
            'Cambio de Elevacion (M)': round(elevationchange, 2),
        },
        'warningresults': {
            'Elevaciones': {
                'Supera Nivel Máximo': 'No hay problema'
            },
            'Volumenes': {
                'Not enough water': 'No hay problem'
            },
        },
        'statisticalresults': {
            'Volumenes': alllastvolumes,
            'Elevaciones': get_reservoirelevations(App.currentpage)
        }
    }

    return JsonResponse(response)
