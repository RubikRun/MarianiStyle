# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QLabel, QPushButton, QComboBox

schedule_font = QFont("Verdana", 12)

class ReservationForm(QWidget):
    def __init__(self, reserve_callback, employees):
        super().__init__()
        self.reserve_callback = reserve_callback
        self.employees = employees

        self.layout = QGridLayout(self)
        self.setContentsMargins(0, 0, 1300, 0)

        self.employee_cbox = QComboBox()
        self.employee_cbox.addItems(self.employees)
        self.employee_cbox.setFont(schedule_font)
        self.layout.addWidget(self.employee_cbox, 0, 1)

        self.atrib_names = ["Време", "Клиент", "Процедура", "%", "Каса"]
        self.atrib_positions = { "Време": [1, 0, 1, 1], "Клиент": [2, 0, 2, 1], "Процедура": [3, 0, 3, 1], "%": [4, 0, 4, 1], "Каса": [5, 0, 5, 1] }
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

        self.reserve_button = QPushButton("Запази")
        self.reserve_button.setFont(schedule_font)
        self.reserve_button.clicked.connect(self.reserve_pressed)
        self.layout.addWidget(self.reserve_button, 6, 1)

    @Slot()
    def reserve_pressed(self):
        self.reserve_callback()
