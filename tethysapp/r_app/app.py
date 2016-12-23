from tethys_sdk.base import TethysAppBase, url_map_maker


class RApp(TethysAppBase):
    """
    Tethys app class for R app.
    """

    name = 'R Analyst - Experimental'
    index = 'r_app:home'
    icon = 'r_app/images/icon.gif'
    package = 'r_app'
    root_url = 'r-app'
    color = '#0060aa'
    description = 'Run R script in Tethys app'
    tags = ''
    enable_feedback = False
    feedback_emails = []

        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='r-app',
                           controller='r_app.controllers.home'),
                    UrlMap(name='scriptView',
                           url='r-app/scriptView',
                           controller='r_app.controllers.scriptView'),
                    UrlMap(name='scriptRun',
                           url='r-app/scriptRun',
                           controller='r_app.controllers.scriptRun'),
        )

        return url_maps