from database.data_io import DataIO
from logger import Logger

class PacketInstance:
    def __init__(self, id, packet_id, client_id, employee_id, bought_on, use_count):
        self.id = id
        self.packet_id = packet_id
        self.client_id = client_id
        self.employee_id = employee_id
        self.bought_on = bought_on
        self.use_count = use_count

    def deserialize(decl):
        data = DataIO.parse_declaration(decl, "iiiiti")

        if data[0] is None or data[0] < 1:
            Logger.log_error("Packet instance has invalid ID. It will be created with ID = 1")
            data[0] = 1

        packet_instance = PacketInstance(data[0], data[1], data[2], data[3], data[4], data[5])
        return packet_instance

    def serialize(self):
        decl = DataIO.create_declaration([self.id, self.packet_id, self.client_id, self.employee_id, self.bought_on, self.use_count], "iiiiti")
        return decl