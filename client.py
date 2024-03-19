from logger import Logger

class Client:
    def __init__(self, name, egn_cifri):
        self.name = name
        self.egn_cifri = egn_cifri

    def serialize(self):
        s = ""
        s += self.name + ";"
        s += self.egn_cifri
        return s

    # Deserializes a client from a declaration string. Returns the client.
    def deserialize(decl):
        if decl is None or decl == "":
            Logger.log_error("Client declaration is empty. Client will be skipped")
            return None
        decl_parts = decl.split(';')
        if len(decl_parts) != 2:
            Logger.log_error("Client declaration is invalid, should have 2 parts. Client will be skipped")
            return None
        name = decl_parts[0].strip()
        if name == "":
            Logger.log_error("Name part of a client is empty. Client will be skipped")
            return None
        egn_cifri = decl_parts[1].strip()
        if egn_cifri == "":
            Logger.log_error("EGN cifri part of a client is empty. Client will be skipped")
            return None

        client = Client(name, egn_cifri)
        return client
