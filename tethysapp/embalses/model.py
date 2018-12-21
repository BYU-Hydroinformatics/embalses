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
    from app import Embalses as app
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
    data = []

    # convert the date listed under nivel to a python usable form and make an entry with the date/value to the list
    timestep = 0
    for index, row in df.iterrows():
        # timestep = row["Nivel"].to_pydatetime()

        # timestep = datetime.datetime.strptime(row['Nivel'], "%Y-%m-%d")
        # timestep = calendar.timegm(timestep.utctimetuple()) * 1000

        # timestep = row['Nivel'].utctimetuple()
        # print(timestep)

        timestep += 1

        data.append([timestep, row[reservoir_name]])

    if reservoir_name == 'Bao':
        del data[0]
        del data[0]
    elif reservoir_name == 'Moncion':
        del data[0]

    return data