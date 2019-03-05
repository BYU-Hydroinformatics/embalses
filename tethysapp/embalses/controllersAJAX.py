from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required()
def reservoir_pg_info(request):
    """
    Called when the reservoir stats page is opened to give data to the historical data chart
    """
    from .model import operations, get_historicaldata
    from .app import Embalses as app
    import datetime

    name = app.currentpage
    info = operations()[name]
    responsedata = {}

    # GET THE DATA FOR THE CHART--------------------------------------------------------------------------
    historical = get_historicaldata(name)
    hist_data = historical['values']
    for i in range(len(hist_data)):
        hist_data[i][1] -= info['ymin']         # change the values from elevations to depths
    responsedata['values'] = hist_data

    min = info['minlvl'] - info['ymin']         # lines for the min/max levels
    max = info['maxlvl'] - info['ymin']
    firstday = hist_data[0][0]
    lastday = hist_data[len(hist_data)-1][0]
    responsedata['minimum'] = [[firstday, min], [lastday, min]]
    responsedata['maximum'] = [[firstday, max], [lastday, max]]

    # GET DATA FOR THE STATS SECTION BELOW THE CHART------------------------------------------------------
    responsedata['minlvl'] = "Nivel MINIMO: " + str(min) + " metros"
    responsedata['maxlvl'] = "Nivel MAXIMO: " + str(max) + " metros"
    responsedata['currentlvl'] = "Nivel actual: " + str(hist_data[len(hist_data) - 1][1]) + " metros"

    lastdate = datetime.datetime.strftime(historical['lastdate'], "%d %B %Y")
    responsedata['lastreport'] = "Fecha de la ultima entrada: " + lastdate

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
    return JsonResponse(make_simulationtable())


@login_required()
def getsfptflows(request):
    """
    called when the simulation page starts to get used
    """
    from .model import reservoirs
    from .tools import get_sfpt_flows

    # convert to the right name syntax so you can get the COM ids from the database
    selected_reservoir = request.body.decode("utf-8")
    reservoirs = reservoirs()
    for reservoir in reservoirs:
        if reservoirs[reservoir] == selected_reservoir:
            selected_reservoir = reservoir
            break
    return JsonResponse(get_sfpt_flows(selected_reservoir))


@login_required()
def reservoirstatistics(request):
    """
    called when the simulation page starts to get used
    """
    from .model import operations, get_reservoirvolumes, get_lastelevations
    from .app import Embalses as app

    reservoir = app.currentpage
    info = operations()
    data = {}
    data['volumes'] = get_reservoirvolumes(reservoir)
    data['elevations'] = {
        'min': info[reservoir]['minlvl'],
        'max': info[reservoir]['maxlvl'],
        'current': get_lastelevations()[reservoir],
    }
    data['averages'] = {
        'monthly': 0,
        'lastyr': 0,
    }

    return JsonResponse(data)
