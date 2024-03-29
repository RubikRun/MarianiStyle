# This Python file uses the following encoding: utf-8
from logger import Logger
from PySide2.QtCore import Qt, QTime
from PySide2.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PySide2.QtGui import QFont

schedule_font = QFont("Verdana", 12)

class ScheduleTablesWidget(QWidget):
    def __init__(self, schedule, employees, employer):
        super().__init__()
        self.schedule = schedule
        self.employees = employees
        self.employer = employer
        self.timegrid = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 10)
        self.layout.setSpacing(5)

        self.create_table_timegrid()
        self.create_tables()
        self.link_table_scrollbars()
        #self.fill_tables()

    def create_table_timegrid(self):
        self.table_timegrid = QTableWidget((len(self.timegrid) - 1) * 2, 1)
        self.table_timegrid.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_timegrid.setHorizontalHeaderLabels([""])
        self.table_timegrid.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_timegrid.setFixedWidth(30)
        self.table_timegrid.verticalHeader().hide()
        # Set style sheet for the table
        self.table_timegrid.setStyleSheet("""
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
        self.table_timegrid.setFont(schedule_font)
        # Add table to layout
        self.layout.addWidget(self.table_timegrid)

        rows_count = 0
        for idx, timepoint in enumerate(self.timegrid[:-1]):
            next_timepoint = self.timegrid[idx + 1]
            time_interval_str = QTime(timepoint, 0).toString("HH")# + "-" + QTime(next_timepoint, 0).toString("HH")
            self.table_timegrid.insertRow(rows_count)
            self.table_timegrid.setItem(rows_count, 0, QTableWidgetItem(time_interval_str))
            self.table_timegrid.insertRow(rows_count + 1)
            self.table_timegrid.setSpan(rows_count, 0, 2, 1)
            rows_count += 2
        self.table_timegrid.setRowCount(rows_count)

    def create_tables(self):
        # Create tables
        self.tables = {}
        # Traverse employees
        for employee in [self.employer] + self.employees:
            # Create a table for each employee
            table = QTableWidget(26, 4)
            if employee != self.employees[-1]:
                table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # Handle properties of rows and columns and their headers
            table.setColumnCount(4)
            if employee == self.employer:
                table.setHorizontalHeaderLabels(["Час", "Клиент", "Процедура", "Каса"])
                table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
                table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
                table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
                table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
            else:
                table.setHorizontalHeaderLabels(["Клиент", "Процедура", "%", "Каса"])
                table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
                table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
                table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
                table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
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

    def link_table_scrollbars(self):
        tables_list = [self.table_timegrid]
        for employee in [self.employer] + self.employees:
            tables_list.append(self.tables[employee])

        scrollbar_0 = tables_list[0].verticalScrollBar()
        scrollbar_1 = tables_list[1].verticalScrollBar()
        scrollbar_2 = tables_list[2].verticalScrollBar()
        scrollbar_3 = tables_list[3].verticalScrollBar()

        scrollbar_0.valueChanged.connect(lambda value: scrollbar_1.setValue(value))
        scrollbar_0.valueChanged.connect(lambda value: scrollbar_2.setValue(value))
        scrollbar_0.valueChanged.connect(lambda value: scrollbar_3.setValue(value))
        scrollbar_1.valueChanged.connect(lambda value: scrollbar_0.setValue(value))
        scrollbar_1.valueChanged.connect(lambda value: scrollbar_2.setValue(value))
        scrollbar_1.valueChanged.connect(lambda value: scrollbar_3.setValue(value))
        scrollbar_2.valueChanged.connect(lambda value: scrollbar_0.setValue(value))
        scrollbar_2.valueChanged.connect(lambda value: scrollbar_1.setValue(value))
        scrollbar_2.valueChanged.connect(lambda value: scrollbar_3.setValue(value))
        scrollbar_3.valueChanged.connect(lambda value: scrollbar_0.setValue(value))
        scrollbar_3.valueChanged.connect(lambda value: scrollbar_1.setValue(value))
        scrollbar_3.valueChanged.connect(lambda value: scrollbar_2.setValue(value))

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
                tab_idx = [-1, 0, 1, 2, 3]
                if employee == self.employer:
                    tab_idx = [0, 1, 2, -1, 3]
                # Handle time interval
                if tab_idx[0] >= 0:
                    time_str = reservation.time_interval.time_begin.toString("HH:mm") + "-" + reservation.time_interval.time_end.toString("HH:mm")
                    table.setItem(self.tables_items_count[employee], tab_idx[0], QTableWidgetItem(time_str))
                # Handle client
                if tab_idx[1] >= 0:
                    client_widget_item = QTableWidgetItem(reservation.client.name)
                    client_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(self.tables_items_count[employee], tab_idx[1], client_widget_item)
                # Handle procedure
                if tab_idx[2] >= 0:
                    procedure_widget_item = QTableWidgetItem(reservation.procedure)
                    procedure_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(self.tables_items_count[employee], tab_idx[2], procedure_widget_item)
                # Handle percent
                if tab_idx[3] >= 0:
                    percent_widget_item = QTableWidgetItem(str(reservation.percent))
                    percent_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(self.tables_items_count[employee], tab_idx[3], percent_widget_item)
                # Handle kasa
                if tab_idx[4] >= 0:
                    kasa_widget_item = QTableWidgetItem(str(reservation.kasa))
                    kasa_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(self.tables_items_count[employee], tab_idx[4], kasa_widget_item)
                # Handle color
                for idx, color in enumerate(reservation.colors):
                    if color is None:
                        continue
                    col = idx % 4
                    bg_fg = (idx < 4)
                    item = table.item(self.tables_items_count[employee], col)
                    if item:
                        if bg_fg:
                            item.setBackground(color)
                        else:
                            item.setForeground(color)
                    else:
                        Logger.log_error("Trying to paint a cell from ScheduleTablesWidget with the color from database but item doesn't exist")
                self.tables_items_count[employee] += 1
            table.setRowCount(self.tables_items_count[employee])

    def paint_cells(self, color, bg_fg):
        for employee, reservations in self.schedule.items():
            table = self.tables[employee]
            selected_items = table.selectedItems()
            if selected_items:
                for item in selected_items:
                    row = item.row()
                    col = item.column()
                    if bg_fg:
                        reservations[row].colors[col] = color
                    else:
                        reservations[row].colors[col + 4] = color
                    item = table.item(row, col)
                    if item:
                        if bg_fg:
                            item.setBackground(color)
                        else:
                            item.setForeground(color)
                    else:
                        Logger.log_error("Trying to paint a cell from ScheduleTablesWidget with the color from clicked color button but item doesn't exist")
            table.clearSelection()

class ScheduleEmployeesWidget(QWidget):
    def __init__(self, employees, employer):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(15 + 30, 0, 10, 0)
        self.layout.setSpacing(10)
        for employee in [employer] + employees:
            label = QLabel(employee)
            label.setFont(schedule_font)
            # Uncomment to make border visible
            #label.setStyleSheet("border: 2px solid black; padding: 5px;")
            self.layout.addWidget(label)
