from schedule_widget import ScheduleWidget
from schedule import Schedule
from logger import Logger
from reservation_form import ReservationForm
from registration_form import RegistrationForm

from PySide6.QtWidgets import QWidget, QGridLayout

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.load_clients("TODO")

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
        # TODO
        self.clients = []

    def export_clients(self, filepath):
        # TODO
        pass

    def register_client(self, new_client):
        for client in self.clients:
            if client.name == new_client.name and client.egn_cifri == new_client.egn_cifri:
                Logger.log_warning("Trying to register a client that already exists. It will be skipped")
                return
        self.clients.append(new_client)
