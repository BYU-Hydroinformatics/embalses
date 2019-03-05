from tethys_sdk.base import TethysAppBase, url_map_maker

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
        )

        return url_maps
