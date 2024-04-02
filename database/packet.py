from database.data_io import DataIO
from logger import Logger

class Packet:
    def __init__(self, id, name, price, uses, validity):
        self.id = id
        self.name = name
        self.price = price
        self.uses = uses
        self.validity = validity

    def deserialize(decl):
        data = DataIO.parse_declaration(decl, "isfii")

        if data[0] is None or data[0] < 1:
            Logger.log_error("Packet has invalid ID. It will be created with ID = 1")
            data[0] = 1

        packet = Packet(data[0], data[1], data[2], data[3], data[4])
        return packet