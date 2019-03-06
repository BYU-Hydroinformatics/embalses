from tethys_sdk.base import TethysAppBase, url_map_maker

# todo style the statistics divs/make them show up
# todo finish the simulation table math
# todo make sure the sfpt query section works
# todo translate the instructions
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
    description = ''
    tags = ''
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
                url='embalses/ajax/respageinfo',
                controller='embalses.controllersAJAX.reservoir_pg_info'
            ),
            UrlMap(
                name='overview',
                url='embalses/ajax/overviewpage',
                controller='embalses.controllersAJAX.overviewpage'
            ),
            UrlMap(
                name='simulationtable',
                url='embalses/ajax/simulationTable',
                controller='embalses.controllersAJAX.simulationtable'
            ),
            UrlMap(
                name='getsfptflows',
                url='embalses/ajax/getSFPTflows',
                controller='embalses.controllersAJAX.getsfptflows'
            ),
            UrlMap(
                name='reservoirstatistics',
                url='embalses/ajax/reservoirstatistics',
                controller='embalses.controllersAJAX.reservoirstatistics'
            ),
            UrlMap(
                name='updatesheet',
                url='embalses/ajax/updatesheet',
                controller='embalses.controllersAJAX.updatesheet'
            ),
        )

        return url_maps
