from smartninja_odm.odm import Model


class User(Model):
    def __init__(self, name, email, secret_number, **kwargs):
        self.name = name
        self.email = email
        self.secret_number = secret_number
        self.deleted = False

        super().__init__(**kwargs)
