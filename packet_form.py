from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QLineEdit, QGridLayout, QLabel, QPushButton, QComboBox

schedule_font = QFont("Verdana", 12)
header_font = QFont("Verdana", 16, QFont.Bold)

class PacketForm(QWidget):
    def __init__(self, create_packet_callback):
        super().__init__()
        self.create_packet_callback = create_packet_callback

        self.layout = QGridLayout(self)
        self.setContentsMargins(0, 0, 0, 0)

        self.packet_label = QLabel("Създаване на пакет")
        self.packet_label.setFont(header_font)
        self.packet_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.packet_label, 0, 0, 1, 2)

        self.name_label = QLabel("Име")
        self.name_label.setFont(schedule_font)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.name_line_edit = QLineEdit()
        self.name_line_edit.setFont(schedule_font)
        self.layout.addWidget(self.name_label, 1, 0)
        self.layout.addWidget(self.name_line_edit, 1, 1)

        self.price_label = QLabel("Цена")
        self.price_label.setFont(schedule_font)
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.price_line_edit = QLineEdit()
        self.price_line_edit.setFont(schedule_font)
        self.layout.addWidget(self.price_label, 2, 0)
        self.layout.addWidget(self.price_line_edit, 2, 1)

        self.count_label = QLabel("Брой ползвания")
        self.count_label.setFont(schedule_font)
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.count_cbox = QComboBox(self)
        self.count_cbox.addItems([str(count) for count in range(2, 11)])
        self.count_cbox.setFont(schedule_font)
        self.count_cbox.setFixedSize(100, int(schedule_font.pointSize() * 2.3))
        self.layout.addWidget(self.count_label, 3, 0)
        self.layout.addWidget(self.count_cbox, 3, 1)

        self.validity_label = QLabel("Месеци валидност")
        self.validity_label.setFont(schedule_font)
        self.validity_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.validity_cbox = QComboBox(self)
        self.validity_cbox.addItems([str(count) for count in range(2, 11)])
        self.validity_cbox.setFont(schedule_font)
        self.validity_cbox.setFixedSize(100, int(schedule_font.pointSize() * 2.3))
        self.layout.addWidget(self.validity_label, 4, 0)
        self.layout.addWidget(self.validity_cbox, 4, 1)

        self.create_packet_button = QPushButton("Създай пакет")
        self.create_packet_button.setFont(schedule_font)
        self.create_packet_button.setFixedSize(150, 40)
        self.create_packet_button.clicked.connect(self.create_packet_pressed)
        self.layout.addWidget(self.create_packet_button, 5, 1)

    @Slot()
    def create_packet_pressed(self):
        pass
        #self.create_packet_callback(client)
