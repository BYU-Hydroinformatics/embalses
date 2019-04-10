# -*- coding: UTF-8 -*-

def operations():
    """
    A list of dams with all their relevant data
    """
    return {
        'Chacuey': {
            'comids': ['1396'],
            'minlvl': 47.00,
            'maxlvl': 54.63,
            'ymin': 30,
        },
        'Hatillo': {
            'comids': ['834', '813', '849', '857'],
            'minlvl': 70.00,
            'maxlvl': 86.50,
            'ymin': 55,
        },
        'Jiguey': {
            'comids': ['475', '496'],
            'minlvl': 500.00,
            'maxlvl': 541.50,
            'ymin': 450,
        },
        'Maguaca': {
            'comids': ['1399'],
            'minlvl': 46.70,
            'maxlvl': 57.00,
            'ymin': 30,
        },
        'Moncion': {
            'comids': ['1148', '1182'],
            'minlvl': 223.00,
            'maxlvl': 280.00,
            'ymin': 180,
        },
        'Rincon': {
            'comids': ['853', '922'],
            'minlvl': 108.50,
            'maxlvl': 122,
            'ymin': 95,
        },
        'Sabaneta': {
            'comids': ['863', '862'],
            'minlvl': 612,
            'maxlvl': 644,
            'ymin': 580,
        },
        'Sabana Yegua': {
            'comids': ['593', '600', '599'],
            'minlvl': 358,
            'maxlvl': 396.4,
            'ymin': 350,
            'custom_history_name': "S. Yegua"
        },
        'Tavera-Bao': {
            'comids': ['1024', '1140', '1142', '1153'],
            'minlvl': 300.00,
            'maxlvl': 327.50,
            'ymin': 270,
            'custom_history_name': "Tavera"
        },
        'Valdesia': {
            'comids': ['159'],
            'minlvl': 130.75,
            'maxlvl': 150.00,
            'ymin': 110,
        }
    }


def reservoirs():
    """
    A dictionary for relating the FULL name of a reservoir to the shortened name in urls/tables
    """
    names = {
        'Chacuey': 'chacuey',
        'Hatillo': 'hatillo',
        'Jiguey': 'jiguey',
        'Maguaca': 'maguaca',
        'Moncion': 'moncion',
        'Rincon': 'rincon',
        'Sabaneta': 'sabaneta',
        'Sabana Yegua': 'sabanayegua',
        'Tavera-Bao': 'taverabao',
        'Valdesia': 'valdesia',
    }
    return names


def get_historicaldata(reservoir_name):
    """
    You give it the name of a reservoir and it will read the excel sheet in the app workspace making a list of all the
    levels recorded so that you can plot them
    """
    from .app import Embalses as App
    import os, pandas, datetime, calendar

    # change the names for two reservoirs who are listed under different names in spreadsheets
    if reservoir_name == 'Sabana Yegua':
        reservoir_name = 'S. Yegua'
    elif reservoir_name == 'Tavera-Bao':
        reservoir_name = 'Tavera'

    # open the sheet with historical levels
    app_workspace = App.get_app_workspace()
    damsheet = os.path.join(app_workspace.path, 'elevations.xlsx')
    # read the sheet, get the water level info (nivel) corresponding to the correct reservoir name
    dfnan = pandas.read_excel(damsheet)
    df1 = dfnan[['Nivel', reservoir_name]]
    df = df1.dropna()       # drop null values from the series
    values = []

    # convert the date listed under nivel to a python usable form and make an entry with the date/value to the list
    for index, row in df.iterrows():
        time = row["Nivel"]
        time = datetime.datetime.strptime(str(time)[0:10], "%Y-%m-%d")
        timestep = calendar.timegm(time.utctimetuple()) * 1000
        values.append([timestep, row[reservoir_name]])

    # not sure why we do this, but it was left over from the old version of the app
    if reservoir_name == 'Bao':
        del values[0]
        del values[0]
    elif reservoir_name == 'Moncion':
        del values[0]

    histdata = {
        'values': values,
        'lastdate': time,
    }
    return histdata


def get_lastelevations():
    """
    Returns the most recently reported ELEVATION for each of the reservoirs as listed in the excel sheet
    """
    from .app import Embalses as App
    import os
    import pandas

    # open the sheet with historical levels
    app_workspace = App.get_app_workspace()
    damsheet = os.path.join(app_workspace.path, 'elevations.xlsx')
    df1 = pandas.read_excel(damsheet)
    elevations = {}

    for reservoir in reservoirs():
        if reservoir == 'Sabana Yegua':                 # change the names for two reservoirs who are
            reservoir = 'S. Yegua'                      # listed under different names in spreadsheets
        elif reservoir == 'Tavera-Bao':
            reservoir = 'Tavera'
        df = df1[['Nivel', reservoir]].dropna()       # load the right columns of data
        df = df.tail(1)
        for index, row in df.iterrows():
            elev = row[reservoir]

        if reservoir == 'S. Yegua':
            reservoir = 'Sabana Yegua'
        elif reservoir == 'Tavera':
            reservoir = 'Tavera-Bao'
        elevations[reservoir] = elev

    return elevations


def get_reservoirvolumes(reservoir_name):
    """
    You give it the name of a reservoir and it returns total volume and usable volume using the bathymetry data gained
    by reading the bathymetry spreadsheet
    """
    from .app import Embalses as App
    import os, pandas

    curr_elev = get_lastelevations()[reservoir_name]
    info = operations()[reservoir_name]
    volumes = {}

    if reservoir_name == 'Sabana Yegua':        # change the names for two reservoirs who are
        reservoir_name = 'Sabana_Yegua'         # listed under different names in spreadsheets
    if reservoir_name == 'Tavera-Bao':
        reservoir_name = 'Bao'
    app_workspace = App.get_app_workspace()
    bath = os.path.join(app_workspace.path, 'bathymetry.xlsx')
    df = pandas.read_excel(bath)[[reservoir_name + '_Elev', reservoir_name + '_Vol']]
    volumes['Actual'] = df.loc[df[reservoir_name + '_Elev'] == float(curr_elev)].values[0, 1]
    volumes['Min'] = df.loc[df[reservoir_name + '_Elev'] == info['minlvl']].values[0, 1]
    volumes['Max'] = df.loc[df[reservoir_name + '_Elev'] == info['maxlvl']].values[0, 1]
    volumes['Util'] = volumes['Actual'] - volumes['Min']
    del df
    for key in volumes:
        volumes[key] = round(volumes[key], 3)

    return volumes


def get_reservoirelevations(reservoir_name):
    """
    You give it the name of a reservoir and it gives you all the possible relevant elevations associated with it
    """
    elevations = {}
    elevations['Actual'] = get_lastelevations()[reservoir_name]
    elevations['Min'] = operations()[reservoir_name]['minlvl']
    elevations['Max'] = operations()[reservoir_name]['maxlvl']
    return elevations


def updatefromGoogleSheets():
    """
    The function that gets called when you want to update the elevations excel sheet from google
    """
    import os
    import pandas
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow

    # the spreadsheet info
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    sheetID = '1RxYxkP3mQvffaEIJQwp3K3QHPTCbvNXCvXLUnBcgUw4'
    sheetrange = 'elevaciones!A:O'
    excelpath = os.path.join(os.path.dirname(__file__), 'workspaces/app_workspace/elevations.xlsx')

    # api query info
    credentialspath = os.path.join(os.path.dirname(__file__), 'workspaces/app_workspace/sheetscredentials.json')
    credentials = InstalledAppFlow.from_client_secrets_file(credentialspath, scopes).run_local_server()
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    data = service.spreadsheets().values().get(spreadsheetId=sheetID, range=sheetrange).execute()
    array = data.get('values', []) if data.get('values')is not None else 0
    df = pandas.DataFrame(array, columns=array[0])
    df = df.drop(df.index[0])
    df.to_excel(excelpath)
    del df, array, data, service, credentials, credentialspath

    return


def get_elevationbyvolume(reservoir_name, newvolume):
    """
    part of the perform reservoir simulation calculation that will get the new elevation based on change in volume
    """
    from .app import Embalses as App
    import os
    import pandas

    if reservoir_name == 'Sabana Yegua':        # change the names for two reservoirs who are
        reservoir_name = 'Sabana_Yegua'         # listed under different names in spreadsheets
    if reservoir_name == 'Tavera-Bao':
        reservoir_name = 'Bao'
    app_workspace = App.get_app_workspace()
    bath = os.path.join(app_workspace.path, 'bathymetry.xlsx')
    df = pandas.read_excel(bath)[[reservoir_name + '_Elev', reservoir_name + '_Vol']].dropna()

    volume_index = 0
    newelevation = 0
    for row in df[reservoir_name + '_Vol']:
        if row > newvolume:
            newelevation = df.loc[df[reservoir_name + '_Vol'] == volume_index].values[0, 0]
            break
        else:
            volume_index = row
    return newelevation


def get_historicalaverages(reservoir_name):
    """
    Get the average elevation for the last 365 days and last 31 days
    """
    from .app import Embalses as App
    import os
    import pandas
    averages = {}

    # open the sheet with historical levels
    app_workspace = App.get_app_workspace()
    damsheet = os.path.join(app_workspace.path, 'elevations.xlsx')
    df = pandas.read_excel(damsheet)

    if reservoir_name == 'Sabana Yegua':    # change the names for two reservoirs who are
        reservoir_name = 'S. Yegua'         # listed under different names in spreadsheets
    elif reservoir_name == 'Tavera-Bao':
        reservoir_name = 'Tavera'

    df = df[['Nivel', reservoir_name]].dropna()  # load the right columns of data and drop the null values
    df = df.tail(365)
    averages['Elevacion, Ultimo Año'] = round(df[reservoir_name].mean(), 2)
    df = df.tail(31)
    averages['Elevacion, Ultimo Mes'] = round(df[reservoir_name].mean(), 2)

    return averages
