from tethys_sdk.base import TethysAppBase, url_map_maker
from django.core.management import settings     # To access settings.py in the portal and check for analytics
import os


class Embalses(TethysAppBase):
    """
    Tethys app class for Herramientas de Operaciones de los Embalses.
    """

    name = 'Administracion de los Embalses'
    index = 'embalses:home'
    icon = 'embalses/images/indrhi.png'
    package = 'embalses'
    root_url = 'embalses'
    color = '#01AEBF'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []

    # handle implementing analytics if available on this portal. python 2/3 compatible
    workingdir = os.path.dirname(__file__)
    with open(os.path.join(workingdir, 'templates/embalses/analytics.html'), 'w') as file:
        if 'analytical' in settings.INSTALLED_APPS:
            file.write("{% load google_analytics_js %}{% google_analytics_js %}")

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='embalses',
                controller='embalses.controllers.home'
            ),
            UrlMap(
                name='reportar',
                url='embalses/reportar',
                controller='embalses.controllers.reportar'
            ),
            UrlMap(                     # this is the controller for the page that shows reservoir specific stats
                name='template',        # {name} is an argument the controller needs to accept second
                url='embalses/{name}',
                controller='embalses.controllers.reservoirviewer'
            ),
        )

        return url_maps
