from reservation import Reservation
from schedule import Schedule
from PySide6.QtCore import QTime, QDate
from PySide6.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont

class ScheduleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.items_count = 0

        # Example schedule
        self.schedule = Schedule()
        self.schedule.load_example_data()

        # Left
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Клиент", "Час", "Клиент", "Час", "Клиент", "Час"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Set styles for the table
        self.table.setStyleSheet("""
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
        self.table.setFont(QFont("Verdana", 12))

        # QWidget Layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.table)

        # Fill example data
        self.fill_table()

    def fill_table(self, schedule=None):
        schedule = self.schedule if not schedule else schedule
        vertical_header_labels = []
        for hour, reservations in schedule.data[QDate(2024, 4, 9)].items():
            self.table.insertRow(self.items_count)
            for idx_reservation, reservation in enumerate(reservations):
                if reservation is None:
                    continue
                self.table.setItem(self.items_count, idx_reservation * 2 + 0, QTableWidgetItem(reservation.client))
                time_str = reservation.time_begin.toString("HH:mm") + " - " + reservation.time_end.toString("HH:mm")
                self.table.setItem(self.items_count, idx_reservation * 2 + 1, QTableWidgetItem(time_str))
            self.items_count += 1
            vertical_header_labels.append(str(hour))
        self.table.setVerticalHeaderLabels(vertical_header_labels)
