from schedule import Schedule
from PySide6.QtCore import QDate
from PySide6.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont

class ScheduleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.items_count = 0

        # Example schedule
        self.schedule = Schedule()
        self.schedule.load_example_data()

        self.date = QDate(2024, 4, 9)
        self.employees_count = self.schedule.get_employees_count(self.date)

        self.layout = QHBoxLayout(self)
        # Create tables
        self.tables = []
        for i in range(self.employees_count):
            table = QTableWidget()
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Клиент", "Час"])
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
                }
            """)
            # Change the font of the table
            table.setFont(QFont("Verdana", 12))
            # add table to layout
            self.layout.addWidget(table)
            self.tables.append(table)

        # Fill example data
        self.fill_tables()

    def fill_tables(self, schedule=None):
        schedule = self.schedule if not schedule else schedule
        vertical_header_labels = []
        for hour, reservations in schedule.data[self.date].items():
            for idx_table, table in enumerate(self.tables):
                table.insertRow(self.items_count)
                reservation = reservations[idx_table]
                if reservation is None:
                    continue
                table.setItem(self.items_count, 0, QTableWidgetItem(reservation.client))
                time_str = reservation.time_begin.toString("HH:mm") + " - " + reservation.time_end.toString("HH:mm")
                table.setItem(self.items_count, 1, QTableWidgetItem(time_str))
            self.items_count += 1
            vertical_header_labels.append(str(hour))
        self.tables[0].setVerticalHeaderLabels(vertical_header_labels)
