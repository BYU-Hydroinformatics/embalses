def forecastdata(comids, reservoir, outflow):

    outtime = 24.0

    from .app import Embalses as app
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

    return dataformatted
