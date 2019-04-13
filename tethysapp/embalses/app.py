# -*- coding: UTF-8 -*-

from tethys_sdk.base import TethysAppBase, url_map_maker

# todo add warnings to the simulation button (skim from hec models)
# todo translate the instructions
# todo make the update button not ask for login every time (make it work on the server???)
# todo record demonstration videos

# todo OPTIONAL- create a persistent store of old reports (header button)
# todo OPTIONAL- give an option to email/download the finished report
# todo OPTIONAL- let the user toggle between elevations and depths on the historical charts
# todo OPTIONAL- add hydrologic factors to analysis like evaporation or infiltration?


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
    description = 'Una aplicación para visualizar datos históricos y hacer simulaciones de elevaciones para los ' \
                  'embalses en la Republica Dominicana.'
    tags = 'reservoirs, hydrology, streamflow prediction'
    enable_feedback = False
    feedback_emails = []
    currentpage = ''        # a custom attribute added for keeping track of which reservoir is being viewed

    def url_maps(self):
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

            # SIMULATIONS PAGES
            UrlMap(
                name='simulations',
                url='embalses/simulaciones',
                controller='embalses.controllers.simulations'
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
                url='embalses/ajax/respgplot',
                controller='embalses.ajax.reservoirpageplot'
            ),
            UrlMap(
                name='overview',
                url='embalses/ajax/overviewpage',
                controller='embalses.ajax.overviewpage'
            ),
            UrlMap(
                name='simulationtable',
                url='embalses/ajax/simulationTable',
                controller='embalses.ajax.simulationtable'
            ),
            UrlMap(
                name='getsfptflows',
                url='embalses/ajax/getSFPTflows',
                controller='embalses.ajax.getsfptflows'
            ),
            UrlMap(
                name='reservoirstatistics',
                url='embalses/ajax/reservoirstatistics',
                controller='embalses.ajax.reservoirstatistics'
            ),
            UrlMap(
                name='updatesheet',
                url='embalses/ajax/updatesheet',
                controller='embalses.ajax.updatesheet'
            ),
            UrlMap(
                name='performsimulation',
                url='embalses/ajax/performsimulation',
                controller='embalses.ajax.performsimulation'
            ),
        )

        return url_maps
