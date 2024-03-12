from schedule import Schedule
from PySide6.QtCore import Qt
from PySide6.QtCore import QDate
from PySide6.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont

class ScheduleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.font_size = 14
        self.tables_items_count = {}

        # Example schedule
        self.schedule = Schedule()
        self.schedule.load_example_data()

        self.date = QDate(2024, 4, 9)
        self.employees = self.schedule.get_employees(self.date)

        self.layout = QHBoxLayout(self)
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
                    font-size: """ + str(self.font_size) + """pt;
                }
            """)
            # Change the font of the table
            table.setFont(QFont("Verdana", self.font_size))
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
        for employee, reservations in schedule.data[self.date].items():
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
