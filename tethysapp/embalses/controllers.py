# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from tethys_sdk.permissions import has_permission

from .tools import generate_app_urls
from .model import reservoirs
from .app import Embalses as App

from tethys_sdk.gizmos import SelectInput

import os

reservoirs = reservoirs()

MOUNT_PATH = os.environ.get('TETHYS_MOUNT_PATH') or '/'
MOUNT_PATH = os.path.join(MOUNT_PATH, '')


def render_with_mount_path(request, templateURL, context):
    context['mount_path'] = MOUNT_PATH
    return render(request, templateURL, context)


@login_required()
def home(request):
    """
    controller for the home page
    """
    # The map on this page is handled entirely using leaflet and javascript
    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs),
        'youtubelink': App.youtubelink
    }

    return render_with_mount_path(request, 'embalses/home.html', context)


@login_required()
def reportar(request):
    """
    controller for the reporting page
    """

    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs),
        'youtubelink': App.youtubelink
    }

    return render_with_mount_path(request, 'embalses/reportar.html', context)


@login_required()
def instructions(request):
    """
    controller for the instructions page
    """

    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs),
        'youtubelink': App.youtubelink
    }

    return render_with_mount_path(request, 'embalses/instructions.html', context)


@login_required()
def simulations(request):
    """
    controller for the instructions page
    """

    # list of reservoirs to choose from for the simulation
    options = [(reservoir, reservoirs[reservoir]) for reservoir in reservoirs]
    options.sort()
    res_list = SelectInput(
        display_text='',
        name='reservoir',
        multiple=False,
        options=options,
        select2_options={
            'placeholder': 'Escoger un Embalse',
            'allowClear': True
        },
    )

    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs),
        'res_list': res_list,
        'youtubelink': App.youtubelink
    }

    return render_with_mount_path(request, 'embalses/simulations.html', context)


@login_required()
def reservoirviewer(request, name):
    """
    controller for the reservoir specific page template. The code does 2 functions in this order:
    - This calls the gethistoricaldata method which takes a long time to read 35 years of daily data
    - Calls getdates to populate the next available forecast dates in the simulation tables
    """
    from .app import Embalses as App

    reservoir_name = ""

    for reservoir in reservoirs:
        if reservoirs[reservoir] == name:
            reservoir_name = reservoir
            break

    context = {
        'admin': has_permission(request, 'update_data'),
        'urls': generate_app_urls(request, reservoirs),
        'name': reservoir_name,
        'youtubelink': App.youtubelink
    }

    return render_with_mount_path(request, 'embalses/reservoir.html', context)
