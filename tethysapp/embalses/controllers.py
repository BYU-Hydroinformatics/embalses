from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.permissions import has_permission

from tools import generate_app_urls, check_portal_analytics
from tools import gethistoricaldata, gettabledates, forecastdata
from model import operations, reservoirs

from tethys_sdk.gizmos import TimeSeries, TableView

check_portal_analytics()
reservoirs = reservoirs()

@login_required()
def home(request):
    """
    controller for the home page
    """

    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs)
    }

    return render(request, 'embalses/home.html', context)


@login_required()
def reportar(request):
    """
    controller for the reporting page
    """

    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs)
    }

    return render(request, 'embalses/reportar.html', context)


@login_required()
def reservoirviewer(request, name):
    """
    controller for the reservoir specific page template
    """
    for reservoir in reservoirs:
        if reservoirs[reservoir] == name:
            name = reservoir

    # Show the historical times series plot
    # Get the historical data and 2 coordinate pairs for lines of min/max water levels
    info = operations()[name]
    hist_data = gethistoricaldata(name)
    minlvl = [ [hist_data[0][0], info['minlvl']], [hist_data[-1][0], info['minlvl']] ]
    maxlvl = [ [hist_data[0][0], info['maxlvl']], [hist_data[-1][0], info['maxlvl']] ]
    timeseries = TimeSeries(
        height='500px',
        width='500px',
        engine='highcharts',
        title=name,
        y_axis_title='Niveles de agua',
        y_axis_units='Metros',
        series=[
            {'name': 'Nivel Historico', 'data': hist_data},
            {'name': 'Nivel Minimo de Operacion', 'data': minlvl, 'type': 'line', 'color': '#660066'},
            {'name': 'Nivel Maximo de Operacion', 'data': maxlvl, 'type': 'line', 'color': '#FF0000'}
        ],
        y_min=info['ymin']
    )

    #
    comid = info['comids']
    tabledates = gettabledates(comid)
    outflows_tbl = TableView(column_names=('Dia', 'Caudal de Salida (cms)', 'Tiempo de salida (horas)'),
                             rows=[(tabledates[0], '0', '0'),
                                   (tabledates[1], '0', '0'),
                                   (tabledates[2], '0', '0'),
                                   (tabledates[3], '0', '0'),
                                   (tabledates[4], '0', '0'),
                                   (tabledates[5], '0', '0'),
                                   (tabledates[6], '0', '0'),
                                   ],
                             hover=True,
                             striped=True,
                             bordered=True,
                             condensed=True,
                             editable_columns=(False, 'Outflow', 'Time'),
                             row_ids=['day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7'],
                             classes="outflowtable"
                             )

    # calculate = Button(display_text='Calcular Niveles del Embalse',
    #                    name='calculate',
    #                    style='',
    #                    icon='',
    #                    href='',
    #                    submit=False,
    #                    disabled=False,
    #                    attributes={"onclick": "calculatelevels()"},
    #                    classes='calcbut'
    #                    )
    #
    # outflow_button = Button(display_text='Ingresar caudales de salida',
    #                         name='dimensions',
    #                         style='',
    #                         icon='',
    #                         href='',
    #                         submit=False,
    #                         disabled=False,
    #                         attributes={"onclick": "outflowmodal()"},
    #                         classes='outflow_button'
    #                         )

    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs),
        'name': name,
        'timeseries_plot': timeseries,
        'table_view': outflows_tbl,
        # 'calculate': calculate,
        # 'outflow_button': outflow_button,
    }

    return render(request, 'embalses/reservoir.html', context)


'''
def site_handler(request, site_name):
    """
    Main controller for the dams page.
    """
    gen_urls(request)
    site_name = site_name.replace('_', " ")

    # Get config
    site_config = config(site_name);
    comids = site_config['comids'];
    forecasteddata = gettabledates(comids)

    historyname = site_name
    if (site_config['custom_history_name']):
        historyname = site_config['custom_history_name'];

    data = gethistoricaldata(historyname)

    min_level = [[data[0][0], site_config['min_level']], [data[-1][0], site_config['min_level']]]
    max_level = [[data[0][0], site_config['max_level']], [data[-1][0], site_config['max_level']]]

    timeseries_plot = TimeSeries(
        height='500px',
        width='500px',
        engine='highcharts',
        title=site_name,
        y_axis_title='Niveles de agua',
        y_axis_units='m',
        series=[
            {'name': 'Historico', 'data': data},
            {'name': 'Nivel Minimo de Operacion', 'data': min_level, 'type': 'line', 'color': '#660066'},
            {'name': 'Nivel Maximo de Operacion', 'data': max_level, 'type': 'line', 'color': '#FF0000'}
        ],
        y_min=site_config['ymin']
    )

    outflow_edit = TableView(column_names=('Dia', 'Caudal de Salida (cms)', 'Tiempo de salida (horas)'),
                             rows=[(forecasteddata[0], '0', '0'),
                                   (forecasteddata[1], '0', '0'),
                                   (forecasteddata[2], '0', '0'),
                                   (forecasteddata[3], '0', '0'),
                                   (forecasteddata[4], '0', '0'),
                                   (forecasteddata[5], '0', '0'),
                                   (forecasteddata[6], '0', '0'),
                                   ],
                             hover=True,
                             striped=True,
                             bordered=True,
                             condensed=True,
                             editable_columns=(False, 'Outflow', 'Time'),
                             row_ids=['day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7'],
                             classes="outflowtable"
                             )

    calculate = Button(display_text='Calcular Niveles del Embalse',
                       name='calculate',
                       style='',
                       icon='',
                       href='',
                       submit=False,
                       disabled=False,
                       attributes={"onclick": "calculatelevels()"},
                       classes='calcbut'
                       )

    outflow_button = Button(display_text='Ingresar caudales de salida',
                            name='dimensions',
                            style='',
                            icon='',
                            href='',
                            submit=False,
                            disabled=False,
                            attributes={"onclick": "outflowmodal()"},
                            classes='outflow_button'
                            )
    context = {
        'site_urls': gen_urls(request),
        'name': site_name,
        'timeseries_plot': timeseries_plot,
        'outflow_button': edit_passthrough(request, outflow_button),
        'calculate': calculate,
        'outflow_edit': outflow_edit,
        'show_edit': has_permission(request, 'update_data')
    }

    return render(request, 'reservoir_management/site_renderer.html', context)



'''