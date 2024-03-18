from schedule_widget import ScheduleWidget
from schedule import Schedule
from reservation_form import ReservationForm

from PySide6.QtWidgets import QWidget, QVBoxLayout

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.schedule = Schedule()
        self.schedule.load("database/schedule.data")
        self.employees = self.schedule.get_employees()

        schedule_widget = ScheduleWidget(self.schedule, self.employees)
        reservation_form = ReservationForm(self.employees, schedule_widget.add_reservation, schedule_widget.get_date)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(schedule_widget)
        self.layout.addWidget(reservation_form)
