from database.data_io import DataIO
from logger import Logger

class Packet:
    def __init__(self, id, name, price, price_singular, uses, validity):
        self.id = id
        self.name = name
        self.price = price
        self.price_singular = price_singular
        self.uses = uses
        self.validity = validity

    def deserialize(decl):
        data = DataIO.parse_declaration(decl, "isffii")
        if data is None:
            return None

        if data[0] is None or data[0] < 1:
            Logger.log_error("Packet has invalid ID. It will be created with ID = 1")
            data[0] = 1

        packet = Packet(data[0], data[1], data[2], data[3], data[4], data[5])
        return packet

    def serialize(self):
        decl = DataIO.create_declaration([self.id, self.name, self.price, self.price_singular, self.uses, self.validity], "isffii")
        return decl

    def get_view(self):
        return "{} ({}лв.)".format(self.name, str(self.price))
