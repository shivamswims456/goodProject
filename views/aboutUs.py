from controllers.models.core.server import baseHandler

class aboutUs(baseHandler):

    def get(self):

        self.render("aboutUs.html")