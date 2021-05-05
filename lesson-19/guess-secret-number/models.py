from smartninja_nosql.odm import Model


class User(Model):
    def __init__(self, name, email, secret_number, **kwargs):
        self.name = name
        self.email = email
        self.secret_number = secret_number

        super().__init__(**kwargs)
