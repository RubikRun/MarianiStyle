from schedule_tables_widget import ScheduleTablesWidget, ScheduleEmployeesWidget
from schedule_date_buttons_widget import ScheduleDateButtonsWidget

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QFont

schedule_font = QFont("Verdana", 12)

class ScheduleWidget(QWidget):
    def __init__(self, schedule, date, employees):
        super().__init__()
        self.schedule = schedule
        self.date = date
        self.employees = employees

        self.create_ui()

    def create_ui(self, deleteOldLayout = False):
        self.employees_widget = ScheduleEmployeesWidget(self.employees)
        self.tables_widget = ScheduleTablesWidget(self.schedule.data[self.date], self.employees)
        self.date_buttons_widget = ScheduleDateButtonsWidget(self.date, self.do_prev_date, self.do_next_date)

        if deleteOldLayout:
            # Create a temporary QWidget object and set its layout to be the current old layout.
            # That way, the temporary object is immediately deleted and it deletes the layout and all of its children widgets
            QWidget().setLayout(self.layout)
            # After that we can just create a new layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.employees_widget)
        self.layout.addWidget(self.tables_widget)
        self.layout.addWidget(self.date_buttons_widget)

    def do_next_date(self):
        self.date = self.date.addDays(1)
        self.create_ui(True)

    def do_prev_date(self):
        self.date = self.date.addDays(-1)
        self.create_ui(True)
