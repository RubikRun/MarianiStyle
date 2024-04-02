from database.data_io import DataIO
from logger import Logger

class Reservation:
    def __init__(self, id, employee_id, client_id, date_time, procedure, packet_instance_id, percent, kasa, bg_colors, fg_colors):
        self.id = id
        self.employee_id = employee_id
        self.client_id = client_id
        self.date_time = date_time
        self.procedure = procedure
        self.packet_instance_id = packet_instance_id
        self.percent = percent
        self.kasa = kasa
        self.bg_colors = bg_colors
        self.fg_colors = fg_colors

    def deserialize(decl):
        data = DataIO.parse_declaration(decl, "iiitsiffCC")
        if data is None:
            return None

        if data[0] is None or data[0] < 1:
            Logger.log_error("Reservation has invalid ID. It will be created with ID = 1")
            data[0] = 1

        reservation = Reservation(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9])
        return reservation

    def serialize(self):
        decl = DataIO.create_declaration(
            [self.id, self.employee_id, self.client_id, self.date_time, self.procedure, self.packet_instance_id, self.percent, self.kasa, self.bg_colors, self.fg_colors],
            "iiitsiffCC"
        )
        return decl