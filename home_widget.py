from schedule_widget import ScheduleWidget
from schedule import Schedule
from reservation_form import ReservationForm

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QWidget, QVBoxLayout

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.schedule = Schedule()
        self.schedule.load_example_data()
        self.date = QDate(2024, 4, 9)
        self.employees = self.schedule.get_employees(self.date)

        schedule_widget = ScheduleWidget(self.schedule, self.date, self.employees)
        reservation_form = ReservationForm(self.employees, schedule_widget.add_reservation, schedule_widget.get_date)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(schedule_widget)
        self.layout.addWidget(reservation_form)
