from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required()
def reservoir_pg_info(request):
    """
    Called when the reservoir stats page is opened to give data to the historical data chart
    """
    from .model import operations, gethistoricaldata
    from .app import Embalses as app
    import datetime

    name = app.currentpage
    info = operations()[name]
    responsedata = {}

    # GET THE DATA FOR THE CHART--------------------------------------------------------------------------
    historical = gethistoricaldata(name)
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
    from .model import make_overviewtable
    return JsonResponse(make_overviewtable())
