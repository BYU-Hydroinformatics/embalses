from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required()
def hist_levels_chart(request):
    """
    called when the reservoir stats page is opened to give data to the historical data chart
    """
    from model import operations, gethistoricaldata
    from app import Embalses as app

    name = app.currentpage
    info = operations()[name]

    responsedata = {}
    responsedata['y_min'] = 0
    responsedata['minlvl'] = info['minlvl'] - info['ymin']
    responsedata['maxlvl'] = info['maxlvl'] - info['ymin']

    hist_data = gethistoricaldata(name)
    for i in range(len(hist_data)):
        hist_data[i][1] -= info['ymin']         # change the values from elevations to depths
    responsedata['values'] = hist_data

    return JsonResponse(responsedata)