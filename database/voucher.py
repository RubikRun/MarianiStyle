from database.data_io import DataIO
from logger import Logger

from PySide2.QtCore import QDateTime

class Voucher:
    def __init__(self, id, client_id, employee_id, bought_on, validity, price, spent):
        self.id = id
        self.client_id = client_id
        self.employee_id = employee_id
        self.bought_on = bought_on
        self.validity = validity
        self.price = price
        self.spent = spent

    def deserialize(decl):
        data = DataIO.parse_declaration(decl, "iiitiff")
        if data is None:
            return None

        if data[0] is None or data[0] < 1:
            Logger.log_error("Voucher has invalid ID. It will be created with ID = 1")
            data[0] = 1

        voucher = Voucher(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        return voucher

    def serialize(self):
        decl = DataIO.create_declaration([self.id, self.client_id, self.employee_id, self.bought_on, self.validity, self.price, self.spent], "iiitiff")
        return decl

    def get_view(self):
        return "Ваучер {}лв".format(int(self.price))

    def is_expired(self, database):
        current = QDateTime.currentDateTime()
        endtime = self.bought_on.addMonths(self.validity)

        return current > endtime

