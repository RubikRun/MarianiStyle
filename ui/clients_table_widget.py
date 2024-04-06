from logger import Logger

from handlers.clients_handler import ClientsHandler
from ui.table_base import TableBase

from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHeaderView

class ClientsTableWidget(QWidget):
    def __init__(self, database, on_client_selected_callback, on_clients_update_callback):
        super().__init__()
        self.database = database
        self.on_client_selected_callback = on_client_selected_callback
        self.on_clients_update_callback = on_clients_update_callback

        self.create_ui()

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

        clients_map = ClientsHandler.get_clients_sorted_map(self.database)

        def viewer_callback(client, column, vrow):
            if column == 0:
                return client.name
            elif column == 1:
                return client.phone
            return ""

        def deleter_callback(client_id, vrow):
            self.database.delete_client(client_id)
            self.on_clients_update_callback()

        def updater_callback(client_id, column, str_val, vrow):
            client = self.database.get_client(client_id)
            if client is None:
                return False

            if column == 0:
                if len(str_val) < 2:
                    return False
                client.name = str_val
            elif column == 1:
                client.phone = str_val
            else:
                return False

            self.on_clients_update_callback()
            return True

        self.table = TableBase("Клиенти", len(clients_map), [1] * len(clients_map), 2, ["Име", "Телефон"], [QHeaderView.Stretch, QHeaderView.ResizeToContents],
                               clients_map, viewer_callback,
                               lambda obj, column, vrow : None, lambda obj, column, vrow : None,
                               deleter_callback,
                               updater_callback,
                               self.on_client_selected)
        self.layout.addWidget(self.table)

    def on_client_selected(self, client_id):
        self.on_client_selected_callback(client_id)