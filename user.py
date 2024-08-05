class User:
    def __init__(self, iduser, lastname, firstname, middlename):
        self.id = iduser
        self.lastname = lastname
        self.firstname = firstname
        self.middlename = middlename

    def to_dict(self):
        return {
            "id": self.id,
            "lastname": self.lastname,
            "firstname": self.firstname,
            "middlename": self.middlename
        }
