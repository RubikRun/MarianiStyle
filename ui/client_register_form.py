from logger import Logger
from ui.input_field import InputField
from ui.text_button import TextButton

from database.client import Client

from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class ClientRegisterForm(QWidget):
    def __init__(self, database, on_register_update_callback):
        super().__init__()
        self.database = database
        self.on_register_update_callback = on_register_update_callback

        self.init_constants()
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

        self.register_label = QLabel("Регистриране на клиент")
        self.register_label.setFont(self.FONT_HEADER)
        self.register_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.register_label)

        self.name_input_field = InputField("Име", self.FONT)
        self.layout.addWidget(self.name_input_field)
        self.layout.setAlignment(self.name_input_field, Qt.AlignLeft)

        self.phone_input_field = InputField("Телефон", self.FONT)
        self.layout.addWidget(self.phone_input_field)
        self.layout.setAlignment(self.phone_input_field, Qt.AlignLeft)

        self.register_button = TextButton("Регистрирай", self.FONT, 150, 40, self.register_pressed)
        self.layout.addWidget(self.register_button)
        self.layout.setAlignment(self.register_button, Qt.AlignLeft)

    def init_constants(self):
        self.FONT = QFont("Verdana", 10)
        self.FONT_HEADER = QFont("Verdana", 12, QFont.Bold)

    @Slot()
    def register_pressed(self):
        name = self.name_input_field.get_text()
        phone = self.phone_input_field.get_text()
        if len(name) < 2:
            Logger.log_error("Invalid name of user. Should be at least 2 characters long")
            return
        if len(phone) < 2 or len(phone) > 20:
            Logger.log_error("Invalid phone number of user. Should be between 2 and 20 characters long")
            return

        client = Client(-1, name, phone, [])
        self.database.add_client(client)
        self.on_register_update_callback()