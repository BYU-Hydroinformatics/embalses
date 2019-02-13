from tethys_sdk.base import TethysAppBase, url_map_maker
from django.core.management import settings
import os

# todo: finish the getvolumefrombathymetry function in the model
# todo: make the reservoir page ajax controller send it and the ajax.js print it
# todo: make the table have a calculate button
# todo: make the calculate button work
# todo: finish the overviewinfo ajax function (depends on the getvolumefrombathymetry)


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
    currentpage = ''        # a custom setting added for keeping track of which reservoir is being viewed
    analytics = bool('analytical' in settings.INSTALLED_APPS and settings.GOOGLE_ANALYTICS_JS_PROPERTY_ID)

    with open(os.path.join(os.path.dirname(__file__), 'templates/embalses/analytics.html'), 'w') as file:
        if analytics:
            file.write("{% load google_analytics_js %}{% google_analytics_js %}")

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (

            # OVERVIEW PAGES
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
            UrlMap(
                name='instrucciones',
                url='embalses/instrucciones',
                controller='embalses.controllers.instructions'
            ),

            # SIMULATIONS PAGE
            UrlMap(
                name='simulaciones',
                url='embalses/simulaciones',
                controller='embalses.controllers.simulaciones'
            ),

            # RESERVOIR SPECIFIC PAGES
            UrlMap(                     # this is the controller for the page that shows reservoir specific stats
                name='template',        # {name} is an argument the controller needs to accept second
                url='embalses/{name}',
                controller='embalses.controllers.reservoirviewer'
            ),

            # CONTROLLERS FOR AJAX PAGES
            UrlMap(
                name='chartdata',
                url='embalses/ajax/respageinfo',
                controller='embalses.controllersAJAX.reservoir_pg_info'
            ),
            UrlMap(
                name='overview',
                url='embalses/ajax/overviewpage',
                controller='embalses.controllersAJAX.overviewpage'
            )
        )

        return url_maps
