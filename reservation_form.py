# This Python file uses the following encoding: utf-8
from reservation import Reservation, TimeInterval
from logger import Logger
from PySide2.QtCore import Qt, Slot, QTime
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QLineEdit, QGridLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QCompleter

schedule_font = QFont("Verdana", 12)
header_font = QFont("Verdana", 16, QFont.Bold)

class TimeIntervalWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.begin_hour_cbox = QComboBox(self)
        self.begin_hour_cbox.addItems(["{:02d}".format(hour) for hour in range(7, 22)])
        self.begin_hour_cbox.setCurrentIndex(2)
        self.begin_hour_cbox.setFont(schedule_font)
        self.begin_hour_cbox.setFixedSize(50, int(schedule_font.pointSize() * 2.3))
        self.layout.addWidget(self.begin_hour_cbox)

        self.begin_colon_label = QLabel(" : ")
        self.begin_colon_label.setFont(schedule_font)
        #self.begin_colon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.begin_colon_label)

        self.begin_minute_cbox = QComboBox(self)
        self.begin_minute_cbox.addItems(["{:02d}".format(minute) for minute in range(0, 65, 5)])
        self.begin_minute_cbox.setFont(schedule_font)
        self.begin_minute_cbox.setFixedSize(50, int(schedule_font.pointSize() * 2.3))
        self.layout.addWidget(self.begin_minute_cbox)

        self.dash_label = QLabel("    -    ")
        self.dash_label.setFont(schedule_font)
        #self.dash_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.dash_label)

        self.end_hour_cbox = QComboBox(self)
        self.end_hour_cbox.addItems(["{:02d}".format(hour) for hour in range(7, 22)])
        self.end_hour_cbox.setCurrentIndex(3)
        self.end_hour_cbox.setFont(schedule_font)
        self.end_hour_cbox.setFixedSize(50, int(schedule_font.pointSize() * 2.3))
        self.layout.addWidget(self.end_hour_cbox)

        self.end_colon_label = QLabel(" : ")
        self.end_colon_label.setFont(schedule_font)
        #self.end_colon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.end_colon_label)

        self.end_minute_cbox = QComboBox(self)
        self.end_minute_cbox.addItems(["{:02d}".format(minute) for minute in range(0, 65, 5)])
        self.end_minute_cbox.setFont(schedule_font)
        self.end_minute_cbox.setFixedSize(50, int(schedule_font.pointSize() * 2.3))
        self.layout.addWidget(self.end_minute_cbox)

        self.setLayout(self.layout)

    def get_time_interval(self):
        time_begin = QTime(
            int(self.begin_hour_cbox.currentText()),
            int(self.begin_minute_cbox.currentText())
        )
        time_end = QTime(
            int(self.end_hour_cbox.currentText()),
            int(self.end_minute_cbox.currentText())
        )
        time_interval = TimeInterval(time_begin, time_end)
        return time_interval

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
        time_interval = self.time_interval_widget.get_time_interval()
        client_name = self.line_edits["Клиент"].text().strip()
        client_exists = False
        for cl in self.clients:
            if client_name == cl.name:
                client = cl
                client_exists = True
        if not client_exists:
            Logger.log_error("Reserving for a client that doesn't exist. First register the client.")
            return
        procedure = self.line_edits["Процедура"].text().strip()
        percent = int(self.line_edits["%"].text().strip())
        kasa = int(self.line_edits["Каса"].text().strip())
        reservation = Reservation(employee, date, time_interval, client, procedure, percent, kasa)
        self.reserve_callback(reservation)

    def create_ui(self, deleteOldLayout = False):
        if deleteOldLayout:
            # Create a temporary QWidget object and set its layout to be the current old layout.
            # That way, the temporary object is immediately deleted and it deletes the layout and all of its children widgets
            QWidget().setLayout(self.layout)
            # After that we can just create a new layout
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.reserve_label = QLabel("Запазване на час")
        self.reserve_label.setFont(header_font)
        self.reserve_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.reserve_label, 0, 0, 1, 2)

        self.employee_cbox = QComboBox(self)
        self.employee_cbox.addItems(self.employees)
        self.employee_cbox.setFont(schedule_font)
        self.employee_cbox.setFixedSize(200, int(schedule_font.pointSize() * 2.5))
        self.layout.addWidget(self.employee_cbox, 1, 0, 1, 2)

        self.time_label = QLabel("Време")
        self.time_label.setFont(schedule_font)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.time_interval_widget = TimeIntervalWidget()
        self.time_interval_widget.setFixedSize(290, int(schedule_font.pointSize() * 2.3))
        self.layout.addWidget(self.time_label, 2, 0)
        self.layout.addWidget(self.time_interval_widget, 2, 1)

        self.atrib_names = ["Клиент", "Процедура", "%", "Каса"]
        atrib_positions = { "Клиент": [3, 0, 3, 1], "Процедура": [4, 0, 4, 1], "%": [5, 0, 5, 1], "Каса": [6, 0, 6, 1] }
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
            pos = atrib_positions[atrib]
            self.layout.addWidget(self.labels[atrib], pos[0], pos[1])
            self.layout.addWidget(self.line_edits[atrib], pos[2], pos[3])

        self.reserve_button = QPushButton("Запази")
        self.reserve_button.setFont(schedule_font)
        self.reserve_button.setFixedSize(100, 40)
        self.reserve_button.clicked.connect(self.reserve_pressed)
        self.layout.addWidget(self.reserve_button, 7, 1)

    def update_clients(self, new_clients):
        self.clients = new_clients
        self.create_ui(True)
