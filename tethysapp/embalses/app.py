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
    currentpage = ''        # a custom setting added for keeping track of which reservoir is being viewed

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (

            # CONTROLLERS FOR NAVIAGABLE PAGES
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
            )
        )

        return url_maps
