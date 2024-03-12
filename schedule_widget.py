from schedule import Schedule
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
        for employee in self.employees:
            table = QTableWidget()
            table.setColumnCount(1)
            table.setHorizontalHeaderLabels(["Клиент"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            # Set styles for the table
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

            # add table to layout
            self.layout.addWidget(table)
            self.tables[employee] = table
            self.tables_items_count[employee] = 0

        # Fill example data
        self.fill_tables()

    def fill_tables(self, schedule=None):
        schedule = self.schedule if not schedule else schedule
        for employee, reservations in schedule.data[self.date].items():
            table = self.tables[employee]
            vertical_header_labels = []
            for time_interval, client in reservations.items():
                table.insertRow(self.tables_items_count[employee])
                table.setItem(self.tables_items_count[employee], 0, QTableWidgetItem(client))
                time_str = time_interval.time_begin.toString("HH:mm") + " - " + time_interval.time_end.toString("HH:mm")
                vertical_header_labels.append(time_str)
                self.tables_items_count[employee] += 1
            table.setVerticalHeaderLabels(vertical_header_labels)
