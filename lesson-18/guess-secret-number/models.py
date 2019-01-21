from smartninja_odm.odm import Model


class User(Model):
    def __init__(self, name, email):
        super().__init__()
        self.name = name
        self.email = email
