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
    from .model import get_reservoirvolumes, get_reservoirelevations
    from .app import Embalses as app

    reservoir = app.currentpage
    data = {}
    data['volumes'] = get_reservoirvolumes(reservoir)
    data['elevations'] = get_reservoirelevations(reservoir)
    data['averages'] = {
        'monthly': 0,
        'lastyr': 0,
    }

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
    from .model import get_elevationbyvolume, get_lastelevations, get_reservoirvolumes
    from .app import Embalses as App
    import ast

    tabledata = ast.literal_eval(request.body.decode('UTF-8'))  # data is a list of dictionaries for each row
    print(type(tabledata))
    print(tabledata)

    warnings = {
        'maxlevel': [],             # a list of the days when the reservoir will be above max capacity
        'minlevel': [],             # a list of the days when the reservoir will be below min capacity
        'estimatedloss': '',        # how much will be lost when the reservoir goes over capacity if spillway used
    }
    total_inflow = 0
    total_outflow = 0
    for i in range(len(tabledata)):
        # calculate the inflow/day and total
        total_inflow += tabledata[i]['inflow']
        # calculate the outflow/day and total
        total_outflow += tabledata[i]['release'] * tabledata[i]['time'] * 3600
        # check to see if you cross the max/min value each day

    # calculate the total difference
    volume_change = total_inflow - total_outflow
    print(volume_change)
    # warnings.append(whichever error you got)

    response = {
        'totalin': total_inflow,
        'totalout': total_outflow,
        'volchange': volume_change,
        'lastelevation': get_lastelevations()[App.currentpage],
        'lastvolume': get_reservoirvolumes(App.currentpage),
        'newelevation': get_elevationbyvolume(),
        'newvolume': 'number calculated in steps above',
        'elevchange': '',

        'dailyinflows': '',
        'dailyoutflows': '',
        'dailytotals': '',
        'daysremaining': '',

        'warnings': warnings,
    }
    print(response)
    return JsonResponse(response)