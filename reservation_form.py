# This Python file uses the following encoding: utf-8
from reservation import Reservation, TimeInterval
from logger import Logger
from PySide6.QtCore import Qt, Slot, QTime
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QLabel, QPushButton, QComboBox

schedule_font = QFont("Verdana", 12)

# Returns a QTime object parsing it from a string in format HH:mm
def parse_time(str):
    try:
        time_obj = QTime.fromString(str, "HH:mm")
        if time_obj.isValid():
            return time_obj
        else:
            Logger.log_error("Invalid time format when making a reservation")
            return None
    except ValueError as e:
        Logger.log_error("Cannot parse time when making a reservation: {}".format(str(e)))
        return None

# Returns a TimeInterval object parsing it from a string in format HH:mm-HH:mm
def parse_time_interval(str):
    str_parts = str.split('-')
    if len(str_parts) != 2:
        Logger.log_error("Invalid time interval when making a reservation")
        return None
    time_begin = parse_time(str_parts[0])
    if time_begin is None:
        Logger.log_error(" Invalid beginning time of time interval when making a reservation")
        return None
    time_end = parse_time(str_parts[1])
    if time_end is None:
        Logger.log_error(" Invalid ending time of time interval when making a reservation")
        return None
    return TimeInterval(time_begin, time_end)

class ReservationForm(QWidget):
    def __init__(self, employees, reserve_callback, get_date_callback):
        super().__init__()
        self.reserve_callback = reserve_callback
        self.get_date_callback = get_date_callback
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
        employee = self.employee_cbox.currentText()
        date = self.get_date_callback()
        time_interval = parse_time_interval(self.line_edits["Време"].text())
        client = self.line_edits["Клиент"].text()
        procedure = self.line_edits["Процедура"].text()
        percent = int(self.line_edits["%"].text())
        kasa = int(self.line_edits["Каса"].text())
        reservation = Reservation(employee, date, time_interval, client, procedure, percent, kasa)
        self.reserve_callback(reservation)
