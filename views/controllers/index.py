from models.core.server import baseHandler
class index( baseHandler ):

    def get(self):

        self.render("index.html")
