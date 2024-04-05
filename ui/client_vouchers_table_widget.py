from handlers.client_vouchers_handler import ClientVouchersHandler
from ui.table_base import TableBase

from PySide2.QtCore import Qt, QDateTime
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHeaderView

class ClientVouchersTableWidget(QWidget):
    def __init__(self, database, client_id, on_vouchers_update_callback):
        super().__init__()
        self.database = database
        self.client_id = client_id
        self.on_vouchers_update_callback = on_vouchers_update_callback

        self.init_constants()
        self.create_ui()

    def init_constants(self):
        self.FONT = QFont("Verdana", 10)

    def create_ui(self, delete_old_layout = False):
        if delete_old_layout:
            # Create a temporary QWidget object and set its layout to be the current old layout.
            # That way, the temporary object is immediately deleted and it deletes the layout and all of its children widgets
            QWidget().setLayout(self.layout)
            # After that we can just create a new layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        should_be_empty = False
        if self.client_id >= 0:
            self.client = self.database.get_client(self.client_id)
            if self.client is None:
                should_be_empty = True
        else:
            should_be_empty = True

        if should_be_empty:
            vouchers_map = {}
        else:
            vouchers_map = ClientVouchersHandler.get_vouchers_map(self.database, self.client_id)

        def viewer_callback(voucher, column, vrow):
            if column == 0:
                return "{}лв".format(int(voucher.price))
            elif column == 1:
                return "{}лв".format(int(voucher.spent))
            elif column == 2:
                return voucher.bought_on.toString("dd.MM.yyyy HH:mm")
            elif column == 3:
                current = QDateTime.currentDateTime()
                endtime = voucher.bought_on.addMonths(voucher.validity)

                if current >= endtime:
                    return "Изтекъл на ".format(endtime.toString("dd.MM.yyyy HH:mm"))

                months = 0
                while months < 20 and (current < endtime):
                    current = current.addMonths(1)
                    months += 1
                if months > 1:
                    current = current.addMonths(-1)
                    months -= 1
                days = current.daysTo(endtime)

                if days == 31:
                    days = 0
                    months += 1

                if days == 0:
                    if months > 0:
                        return "{} месеца".format(months)
                    else:
                        return "0 дни"
                if months == 0:
                    return "{} дни".format(days)
                return "{} месеца и {} дена".format(months, days)
            return ""

        def deleter_callback(voucher_id, vrow):
            self.database.delete_voucher(voucher_id)
            self.on_vouchers_update_callback()

        if should_be_empty:
            table_name = ""
        else:
            table_name = "Ваучери на {}".format(self.client.get_view())

        self.table = TableBase(table_name, len(vouchers_map), [1] * len(vouchers_map), 4,
                               ["Стойност", "Използвани", "Купен кога", "Изтича след"], [QHeaderView.Stretch, QHeaderView.ResizeToContents, QHeaderView.Stretch, QHeaderView.Stretch],
                               vouchers_map, viewer_callback,
                               lambda obj, column, vrow : None, lambda obj, column, vrow : None,
                               deleter_callback,
                               lambda id, col, s, vrow : False)
        self.layout.addWidget(self.table)

    def set_client_id(self, client_id):
        self.client_id = client_id
        self.create_ui(True)