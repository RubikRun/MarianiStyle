from schedule_widget import ScheduleWidget
from schedule import Schedule
from logger import Logger
from client import Client
from packet import Packet
from reservation_form import ReservationForm
from registration_form import RegistrationForm
from settings_window import SettingsWindow

from PySide2.QtGui import QFont
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton

schedule_font = QFont("Verdana", 12)

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.load_clients("database/clients.data")
        self.load_packets("database/packets.data")

        self.schedule = Schedule(self.clients)
        self.schedule.load("database/schedule.data")
        self.employees = self.schedule.get_employees()

        self.schedule_widget = ScheduleWidget(self.schedule)
        self.reservation_form = ReservationForm(self.employees, self.clients, self.schedule_widget.add_reservation, self.schedule_widget.get_date)
        self.registration_form = RegistrationForm(self.register_client)

        self.settings_button = QPushButton("Настройки")
        self.settings_button.setFont(schedule_font)
        self.settings_button.setFixedSize(150, 40)
        self.settings_button.clicked.connect(self.open_settings_window)

        self.settings_window = None

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.layout.addWidget(self.settings_button, 0, 1, 1, 1)
        self.layout.setAlignment(self.settings_button, Qt.AlignRight)
        self.layout.addWidget(self.schedule_widget, 1, 0, 1, 2)
        self.layout.addWidget(self.reservation_form, 2, 0, 1, 1)
        self.layout.addWidget(self.registration_form, 2, 1, 1, 1)

    @Slot()
    def open_settings_window(self):
        self.settings_window = SettingsWindow(self, self.packets, self.add_packet)
        self.settings_window.show()

    def load_clients(self, filepath):
        self.clients = []
        try:
            file = open(filepath, 'r', encoding = "utf-8")
        except FileNotFoundError:
            Logger.log_warning("Requested clients file not found - {}. Loading of clients will be skipped".format(filepath))
            return

        for line in file:
            line = line.strip()
            if line == "":
                continue
            client = Client.deserialize(line)
            self.register_client(client)

    def export_clients(self, filepath):
        try:
            file = open(filepath, 'w', encoding = "utf-8")
        except PermissionError:
            Logger.log_error("You don't have permission to export clients to this file - {}".format(filepath))
            return
        if file is None:
            Logger.log_error("Cannot open file to export clients - {}".format(filepath))

        for client in self.clients:
            file.write(client.serialize() + "\n")

    def load_packets(self, filepath):
        self.packets = []
        try:
            file = open(filepath, 'r', encoding = "utf-8")
        except FileNotFoundError:
            Logger.log_warning("Requested packets file not found - {}. Loading of packets will be skipped".format(filepath))
            return

        for line in file:
            line = line.strip()
            if line == "":
                continue
            packet = Packet.deserialize(line)
            self.add_packet(packet)

    def export_packets(self, filepath):
        try:
            file = open(filepath, 'w', encoding = "utf-8")
        except PermissionError:
            Logger.log_error("You don't have permission to export packets to this file - {}".format(filepath))
            return
        if file is None:
            Logger.log_error("Cannot open file to export packets - {}".format(filepath))

        for packet in self.packets:
            file.write(packet.serialize() + "\n")

    def add_packet(self, new_packet, should_update_settings_ui = False):
        for packet in self.packets:
            if packet.name == new_packet.name:
                Logger.log_warning("Trying to add a packet with existing name. It will be skipped")
                return
        self.packets.append(new_packet)

        if should_update_settings_ui:
            if self.settings_window:
                self.settings_window.create_ui(True, self.packets)
            else:
                Logger.log_error("Adding a packet and setting's UI needs to be updated but there is no settings window. It won't be updated")

    def register_client(self, new_client, do_update_reservation_form = False):
        for client in self.clients:
            if client.name == new_client.name and client.egn_cifri == new_client.egn_cifri:
                Logger.log_warning("Trying to register a client that already exists. It will be skipped")
                return
        self.clients.append(new_client)
        if do_update_reservation_form:
            self.reservation_form.update_clients(self.clients)
