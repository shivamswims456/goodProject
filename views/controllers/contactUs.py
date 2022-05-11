from models.core.server import baseHandler


class contactUs(baseHandler):

    def get(self):

        self.render("contactUs.html")

