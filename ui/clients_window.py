from ui.client_register_form import ClientRegisterForm
from ui.clients_table_widget import ClientsTableWidget
from ui.client_packets_table_widget import ClientPacketsTableWidget

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QWidget, QGridLayout

class ClientsWindow(QDialog):
    def __init__(self, database, on_clients_update_callback, ):
        super().__init__()
        self.database = database
        self.on_clients_update_callback = on_clients_update_callback

        self.setWindowTitle("Клиенти")
        self.setGeometry(200, 200, 1400, 600)

        self.create_ui()

    def create_ui(self, deleteOldLayout = False):
        if deleteOldLayout:
            # Create a temporary QWidget object and set its layout to be the current old layout.
            # That way, the temporary object is immediately deleted and it deletes the layout and all of its children widgets
            QWidget().setLayout(self.layout)
            # After that we can just create a new layout
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.client_register_form = ClientRegisterForm(self.database, self.on_clients_update)
        self.layout.addWidget(self.client_register_form, 0, 0, 1, 1)

        self.clients_table_widget = ClientsTableWidget(self.database, self.on_client_selected, self.on_clients_update)
        self.layout.addWidget(self.clients_table_widget, 1, 0, 1, 1)

        self.client_packets_table_widget = ClientPacketsTableWidget(self.database, -1, self.on_packets_update)
        self.layout.addWidget(self.client_packets_table_widget, 1, 1, 1, 1)

    def on_clients_update(self):
        self.create_ui(True)
        self.on_clients_update_callback()

    def on_packets_update(self):
        self.on_clients_update_callback()

    def on_client_selected(self, client_id):
        self.client_packets_table_widget.set_client_id(client_id)