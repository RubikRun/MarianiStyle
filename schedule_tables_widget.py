# This Python file uses the following encoding: utf-8
from logger import Logger
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PySide2.QtGui import QFont

schedule_font = QFont("Verdana", 12)

class ScheduleTablesWidget(QWidget):
    def __init__(self, schedule, employees):
        super().__init__()
        self.schedule = schedule
        self.employees = employees

        self.tables_items_count = {}

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 10)
        self.layout.setSpacing(20)

        self.create_tables()
        self.fill_tables()

    def create_tables(self):
        # Create tables
        self.tables = {}
        # Traverse employees
        for employee in self.employees:
            # Create a table for each employee
            table = QTableWidget()
            # Handle properties of rows and columns and their headers
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["Час", "Клиент", "Процедура", "%", "Каса"])
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
            table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
            table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
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

    def fill_tables(self):
        # Traverse employees and their reservations for current date
        for employee, reservations in self.schedule.items():
            table = self.tables[employee]
            # Traverse current employee's reservations
            for reservation in reservations:
                if reservation.employee != employee:
                    Logger.log_error("Reservation's employee doesn't match the employee that the reservation is put under in the schedule. Ignoring that reservation.")
                    continue
                table.insertRow(self.tables_items_count[employee])
                # Handle time interval
                time_str = reservation.time_interval.time_begin.toString("HH:mm") + "-" + reservation.time_interval.time_end.toString("HH:mm")
                table.setItem(self.tables_items_count[employee], 0, QTableWidgetItem(time_str))
                # Handle client
                client_widget_item = QTableWidgetItem(reservation.client.name)
                client_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(self.tables_items_count[employee], 1, client_widget_item)
                # Handle procedure
                procedure_widget_item = QTableWidgetItem(reservation.procedure)
                procedure_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(self.tables_items_count[employee], 2, procedure_widget_item)
                # Handle percent
                percent_widget_item = QTableWidgetItem(str(reservation.percent))
                percent_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(self.tables_items_count[employee], 3, percent_widget_item)
                # Handle kasa
                kasa_widget_item = QTableWidgetItem(str(reservation.kasa))
                kasa_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(self.tables_items_count[employee], 4, kasa_widget_item)
                # Handle color
                if reservation.color is not None:
                    for col in range(table.columnCount()):
                        item = table.item(self.tables_items_count[employee], col)
                        if item:
                            item.setBackground(reservation.color)
                        else:
                            Logger.log_error("Trying to paint a row from ScheduleTablesWidget with the color from database but item doesn't exist")
                self.tables_items_count[employee] += 1
            table.setRowCount(self.tables_items_count[employee])

    def paint_cells(self, color):
        for employee, reservations in self.schedule.items():
            table = self.tables[employee]
            selected_items = table.selectedItems()
            if selected_items:
                for selected_item in selected_items:
                    row = selected_item.row()
                    reservations[row].color = color
                    for col in range(table.columnCount()):
                        item = table.item(row, col)
                        if item:
                            item.setBackground(color)
                        else:
                            Logger.log_error("Trying to paint a row from ScheduleTablesWidget with the color from clicked color button but item doesn't exist")
            table.clearSelection()

class ScheduleEmployeesWidget(QWidget):
    def __init__(self, employees):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.layout.setSpacing(20)
        for employee in employees:
            label = QLabel(employee)
            label.setFont(schedule_font)
            # Uncomment to make border visible
            #label.setStyleSheet("border: 2px solid black; padding: 5px;")
            self.layout.addWidget(label)
