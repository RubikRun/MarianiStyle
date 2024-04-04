from ui.client_register_form import ClientRegisterForm

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QWidget, QGridLayout

class ClientsWindow(QDialog):
    def __init__(self, parent, database, on_client_register_callback):
        super().__init__(parent)
        self.database = database
        self.on_client_register_callback = on_client_register_callback

        self.setWindowTitle("Клиенти")
        self.setGeometry(200, 200, 800, 800)

        self.create_ui()

    def create_ui(self, deleteOldLayout = False):
        if deleteOldLayout:
            # Create a temporary QWidget object and set its layout to be the current old layout.
            # That way, the temporary object is immediately deleted and it deletes the layout and all of its children widgets
            QWidget().setLayout(self.layout)
            # After that we can just create a new layout
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.client_register_form = ClientRegisterForm(self.database, self.on_client_register)
        self.layout.addWidget(self.client_register_form, 0, 0, 1, 1)

    def on_client_register(self):
        self.create_ui(True)
        self.on_client_register_callback()