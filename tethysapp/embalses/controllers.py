from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.permissions import has_permission

from .tools import generate_app_urls
from .model import reservoirs

from tethys_sdk.gizmos import SelectInput

reservoirs = reservoirs()


@login_required()
def home(request):
    """
    controller for the home page
    """
    # The map on this page is handled entirely using leaflet and javascript
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
def instructions(request):
    """
    controller for the instructions page
    """

    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs)
    }

    return render(request, 'embalses/instructions.html', context)


@login_required()
def simulations(request):
    """
    controller for the instructions page
    """

    # list of reservoirs to choose from for the simulation
    res_list = SelectInput(
        display_text='',
        name='reservoir',
        multiple=False,
        options=[(reservoir, reservoirs[reservoir]) for reservoir in reservoirs],
        select2_options={
            'placeholder': 'Escoger un Embalse',
            'allowClear': True
        },
    )

    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs),
        'res_list': res_list,
    }

    return render(request, 'embalses/simulations.html', context)


@login_required()
def reservoirviewer(request, name):
    """
    controller for the reservoir specific page template. The code does 2 functions in this order:
    - This calls the gethistoricaldata method which takes a long time to read 35 years of daily data
    - Calls getdates to populate the next available forecast dates in the simulation tables
    """
    from .app import Embalses as App

    for reservoir in reservoirs:
        if reservoirs[reservoir] == name:
            name = reservoir
            App.currentpage = name
            break

    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs),
        'name': name,
    }

    return render(request, 'embalses/reservoir.html', context)
