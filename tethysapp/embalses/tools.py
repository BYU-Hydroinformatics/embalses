def check_portal_analytics():
    """
    This is the code that checks to see if django analytics is installed. If it is, it adds the tags to implement it
    """
    import os
    from django.core.management import settings

    print('ADMINSTRACION DE LOS EMBALSES: Getting portal analytical configuration status.')
    my_directory = os.path.dirname(__file__)
    with open(os.path.join(my_directory, 'templates/embalses/embalses.html'), 'w') as file:
        if 'analytical' in settings.INSTALLED_APPS:
            print('ADMINSTRACION DE LOS EMBALSES: Analytics is enabled for this Portal. Enabling tracking.')
            file.write("{% load google_analytics_js %}{% google_analytics_js %}")
        else:
            print('ADMINSTRACION DE LOS EMBALSES: Analytics has not been configured for this portal. Disabling tracking.')
    return


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

    if (settings.FORCE_SCRIPT_NAME):
        base = settings.FORCE_SCRIPT_NAME
    else:
        base = str(current_site)
    site_urls = list(map((lambda x: {
        'name': x,
        'url': request.build_absolute_uri(
            '//' + base + '/apps/embalses/' + res_dict[x].replace(" ", "_") + '/'),
        'active': request.path.endswith('embalses/' + res_dict[x] + '/')
    }), res_dict))

    return site_urls


def gethistoricaldata(reservoir_name):

    from app import Embalses as app
    import os, pandas

    # change the names for two reservoirs who are listed under different names in spreadsheets
    if reservoir_name == 'Sabana Yegua':
        reservoir_name = 'S. Yegua'
    elif reservoir_name == 'Tavera-Bao':
        reservoir_name = 'Tavera'

    # open the sheet with historical levels
    app_workspace = app.get_app_workspace()
    damsheet = os.path.join(app_workspace.path, 'DamLevel_DR_BYU 2018.xlsx')
    # read the sheet, get the water level info (nivel) corresponding to the correct reservoir name
    dfnan = pandas.read_excel(damsheet)
    df1 = dfnan[['Nivel', reservoir_name]]
    df = df1.dropna()       # drop null values from the series
    data = []

    # convert the date listed under nivel to a python usable form and make an entry with the date/value to the list
    for index, row in df.iterrows():
        timestep = row["Nivel"].to_pydatetime()
        data.append([timestep, row[reservoir_name]])

    if reservoir_name == 'Bao':
        del data[0]
        del data[0]
    elif reservoir_name == 'Moncion':
        del data[0]

    return data