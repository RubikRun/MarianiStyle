from logger import Logger
from ui.input_field import InputField
from ui.text_button import TextButton

from database.packet import Packet

from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class PacketRegisterForm(QWidget):
    def __init__(self, database, on_packets_update_callback):
        super().__init__()
        self.database = database
        self.on_packets_update_callback = on_packets_update_callback

        self.init_constants()
        self.create_ui()

    def init_constants(self):
        self.FONT = QFont("Verdana", 12)
        self.FONT_HEADER = QFont("Verdana", 16, QFont.Bold)

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

        self.register_label = QLabel("Създаване на пакет")
        self.register_label.setFont(self.FONT_HEADER)
        self.register_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.register_label)

        self.name_input_field = InputField("Име", self.FONT)
        self.layout.addWidget(self.name_input_field)
        self.layout.setAlignment(self.name_input_field, Qt.AlignLeft)

        self.price_input_field = InputField("Цена на пакет", self.FONT)
        self.layout.addWidget(self.price_input_field)
        self.layout.setAlignment(self.price_input_field, Qt.AlignLeft)

        self.price_singular_input_field = InputField("Цена без пакет", self.FONT)
        self.layout.addWidget(self.price_singular_input_field)
        self.layout.setAlignment(self.price_singular_input_field, Qt.AlignLeft)

        self.uses_input_field = InputField("Брой ползвания", self.FONT)
        self.layout.addWidget(self.uses_input_field)
        self.layout.setAlignment(self.uses_input_field, Qt.AlignLeft)

        self.validity_input_field = InputField("Валидност", self.FONT)
        self.layout.addWidget(self.validity_input_field)
        self.layout.setAlignment(self.validity_input_field, Qt.AlignLeft)

        self.register_button = TextButton("Създай", self.FONT, 150, 40, self.register_pressed)
        self.layout.addWidget(self.register_button)
        self.layout.setAlignment(self.register_button, Qt.AlignLeft)

    @Slot()
    def register_pressed(self):
        name = self.name_input_field.get_text()
        price_str = self.price_input_field.get_text()
        price_singular_str = self.price_singular_input_field.get_text()
        uses_str = self.uses_input_field.get_text()
        validity_str = self.validity_input_field.get_text()
        if len(name) < 2:
            Logger.log_error("Invalid name of user. Should be at least 2 characters long")
            return
        try:
            price = float(price_str)
        except ValueError:
            Logger.log_error("Input price of new packet is not a float")
            return
        try:
            price_singular = float(price_str)
        except ValueError:
            Logger.log_error("Input singular price of new packet is not a float")
            return
        try:
            uses = float(uses_str)
        except ValueError:
            Logger.log_error("Input uses of new packet is not a float")
            return
        try:
            validity = float(validity_str)
        except ValueError:
            Logger.log_error("Input validity of new packet is not a float")
            return

        packet = Packet(-1, name, price, price_singular, uses, validity)
        self.database.add_packet(packet)
        self.on_packets_update_callback()