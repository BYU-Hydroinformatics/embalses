from tethys_sdk.base import TethysAppBase, url_map_maker

# todo finish the simulation table math (see the ajax.js function for the simulation table for notes)
# todo translate the instructions
# todo make the update button not ask for login every time
# todo OPTIONAL- generate a report based on the simulations
# todo OPTIONAL- create a persistent store of old reports
# todo OPTIONAL- add the sync button to many pages
# todo OPTIONAL- add a modal button for finding help videos for each page
# todo OPTIONAL- make the forecasting more complicated based on heights (warnings, etc)
# todo OPTIONAL- give an option to email the finished report to someone
# todo OPTIONAL- let the user toggle between elevations and depths on the historical charts


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
    description = 'An application for forecasting future reservoir levels in the Dominican Republic'
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
                name='simulations_short',
                url='embalses/simulaciones-breves',
                controller='embalses.controllers.simulations_short'
            ),
            UrlMap(
                name='simulations_long',
                url='embalses/simulaciones-prolngados',
                controller='embalses.controllers.simulations_long'
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
        )

        return url_maps
