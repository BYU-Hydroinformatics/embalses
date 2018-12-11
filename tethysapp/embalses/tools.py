def check_portal_analytics():
    """
    This is the code that checks to see if django analytics is installed. If it is it adds the tags to implement it
    """
    import os
    from django.core.management import settings

    print('PORTAL ANALYTICS: Getting portal analytical configuration status.')
    my_directory = os.path.dirname(__file__)
    with open(os.path.join(my_directory, 'templates/embalses/embalses.html'), 'w') as file:
        if 'analytical' in settings.INSTALLED_APPS:
            print('PORTAL ANALYTICS: Analytics is enabled for this Portal. Enabling tracking.')
            file.write("{% load google_analytics_js %}{% google_analytics_js %}")
        else:
            print('PORTAL ANALYTICS: Analytics has not been configured for this portal. Disabling tracking.')
    return


def generate_app_urls(request, res_dict):
    """
    This fucntion creates urls for every app installed on the portal this app is on.

    Use this app in the controller for every navigable page so that the list of app links is visible in the navigation
    pane of that page. In base.html, there is a conditional set of django tags that will load the links if you give it
    this list of links and otherwise not.

    :param request: You need to give it the request passed to the controller of the page you're on (in the controller)
            so that that it knows what the base of the urls is supposed to be. then it manually adds urls using the
            lamda function. the x for the lambda function is the app dictionary parameter
    :param res_dict: the dictionary containing the names and slimmed names of each reservoir in reservoirs() in tools.py
    :return: site_urls which is a list of dictionaries. Each dictionary contains the name, url, and active (a boolean
            check whether or not the current url is the url generated). active needs to be this verbose otherwise the
            analytics app link will be highlighted all the time.
    """

    from django.contrib.sites.shortcuts import get_current_site
    from django.conf import settings

    current_site = get_current_site(request)

    if (settings.FORCE_SCRIPT_NAME):
        base = settings.FORCE_SCRIPT_NAME
    else:
        base = str(current_site);
    site_urls = list(map((lambda x: {
        'name': x,
        'url': request.build_absolute_uri(
            '//' + base + '/apps/embalses/' + res_dict[x].replace(" ", "_") + '/'),
        'active': request.path.endswith('embalses/' + res_dict[x] + '/')
    }), res_dict))

    return site_urls


def gettabledates(comid):
    """
    You give it the comid you want flows for
    :param comid:
    :return:
    """
    import requests

    comid = comid[0]
    request_params = dict(watershed_name='Dominican Republic', subbasin_name='National', reach_id=comid,
                          forecast_folder='most_recent', stat_type='mean', return_format='csv')
    request_headers = dict(Authorization='Token fa7fa9f7d35eddb64011913ef8a27129c9740f3c')
    res = requests.get('https://tethys-staging.byu.edu/apps/streamflow-prediction-tool/api/GetForecast/',
                       params=request_params, headers=request_headers)

    timeseries = []
    dates = []

    content = res.content.splitlines()
    for i in content:
        timeseries.append(i.split(','))
    timeseries.pop(0)

    for i in range(len(timeseries)):
        if '12:00:00' in timeseries[i][0]:
            dates.append(str(timeseries[i][0])[5:-9])

    return(dates)


def forecastdata(comids, reservoir, outflow):

    outtime = 24.0

    from app import Embalses as app
    import os, pandas, requests
    import datetime as datetime

    # Open the sheets with the bathimetry data and historical level
    app_workspace = app.get_app_workspace()
    damsheet = os.path.join(app_workspace.path, 'DamLevel_DR_BYU 2018.xlsx')
    bathimetry = os.path.join(app_workspace.path, 'BATIMETRIA PRESAS RD.xlsx')

    # Read the historical data sheet and get the last entry date, last level, last observed date
    if reservoir == 'Sabana_Yegua':
        reservoir = 'S. Yegua'
    dfnan = pandas.read_excel(damsheet)
    df1 = dfnan[['Nivel', reservoir]]
    df = df1.dropna()[::-1]
    reslevel = df[:1]
    lastdate = reslevel['Nivel']
    lastlevel = reslevel[reservoir]

    lastobsdate = str(lastdate.iloc[0])[:10]
    elevval = lastlevel.iloc[0]

    outvol = outflow * outtime * 3600.0

    totalflow = []
    tsvol = []
    tselev = []
    data = {}
    dataformatted = {}

    if reservoir == 'S. Yegua':
        reservoir = 'Sabana_Yegua'

    elev = reservoir + '_Elev'
    vol = reservoir + '_Vol'



    df = pandas.read_excel(bathimetry)
    volres = df.loc[df[elev] == elevval, vol].iloc[0]
    volin = volres * 1000000

    for comid in comids:
        request_params = dict(watershed_name='Dominican Republic', subbasin_name='National', reach_id=comid,
                              forecast_folder='most_recent', stat_type='mean', return_format='csv')
        request_headers = dict(Authorization='Token fa7fa9f7d35eddb64011913ef8a27129c9740f3c')
        reservoir = requests.get('https://tethys-staging.byu.edu/apps/streamflow-prediction-tool/api/GetForecast/',
                                 params=request_params, headers=request_headers)

        content = reservoir.content.splitlines()

        ts = []
        comidflows = []
        allcomidflows = []

        for i in content:
            ts.append(i.split(','))

        ts.pop(0)

        for r in ts:
            allcomidflows.append(float(r[1]))
            if r[0].endswith('12:00:00'):
                comidflows.append(float(r[1]))

        totalflow.append(allcomidflows)
        data[comid] = comidflows

    newseries = []
    for x in data:
        newseries.append(data[x])

    total = [sum(x) for x in zip(*newseries)]
    alltotal = [sum(x) for x in zip(*totalflow)]
    data['total'] = total

    for x in data:
        formattedtotal = ["%.2f" % elem for elem in data[x]]
        dataformatted[x] = formattedtotal

    dates = []

    for x in range(len(ts)):
        if x == 0:
            inflow1 = float(alltotal[x])
            time1 = datetime.datetime.strptime(ts[x][0], "%Y-%m-%d %H:%M:%S")
        else:
            inflow2 = float(alltotal[x])
            time2 = datetime.datetime.strptime(ts[x][0], "%Y-%m-%d %H:%M:%S")
            timedif = (time2 - time1).total_seconds()
            vol2 = (inflow2 + inflow1) / 2 * timedif
            volin = volin + vol2
            inflow1 = inflow2
            time1 = time2
            if ts[x][0].endswith('12:00:00'):
                if not tsvol:
                    tsvol.append([str(ts[x][0])[:10], volin - (outvol / 2.0)])
                    dates.append(str(ts[x][0])[5:-9])
                    volin = volin - (outvol / 2.0)
                else:
                    tsvol.append([str(ts[x][0])[:10], volin - outvol])
                    dates.append(str(ts[x][0])[5:-9])
                    volin = volin - (outvol)

    for q in tsvol:
        volval = q[1]
        volval = volval / 1000000.0
        evolval = (df.loc[df[vol] > volval, elev].iloc[0])
        tselev.append(evolval)

    dataformatted['levels'] = tselev
    dataformatted['dates'] = dates

    return(dataformatted)


def gethistoricaldata(reservoir_name):

    from app import Embalses as app
    import os, pandas

    # change the names for two reservoirs who are listed under different names in spreadsheets
    if reservoir_name == 'Sabana Yegua':
        reservoir_name = 'S. Yegua'
    elif reservoir_name == 'Tavera-Bao':
        reservoir_name = 'Tavera'

    app_workspace = app.get_app_workspace()
    damsheet = os.path.join(app_workspace.path, 'DamLevel_DR_BYU 2018.xlsx')

    dfnan = pandas.read_excel(damsheet)
    df1 = dfnan[['Nivel', reservoir_name]]
    df = df1.dropna()

    data = []

    for index, row in df.iterrows():
        timestep = row["Nivel"].to_pydatetime()
        value = row[reservoir_name]
        data.append([timestep, value])

    if reservoir_name == 'Bao':
        del data[0]
        del data[0]
    elif reservoir_name == 'Moncion':
        del data[0]

    return data