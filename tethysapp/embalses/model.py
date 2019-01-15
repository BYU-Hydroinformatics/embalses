def operations():
    """
    A list of dams with all their relevant data
    """
    operations = {
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
    return operations

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


def gethistoricaldata(reservoir_name):
    """
    You give it the name of a reservoir and it will read the excel sheet in the app workspace making a list of all the
    levels recorded so that you can plot them
    """
    from .app import Embalses as app
    import os, pandas, datetime, calendar

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
    values = []

    # convert the date listed under nivel to a python usable form and make an entry with the date/value to the list
    for index, row in df.iterrows():
        time = row["Nivel"].to_pydatetime()
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


def getlastelevation():
    """
    Returns the most recently reported ELEVATION for each of the reservoirs as listed in the excel sheet
    """
    from .app import Embalses as app
    import os, pandas
    elevations = {}

    # open the sheet with historical levels
    app_workspace = app.get_app_workspace()
    damsheet = os.path.join(app_workspace.path, 'DamLevel_DR_BYU 2018.xlsx')
    dfnan = pandas.read_excel(damsheet)

    reservoirs = operations()
    for reservoir in reservoirs:
        # change the names for two reservoirs who are listed under different names in spreadsheets
        if reservoir == 'Sabana Yegua':
            reservoir = 'S. Yegua'
        elif reservoir == 'Tavera-Bao':
            reservoir = 'Tavera'

        df = dfnan[['Nivel', reservoir]].dropna()       # load the right columns of data and drop the null values
        df = df.tail(1)
        for index, row in df.iterrows():
            elev = row[reservoir]

        if reservoir == 'S. Yegua':
            reservoir = 'Sabana Yegua'
        elif reservoir == 'Tavera':
            reservoir = 'Tavera-Bao'
        elevations[reservoir] = elev

    return elevations


def getvolumefrombathymetry(reservoir_name):
    """
    You give it the name of a reservoir and it returns total volume and usable volume using the bathymetry data gained
    by reading the bathymetry spreadsheet
    """
    from .app import Embalses as app
    import os, pandas

    elevs = getlastelevation()
    info = operations()[reservoir_name]

    app_workspace = app.get_app_workspace()
    bath = os.path.join(app_workspace.path, 'BATIMETRIA PRESAS RD.xlsx')
    df = pandas.read_excel(bath)
    df1 = df[[reservoir_name + '_Elev', reservoir_name + '_Vol']]

    data = {}

    return data
