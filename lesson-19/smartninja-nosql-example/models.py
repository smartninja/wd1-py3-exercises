from smartninja_nosql.odm import Model


class User(Model):
    def __init__(self, name, email, **kwargs):
        self.name = name
        self.email = email

        super().__init__(**kwargs)  # this line calls the __init__ method from the parent class
