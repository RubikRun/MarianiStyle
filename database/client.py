from database.data_io import DataIO
from logger import Logger

class Client:
    def __init__(self, id, name, phone, packet_instances):
        self.id = id
        self.name = name
        self.phone = phone
        self.packet_instances = packet_instances

    def deserialize(decl):
        data = DataIO.parse_declaration(decl, "issI")

        if data[0] is None or data[0] < 1:
            Logger.log_error("Client has invalid ID. It will be created with ID = 1")
            data[0] = 1

        client = Client(data[0], data[1], data[2], data[3])
        return client

    def serialize(self):
        decl = DataIO.create_declaration([self.id, self.name, self.phone, self.packet_instances], "issI")
        return decl