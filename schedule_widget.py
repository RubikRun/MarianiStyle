from schedule import Schedule
from PySide6.QtCore import Qt
from PySide6.QtCore import QDate
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PySide6.QtGui import QFont

schedule_font = QFont("Verdana", 14)

class ScheduleTablesWidget(QWidget):
    def __init__(self, schedule, employees):
        super().__init__()
        self.schedule = schedule
        self.employees = employees

        self.font_size = 14
        self.tables_items_count = {}

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 10)
        self.layout.setSpacing(20)
        # Create tables
        self.tables = {}
        # Traverse employees
        for employee in self.employees:
            # Create a table for each employee
            table = QTableWidget()
            # Handle properties of rows and columns and their headers
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Час", "Клиент"])
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            table.verticalHeader().hide()
            # Set style sheet for the table
            table.setStyleSheet("""
                QTableWidget {
                    background-color: #f0f0f0;
                    alternate-background-color: #e0e0e0;
                    selection-background-color: #a0a0a0;
                }
                QHeaderView::section {
                    background-color: #606060;
                    color: white;
                    font-size: """ + str(schedule_font.pointSize()) + """pt;
                }
            """)
            # Change the font of the table
            table.setFont(schedule_font)
            # Add table to layout
            self.layout.addWidget(table)
            # Add table to tables member
            self.tables[employee] = table
            self.tables_items_count[employee] = 0

        # Fill tables with data
        self.fill_tables()

    def fill_tables(self, schedule=None):
        schedule = self.schedule if not schedule else schedule
        # Traverse employees and their reservations for current date
        for employee, reservations in schedule.items():
            table = self.tables[employee]
            # Traverse current employee's reservations
            for time_interval, client in reservations.items():
                table.insertRow(self.tables_items_count[employee])
                time_str = time_interval.time_begin.toString("HH:mm") + " - " + time_interval.time_end.toString("HH:mm")
                table.setItem(self.tables_items_count[employee], 0, QTableWidgetItem(time_str))
                client_widget_item = QTableWidgetItem(client)
                client_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(self.tables_items_count[employee], 1, client_widget_item)
                self.tables_items_count[employee] += 1
            table.setRowCount(self.tables_items_count[employee])

class ScheduleEmployeesWidget(QWidget):
    def __init__(self, employees):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 0)
        self.layout.setSpacing(20)
        for employee in employees:
            label = QLabel(employee)
            label.setFont(schedule_font)
            # Uncomment to make border visible
            #label.setStyleSheet("border: 2px solid black; padding: 5px;")
            self.layout.addWidget(label)

class ScheduleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.schedule = Schedule()
        self.schedule.load_example_data()

        self.date = QDate(2024, 4, 9)
        self.employees = self.schedule.get_employees(self.date)

        self.employees_widget = ScheduleEmployeesWidget(self.employees)
        self.tables_widget = ScheduleTablesWidget(self.schedule.data[self.date], self.employees)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.employees_widget)
        self.layout.addWidget(self.tables_widget)

