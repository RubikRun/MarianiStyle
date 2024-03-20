# This Python file uses the following encoding: utf-8
from reservation import Reservation, TimeInterval
from logger import Logger
from PySide2.QtCore import Qt, Slot, QTime
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QLineEdit, QGridLayout, QLabel, QPushButton, QComboBox, QCompleter

schedule_font = QFont("Verdana", 12)
header_font = QFont("Verdana", 16, QFont.Bold)

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
        Logger.log_error("Invalid beginning time of time interval when making a reservation")
        return None
    time_end = parse_time(str_parts[1])
    if time_end is None:
        Logger.log_error("Invalid ending time of time interval when making a reservation")
        return None
    return TimeInterval(time_begin, time_end)

class ReservationForm(QWidget):
    def __init__(self, employees, clients, reserve_callback, get_date_callback):
        super().__init__()
        self.employees = employees
        self.clients = clients
        self.reserve_callback = reserve_callback
        self.get_date_callback = get_date_callback

        self.create_ui()

    @Slot()
    def reserve_pressed(self):
        employee = self.employee_cbox.currentText()
        date = self.get_date_callback()
        time_interval = parse_time_interval(self.line_edits["Време"].text().strip())
        client = self.line_edits["Клиент"].text().strip()
        procedure = self.line_edits["Процедура"].text().strip()
        percent = int(self.line_edits["%"].text().strip())
        kasa = int(self.line_edits["Каса"].text().strip())
        reservation = Reservation(employee, date, time_interval, client, procedure, percent, kasa)
        self.reserve_callback(reservation)

    def create_ui(self):
        self.layout = QGridLayout(self)
        self.setContentsMargins(0, 0, 0, 0)

        self.reserve_label = QLabel("Запазване на час")
        self.reserve_label.setFont(header_font)
        self.reserve_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.reserve_label, 0, 0, 1, 2)

        self.employee_cbox = QComboBox(self)
        self.employee_cbox.addItems(self.employees)
        self.employee_cbox.setFont(schedule_font)
        self.employee_cbox.setFixedSize(200, int(schedule_font.pointSize() * 2.5))
        self.layout.addWidget(self.employee_cbox, 1, 0, 1, 2)

        self.atrib_names = ["Време", "Клиент", "Процедура", "%", "Каса"]
        self.atrib_positions = { "Време": [2, 0, 2, 1], "Клиент": [3, 0, 3, 1], "Процедура": [4, 0, 4, 1], "%": [5, 0, 5, 1], "Каса": [6, 0, 6, 1] }
        self.labels = {}
        self.line_edits = {}
        for atrib in self.atrib_names:
            self.labels[atrib] = QLabel(atrib)
            self.labels[atrib].setFont(schedule_font)
            self.labels[atrib].setAlignment(Qt.AlignmentFlag.AlignRight)
            if atrib == "Клиент":
                clientsNames = [client.name for client in self.clients]
                self.line_edits[atrib] = QLineEdit(self)
                self.client_completer = QCompleter(clientsNames, self)
                self.client_completer.setCaseSensitivity(Qt.CaseInsensitive)
                self.line_edits[atrib].setCompleter(self.client_completer)
            else:
                self.line_edits[atrib] = QLineEdit()
            self.line_edits[atrib].setFont(schedule_font)
            pos = self.atrib_positions[atrib]
            self.layout.addWidget(self.labels[atrib], pos[0], pos[1])
            self.layout.addWidget(self.line_edits[atrib], pos[2], pos[3])

        self.reserve_button = QPushButton("Запази")
        self.reserve_button.setFont(schedule_font)
        self.reserve_button.setFixedSize(100, 40)
        self.reserve_button.clicked.connect(self.reserve_pressed)
        self.layout.addWidget(self.reserve_button, 7, 1)

    def update_clients(self, new_clients):
        self.clients = new_clients
        clientsNames = [client.name for client in self.clients]
        self.line_edits["Клиент"] = QLineEdit(self)
        self.client_completer = QCompleter(clientsNames, self)
        self.client_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.line_edits["Клиент"].setCompleter(self.client_completer)
