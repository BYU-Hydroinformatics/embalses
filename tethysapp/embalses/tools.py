
def generate_app_urls(request, res_dict):
    """
    This function creates urls for every app installed on the portal this app is on.

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

    MOUNT_PATH = os.environ.get('TETHYS_MOUNT_PATH') or '/'
    MOUNT_PATH = os.path.join(MOUNT_PATH, '')

    site_urls = list(map((lambda x: {
        'name': x,
        'url': MOUNT_PATH + 'apps/embalses/' + res_dict[x].replace(" ", "_") + '/',
        'active': request.path.endswith('embalses/' + res_dict[x] + '/')
    }), res_dict))

    return site_urls


def get_sfptflows(reservoir_name):
    """
    Queries the SFPT API for the rivers going into the reservoir specified for the next 7 days. Returns a dictionary of
    the dates of the flows and their magnitudes.
    """

    from .model import operations
    from .app import Embalses as App
    import requests
    import datetime
    import codecs

    flows = {}
    info = operations()

    api_url = 'http://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetForecast/'
    api_token = {'Authorization': 'Token 054ba636689eb081fd9ba75401fc77544a0496e3'}
    parameters = {
        'watershed_name': 'Dominican Republic',
        'subbasin_name': 'National',
        'forecast_folder': 'most_recent',
        'stat_type': 'mean'
    }

    for comid in info[reservoir_name]['comids']:
        parameters['reach_id'] = comid
        content = requests.get(api_url, params=parameters, headers=api_token).content       # returns a bytes object
        content = codecs.decode(content)                                                    # decode into a string
        data = content.split('dateTimeUTC="')      # split the xml into a list of strings that start with dateTimeUTC="
        data.pop(0)                                # get rid of the first string, everything before the first date

        values = []
        timestep = []
        for e in data:
            # split the strings into substrings with the metadata
            parser = e.split('"  methodCode="1"  sourceCode="1"  qualityControlLevelCode="1" >')
            # keep the first part that has the date
            dateraw = parser[0]
            # make it a datetime object
            dates = datetime.datetime.strptime(dateraw, "%Y-%m-%dT%H:%M:%S")
            if str(dates).endswith("00:00:00"):
                value = float(parser[1].split('<')[0])
                values.append(value)
                timestep.append(str(dates)[5:-9])
        # save a dictionary entry in the form {'comid': [list of flows on each day]}
        flows[comid] = values

    total = [0 for i in range(7)]
    for comid in flows:
        for i in range(7):
            total[i] += flows[comid][i]
    flows['total'] = total

    # set the current page to the reservoir you're requesting information for so ajax.performsimulation knows
    App.currentpage = reservoir_name

    return flows


def make_simulationtable(reservoir):
    """
    A function that gets called when the simulations page is opened that creates the list of entries for the table
    """
    import datetime

    # variables declaration
    tabledata = {}          # the response dictionary
    entries = []            # tabulator expects a list with one dictionary per row
    flows = get_sfptflows(reservoir)

    # For each day in the next 7 days
    for i in range(7):
        # set the date we're working on
        date = (datetime.datetime.today() + datetime.timedelta(i)).strftime('%m-%d-%Y')
        new_entry = {
            'date': date,
            'inflow': round(flows['total'][i], 2),
            'release': 0,
            'units': 'mcs',
            'time': 0,
        }
        entries.append(new_entry)

    tabledata['result'] = entries
    del new_entry, entries

    return tabledata


def make_overviewtable():
    """
    A function that creates the data needed for the overview table on the app home page.
    The format for that data is a list of dictionaries
    """
    from .model import operations, get_lastelevations, get_reservoirvolumes
    # variables declaration
    tabledata = {}              # the response dictionary
    entries = []                # tabulator expects a list with one dictionary per row
    res_ops = operations()
    lastelevation = get_lastelevations()

    for reservoir in res_ops:
        # append the max, min, current (actual in spanish), and available (util) elevations and volume
        volumes = get_reservoirvolumes(reservoir)
        new_entry = {
            'name': reservoir,
            'maxlvl': res_ops[reservoir]['maxlvl'],
            'actlvl': lastelevation[reservoir],
            'minlvl': res_ops[reservoir]['minlvl'],
            'maxvol': volumes['Max'],
            'actvol': volumes['Actual'],
            'minvol': volumes['Min'],
            'utilvol': volumes['Util'],
        }
        entries.append(new_entry)

    del lastelevation

    tabledata['result'] = entries

    return tabledata
