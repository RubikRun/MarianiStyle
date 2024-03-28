from client import Client
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QLineEdit, QGridLayout, QLabel, QPushButton

schedule_font = QFont("Verdana", 12)
header_font = QFont("Verdana", 16, QFont.Bold)

class RegistrationForm(QWidget):
    def __init__(self, register_callback):
        super().__init__()
        self.register_callback = register_callback

        self.layout = QGridLayout(self)
        self.setContentsMargins(0, 0, 0, 110)

        self.register_label = QLabel("Регистриране на клиент")
        self.register_label.setFont(header_font)
        self.register_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.register_label, 0, 0, 1, 2)

        self.atrib_names = ["Име", "ЕГН цифри"]
        self.atrib_positions = { "Име": [1, 0, 1, 1], "ЕГН цифри": [2, 0, 2, 1] }
        self.labels = {}
        self.line_edits = {}
        for atrib in self.atrib_names:
            self.labels[atrib] = QLabel(atrib)
            self.labels[atrib].setFont(schedule_font)
            self.labels[atrib].setAlignment(Qt.AlignmentFlag.AlignRight)
            self.line_edits[atrib] = QLineEdit()
            self.line_edits[atrib].setFont(schedule_font)
            pos = self.atrib_positions[atrib]
            self.layout.addWidget(self.labels[atrib], pos[0], pos[1])
            self.layout.addWidget(self.line_edits[atrib], pos[2], pos[3])

        self.register_button = QPushButton("Регистрирай")
        self.register_button.setFont(schedule_font)
        self.register_button.setFixedSize(150, 40)
        self.register_button.clicked.connect(self.register_pressed)
        self.layout.addWidget(self.register_button, 3, 1)

    @Slot()
    def register_pressed(self):
        name = self.line_edits["Име"].text().strip()
        egn_cifri = self.line_edits["ЕГН цифри"].text().strip()

        client = Client(name, egn_cifri, [])
        self.register_callback(client, do_update_reservation_form = True)
