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
    def __init__(self, employees, employer, clients, packets, reserve_callback, buy_packet_callback, get_date_callback):
        super().__init__()
        self.employees = employees
        self.employer = employer
        self.clients = clients
        self.packets = packets
        self.reserve_callback = reserve_callback
        self.buy_packet_callback = buy_packet_callback
        self.get_date_callback = get_date_callback

        self.create_ui()

    @Slot()
    def reserve_pressed(self):
        employee = self.employee_cbox.currentText()
        date = self.get_date_callback()
        client_name = self.client_line_edit.text().strip()
        if client_name == "":
            Logger.log_error("Trying to reserve/buy but client name is empty")
            return
        client_exists = False
        for cl in self.clients:
            if client_name == cl.name:
                client = cl
                client_exists = True
        if not client_exists:
            Logger.log_error("Trying to reserve/buy for a client that doesn't exist. First register the client.")
            return

        packet_mode_index = self.packet_mode_cbox.currentIndex()
        if packet_mode_index == 0:
            time_interval = self.time_interval_widget.get_time_interval()
            procedure = self.procedure_line_edit.text().strip()
            price = int(self.price_line_edit.text().strip())
            percent = price
            kasa = price
            reservation = Reservation(employee, date, time_interval, client, procedure, percent, kasa)
            self.reserve_callback(reservation)
        elif packet_mode_index == 1:
            pass
        else:
            packet_name = self.packet_cbox.currentText()
            left_bracket_idx = packet_name.find("(")
            if left_bracket_idx < 2:
                Logger.log_error("Trying to buy a packet but selected packet name has wrong format. It should contain ( and packet name be to the left of it")
                return
            packet_name = packet_name[: left_bracket_idx - 1].strip()
            if packet_name == "":
                Logger.log_error("Trying to buy a packet but selected packet name is empty")
                return
            packet_exists = False
            for p in self.packets:
                if packet_name == p.name:
                    packet = p
                    packet_exists = True
                    break
            if not packet_exists:
                Logger.log_error("Trying to buy a packet but selected packet doesn't exist. Try first creating it in the packets window.")
                return
            self.buy_packet_callback(client, packet)

    def delete_widgets(self, widgets):
        for widget in widgets:
            index = self.layout.indexOf(widget)
            if index != -1:
                widget.setParent(None)
                widget.deleteLater()

    def create_widgets_for_packet_mode(self):
        packet_mode_index = self.packet_mode_cbox.currentIndex()

        self.widgets_of_current_packet_mode = []

        if packet_mode_index == 0:
            self.time_label = QLabel("Време")
            self.time_label.setFont(schedule_font)
            self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.time_interval_widget = TimeIntervalWidget()
            self.time_interval_widget.setFixedSize(290, int(schedule_font.pointSize() * 2.3))
            self.layout.addWidget(self.time_label, 4, 0)
            self.layout.addWidget(self.time_interval_widget, 4, 1)
            self.widgets_of_current_packet_mode.append(self.time_label)
            self.widgets_of_current_packet_mode.append(self.time_interval_widget)

            self.procedure_label = QLabel("Процедура")
            self.procedure_label.setFont(schedule_font)
            self.procedure_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.procedure_line_edit = QLineEdit(self)
            self.procedure_line_edit.setFont(schedule_font)
            self.layout.addWidget(self.procedure_label, 5, 0)
            self.layout.addWidget(self.procedure_line_edit, 5, 1)
            self.widgets_of_current_packet_mode.append(self.procedure_label)
            self.widgets_of_current_packet_mode.append(self.procedure_line_edit)

            self.price_label = QLabel("Цена")
            self.price_label.setFont(schedule_font)
            self.price_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.price_line_edit = QLineEdit(self)
            self.price_line_edit.setFont(schedule_font)
            self.layout.addWidget(self.price_label, 6, 0)
            self.layout.addWidget(self.price_line_edit, 6, 1)
            self.widgets_of_current_packet_mode.append(self.price_label)
            self.widgets_of_current_packet_mode.append(self.price_line_edit)

            self.reserve_button = QPushButton("Запази")
            self.reserve_button.setFont(schedule_font)
            self.reserve_button.setFixedSize(100, 40)
            self.reserve_button.clicked.connect(self.reserve_pressed)
            self.layout.addWidget(self.reserve_button, 7, 1)
            self.widgets_of_current_packet_mode.append(self.reserve_button)
        elif packet_mode_index == 1:
            self.time_label = QLabel("Време")
            self.time_label.setFont(schedule_font)
            self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.time_interval_widget = TimeIntervalWidget()
            self.time_interval_widget.setFixedSize(290, int(schedule_font.pointSize() * 2.3))
            self.layout.addWidget(self.time_label, 4, 0)
            self.layout.addWidget(self.time_interval_widget, 4, 1)
            self.widgets_of_current_packet_mode.append(self.time_label)
            self.widgets_of_current_packet_mode.append(self.time_interval_widget)

            self.packet_label = QLabel("Пакет")
            self.packet_label.setFont(schedule_font)
            self.packet_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.packet_cbox = QComboBox(self)
            self.packet_cbox.setFont(schedule_font)
            self.packet_cbox.setFixedSize(200, int(schedule_font.pointSize() * 2.5))
            self.layout.addWidget(self.packet_label, 5, 0)
            self.layout.addWidget(self.packet_cbox, 5, 1)
            self.widgets_of_current_packet_mode.append(self.packet_label)
            self.widgets_of_current_packet_mode.append(self.packet_cbox)

            self.reserve_button = QPushButton("Купи")
            self.reserve_button.setFont(schedule_font)
            self.reserve_button.setFixedSize(100, 40)
            self.reserve_button.clicked.connect(self.reserve_pressed)
            self.layout.addWidget(self.reserve_button, 6, 1)
            self.widgets_of_current_packet_mode.append(self.reserve_button)
        else:
            self.packet_label = QLabel("Пакет")
            self.packet_label.setFont(schedule_font)
            self.packet_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.packet_cbox = QComboBox(self)
            self.packet_cbox.addItems([packet.name + " (" + str(packet.price) + "лв.)" for packet in self.packets])
            self.packet_cbox.setFont(schedule_font)
            self.packet_cbox.setFixedSize(200, int(schedule_font.pointSize() * 2.5))
            self.layout.addWidget(self.packet_label, 4, 0)
            self.layout.addWidget(self.packet_cbox, 4, 1)
            self.widgets_of_current_packet_mode.append(self.packet_label)
            self.widgets_of_current_packet_mode.append(self.packet_cbox)

            self.reserve_button = QPushButton("Купи")
            self.reserve_button.setFont(schedule_font)
            self.reserve_button.setFixedSize(100, 40)
            self.reserve_button.clicked.connect(self.reserve_pressed)
            self.layout.addWidget(self.reserve_button, 7, 1)
            self.widgets_of_current_packet_mode.append(self.reserve_button)

    @Slot()
    def packet_mode_changed(self):
        self.delete_widgets(self.widgets_of_current_packet_mode)
        self.create_widgets_for_packet_mode()

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
        self.employee_cbox.addItems([self.employer] + self.employees)
        self.employee_cbox.setFont(schedule_font)
        self.employee_cbox.setFixedSize(100, int(schedule_font.pointSize() * 2.5))
        self.layout.addWidget(self.employee_cbox, 1, 0, 1, 2)

        self.client_label = QLabel("Клиент")
        self.client_label.setFont(schedule_font)
        self.client_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.client_line_edit = QLineEdit(self)
        self.client_line_edit.setFont(schedule_font)
        clientsNames = [client.name for client in self.clients]
        self.client_completer = QCompleter(clientsNames, self)
        self.client_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.client_line_edit.setCompleter(self.client_completer)
        self.client_line_edit.textChanged.connect(self.on_client_change)
        self.layout.addWidget(self.client_label, 2, 0)
        self.layout.addWidget(self.client_line_edit, 2, 1)

        self.packet_mode_cbox = QComboBox(self)
        self.packet_mode_cbox.addItems(["Без пакет", "С пакет", "Купуване на пакет"])
        self.packet_mode_cbox.setFont(schedule_font)
        self.packet_mode_cbox.setFixedSize(250, int(schedule_font.pointSize() * 2.5))
        self.packet_mode_cbox.currentIndexChanged.connect(self.packet_mode_changed)
        self.layout.addWidget(self.packet_mode_cbox, 3, 0, 1, 2)

        self.create_widgets_for_packet_mode()

    def update_clients(self, new_clients):
        self.clients = new_clients
        self.create_ui(True)

    def on_client_change(self):
        if self.packet_mode_cbox.currentIndex() != 1:
            return

        client_name = self.client_line_edit.text().strip()
        if client_name == "":
            self.packet_cbox.clear()
            return
        client_exists = False
        for cl in self.clients:
            if client_name == cl.name:
                client = cl
                client_exists = True
        if not client_exists:
            self.packet_cbox.clear()
            return

        self.packet_cbox.clear()
        self.packet_cbox.addItems([packet.name + " (" + str(packet.price) + "лв.)" for packet in client.packets])