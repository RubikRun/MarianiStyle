from logger import Logger

from handlers.packets_handler import PacketsHandler
from ui.table_base import TableBase

from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHeaderView

class PacketsTableWidget(QWidget):
    def __init__(self, database, on_packets_update_callback):
        super().__init__()
        self.database = database
        self.on_packets_update_callback = on_packets_update_callback

        self.init_constants()
        self.create_ui()

    def init_constants(self):
        self.FONT = QFont("Verdana", 12)

    def create_ui(self, delete_old_layout = False):
        if delete_old_layout:
            # Create a temporary QWidget object and set its layout to be the current old layout.
            # That way, the temporary object is immediately deleted and it deletes the layout and all of its children widgets
            QWidget().setLayout(self.layout)
            # After that we can just create a new layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        packets_map = PacketsHandler.get_packets_map(self.database)

        def viewer_callback(packet, column, vrow):
            if column == 0:
                return packet.name
            elif column == 1:
                return str(int(packet.price))
            elif column == 2:
                return str(int(packet.price_singular))
            elif column == 3:
                return str(packet.uses)
            elif column == 4:
                return str(packet.validity)
            return ""

        def deleter_callback(packet_id, vrow):
            self.database.delete_packet(packet_id)
            self.on_packets_update_callback()

        def updater_callback(packet_id, column, str_val, vrow):
            packet = self.database.get_packet(packet_id)
            if packet is None:
                return False

            if column == 0:
                if len(str_val) < 2:
                    return False
                packet.name = str_val
            elif column == 1:
                try:
                    packet.price = float(str_val)
                except ValueError:
                    Logger.log_error("Updated price of packet is not a float. It will not be allowed.")
                    return False
            elif column == 2:
                try:
                    packet.price_singular = float(str_val)
                except ValueError:
                    Logger.log_error("Updated singular price of packet is not a float. It will not be allowed.")
                    return False
            elif column == 3:
                try:
                    packet.uses = int(str_val)
                except ValueError:
                    Logger.log_error("Updated uses of packet is not an int. It will not be allowed.")
                    return False
            elif column == 4:
                try:
                    packet.validity = int(str_val)
                except ValueError:
                    Logger.log_error("Updated validity of packet is not an int. It will not be allowed.")
                    return False
            else:
                return False

            self.on_packets_update_callback(False)
            return True

        self.table = TableBase("Пакети", len(packets_map), [1] * len(packets_map), 5,
                               ["Име", "Цена на пакет", "Единична цена", "Брой ползвания", "Валидност"],
                               [QHeaderView.Stretch, QHeaderView.Stretch, QHeaderView.Stretch, QHeaderView.ResizeToContents, QHeaderView.ResizeToContents],
                               packets_map, viewer_callback,
                               lambda obj, column, vrow : None, lambda obj, column, vrow : None,
                               deleter_callback,
                               updater_callback)
        self.layout.addWidget(self.table)
