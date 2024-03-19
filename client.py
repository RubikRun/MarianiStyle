class Client:
    def __init__(self, name, egn_cifri):
        self.name = name
        self.egn_cifri = egn_cifri

    def serialize(self):
        s = ""
        s += self.name + ";"
        s += self.egn_cifri
        return s
