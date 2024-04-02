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
        self.timegrid = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 10)
        self.layout.setSpacing(5)

        self.init_timegrid_rows_counts()
        self.create_table_timegrid()
        self.create_tables()
        self.link_table_scrollbars()
        self.fill_tables()

    # Initializes a list of counts self.timegrid_rows_counts
    # such that self.timegrid_rows_counts[i] is
    # the number of table rows needed for the timegrid row i.
    # Currently this count can be either 1 or 2,
    # depending on whether any employee has more than 1 reservation in this timegrid cell
    def init_timegrid_rows_counts(self):
        # res_count_map[employee][timegrid_idx] will be the number of reservations that employee has for that timegrid index
        res_count_map = {}
        for employee, reservations in self.schedule.items():
            if employee not in res_count_map:
                res_count_map[employee] = [0] * len(self.timegrid)
            for reservation in reservations:
                if reservation.employee != employee:
                    Logger.log_error("Reservation's employee doesn't match the employee that the reservation is put under in the schedule. Ignoring that reservation.")
                    continue
                # Find the timegrid row/index where the reservation should be put based on its begin time
                timegrid_idx = self.find_row_for_time(reservation.time_interval.time_begin)
                res_count_map[employee][timegrid_idx] += 1
            for res_count_idx, res_count in enumerate(res_count_map[employee]):
                if res_count == 0:
                    res_count_map[employee][res_count_idx] = 1

        self.timegrid_rows_counts = []
        for timegrid_idx, timepoint in enumerate(self.timegrid):
            max_res_count = 0
            for employee, res_count in res_count_map.items():
                if res_count[timegrid_idx] > max_res_count:
                    max_res_count = res_count[timegrid_idx]
            self.timegrid_rows_counts.append(max_res_count)

        self.rows_count = sum(self.timegrid_rows_counts)

    def get_first_table_row_from_timegrid_row(self, req_timegrid_row):
        table_row = 0
        for timegrid_row in range(req_timegrid_row):
            table_row += self.timegrid_rows_counts[timegrid_row]
        return table_row

    def create_table_timegrid(self):
        self.table_timegrid = QTableWidget(self.rows_count, 1)
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

        rows_filled = 0
        for timegrid_idx, timepoint in enumerate(self.timegrid):
            time_interval_str = QTime(timepoint, 0).toString("HH")
            for sub_row_idx in range(self.timegrid_rows_counts[timegrid_idx]):
                self.table_timegrid.insertRow(rows_filled + sub_row_idx)
            if self.timegrid_rows_counts[timegrid_idx] >= 2:
                self.table_timegrid.setSpan(rows_filled, 0, self.timegrid_rows_counts[timegrid_idx], 1)
            self.table_timegrid.setItem(rows_filled, 0, QTableWidgetItem(time_interval_str))
            rows_filled += self.timegrid_rows_counts[timegrid_idx]
        if rows_filled != self.rows_count:
            Logger.log_error("Rows filled is different than expected rows count. Something wrong with dynamic timegrid rows count.")
        self.table_timegrid.setRowCount(rows_filled)

    def create_tables(self):
        # Create tables
        self.tables = {}
        # Traverse employees
        for employee in [self.employer] + self.employees:
            # Create a table for each employee
            if employee == self.employer:
                table = QTableWidget(self.rows_count, 4)
            else:
                table = QTableWidget(self.rows_count, 5)
            if employee != self.employees[-1]:
                table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # Handle properties of rows and columns and their headers
            if employee == self.employer:
                table.setHorizontalHeaderLabels(["Час", "Клиент", "Процедура", "Каса"])
                table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
                table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
                table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
                table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
            else:
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
        timegrid_cells_filled_map = {}
        # Traverse employees and their reservations for current date
        for employee, reservations in self.schedule.items():
            table = self.tables[employee]
            tab_idx = [0, 1, 2, 3, 4]
            if employee == self.employer:
                tab_idx = [0, 1, 2, -1, 3]

            timegrid_cells_filled_map[employee] = [0] * len(self.timegrid)
            timegrid_cells_filled = timegrid_cells_filled_map[employee]
            # Traverse current employee's reservations
            for reservation in reservations:
                if reservation.employee != employee:
                    Logger.log_error("Reservation's employee doesn't match the employee that the reservation is put under in the schedule. Ignoring that reservation.")
                    continue
                # Find the timegrid row where the reservation should be put based on its begin time
                timegrid_row = self.find_row_for_time(reservation.time_interval.time_begin)
                row = self.get_first_table_row_from_timegrid_row(timegrid_row) + timegrid_cells_filled[timegrid_row]
                timegrid_cells_filled[timegrid_row] += 1
                if timegrid_cells_filled[timegrid_row] > self.timegrid_rows_counts[timegrid_row]:
                    Logger.log_error("Filled more table rows inside a single timegrid row than expected. Something wrong with dynamic timegrid rows count.")
                # Handle time interval
                if tab_idx[0] >= 0:
                    time_str = reservation.time_interval.time_begin.toString("HH:mm")
                    table.setItem(row, tab_idx[0], QTableWidgetItem(time_str))
                # Handle client
                if tab_idx[1] >= 0:
                    client_widget_item = QTableWidgetItem(reservation.client.name)
                    client_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, tab_idx[1], client_widget_item)
                # Handle procedure
                if tab_idx[2] >= 0:
                    procedure_widget_item = QTableWidgetItem(reservation.procedure)
                    procedure_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, tab_idx[2], procedure_widget_item)
                # Handle percent
                if tab_idx[3] >= 0:
                    percent_widget_item = QTableWidgetItem(str(reservation.percent))
                    percent_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, tab_idx[3], percent_widget_item)
                # Handle kasa
                if tab_idx[4] >= 0:
                    kasa_widget_item = QTableWidgetItem(str(reservation.kasa))
                    kasa_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, tab_idx[4], kasa_widget_item)
                # Handle color
                for idx, color in enumerate(reservation.colors):
                    if color is None:
                        continue
                    col = idx % 4
                    bg_fg = (idx < 4)
                    item = table.item(row, col)
                    if item:
                        if bg_fg:
                            item.setBackground(color)
                        else:
                            item.setForeground(color)
                    else:
                        Logger.log_error("Trying to paint a cell from ScheduleTablesWidget with the color from database but item doesn't exist")

            for employee, table in self.tables.items():
                if employee not in timegrid_cells_filled_map:
                    # TODO: handle this case. What do we do if employee didn't have reservations at all for this day?
                    # We still need to make their rows with a bigger span so that there is 1 row per 1 timegrid row
                    continue
                for timegrid_row in range(len(self.timegrid)):
                    timegrid_cells_filled = timegrid_cells_filled_map[employee]
                    if timegrid_cells_filled[timegrid_row] < self.timegrid_rows_counts[timegrid_row]:
                        last_row = self.get_first_table_row_from_timegrid_row(timegrid_row) + timegrid_cells_filled[timegrid_row] - 1
                        if last_row < self.get_first_table_row_from_timegrid_row(timegrid_row):
                            last_row = self.get_first_table_row_from_timegrid_row(timegrid_row)
                        span = self.timegrid_rows_counts[timegrid_row] - timegrid_cells_filled[timegrid_row] + 1
                        if span > self.timegrid_rows_counts[timegrid_row]:
                            span = self.timegrid_rows_counts[timegrid_row]
                        if span >= 2:
                            cols_count = 5
                            if employee == self.employer:
                                cols_count = 4
                            for col in range(cols_count):
                                table.setSpan(last_row, col, span, 1)


    def find_row_for_time(self, time):
        if QTime(self.timegrid[0], 0) > time:
            Logger.log_error("Cannot find a cell in time grid for a reservation's time. Putting it in first row.")
            return 0
        if QTime(self.timegrid[-1] + 1, 0) <= time:
            Logger.log_error("Cannot find a cell in time grid for a reservation's time. Putting it in last row.")
            return len(self.timegrid) - 1

        row = 0
        while row + 1 < len(self.timegrid) and QTime(self.timegrid[row + 1], 0) <= time:
            row += 1
        return row

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
