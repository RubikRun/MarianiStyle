from schedule_widget import ScheduleWidget
from schedule import Schedule
from logger import Logger
from client import Client
from reservation_form import ReservationForm
from registration_form import RegistrationForm

from PySide6.QtWidgets import QWidget, QGridLayout

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.load_clients("database/clients.data")

        self.schedule = Schedule()
        self.schedule.load("database/schedule.data")
        self.employees = self.schedule.get_employees()

        schedule_widget = ScheduleWidget(self.schedule)
        reservation_form = ReservationForm(self.employees, schedule_widget.add_reservation, schedule_widget.get_date)
        registration_form = RegistrationForm(self.register_client)

        self.layout = QGridLayout(self)
        self.layout.addWidget(schedule_widget, 0, 0, 1, 2)
        self.layout.addWidget(reservation_form, 1, 0, 1, 1)
        self.layout.addWidget(registration_form, 1, 1, 1, 1)

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

    def register_client(self, new_client):
        for client in self.clients:
            if client.name == new_client.name and client.egn_cifri == new_client.egn_cifri:
                Logger.log_warning("Trying to register a client that already exists. It will be skipped")
                return
        self.clients.append(new_client)
