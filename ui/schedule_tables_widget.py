from logger import Logger
from handlers.schedule_handler import ScheduleHandler
from ui.table_base import TableBase

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PySide2.QtGui import QFont

class ScheduleTablesWidget(QWidget):
    def __init__(self, date, database):
        super().__init__()
        self.init_constants()

        self.date = date
        self.database = database

        self.employees = self.database.employees
        self.employer = self.database.get_employer()
        self.schedule_handler = ScheduleHandler(self.date, self.HOUR_BEGIN, self.HOUR_END, self.database)

        self.init_vrows()
        self.create_ui()

    def init_constants(self):
        self.FONT = QFont("Verdana", 12)
        self.HOUR_BEGIN = 8
        self.HOUR_END = 20

    def init_vrows(self):
        # Handle timegrid table
        self.vrows_count_timegrid = self.HOUR_END - self.HOUR_BEGIN + 1
        self.vrows_sizes_timegrid = []
        for vrow in range(self.vrows_count_timegrid):
            hour = self.HOUR_BEGIN + vrow
            # Size of virtual row should be the maximum number of reservations for current hour across all employees
            # But if there are no reservations for the current hour then we don't want the size to be 0, we want it to be 1,
            # so let's add 1 to the list before taking the max
            vrow_size = max([1] + [
                len(self.schedule_handler.get_reservations(employee.id, hour)) for employee in self.employees
            ])
            self.vrows_sizes_timegrid.append(vrow_size)
        # Handle employee tables
        self.vrows_count = {}
        self.vrows_sizes = {}
        for employee in self.employees:
            self.vrows_count[employee.id] = 0
            self.vrows_sizes[employee.id] = []
            for hour in range(self.HOUR_BEGIN, self.HOUR_END + 1):
                hour_idx = hour - self.HOUR_BEGIN
                hour_size = self.vrows_sizes_timegrid[hour_idx]
                reservations_count = len(self.schedule_handler.get_reservations(employee.id, hour))
                if reservations_count > hour_size:
                    Logger.log_error("When initializing vrows logic in ScheduleTablesWidget we have reservations_count > hour_size. Logic error.")
                    reservations_count = hour_size
                if reservations_count == 0:
                    self.vrows_sizes[employee.id].append(hour_size)
                else:
                    # Try to divide the hour interval evenly between the reservations
                    fair_vrow_size = hour_size // reservations_count
                    self.vrows_sizes[employee.id] += [fair_vrow_size] * (reservations_count - 1)
                    # Only last reservation might need to be bigger if the numbers don't divide
                    self.vrows_sizes[employee.id].append(hour_size - fair_vrow_size * (reservations_count - 1))
                # Each hour will contribute as many vrows as there are reservations for the employee at that hour, or 1 if there are no reservations
                self.vrows_count[employee.id] += max(1, reservations_count)

    def create_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 10)
        self.layout.setSpacing(5)

        self.create_timegrid_table()
        self.create_tables()
        self.link_table_scrollbars()

    def create_timegrid_table(self):
        # Timegrid map should map from vrow indices to timegrid label strings
        timegrid_map = {}
        for vrow in range(self.vrows_count_timegrid):
            timegrid_map[vrow] = str(vrow + self.HOUR_BEGIN)
        self.timegrid_table = TableBase(
            "", self.vrows_count_timegrid, self.vrows_sizes_timegrid, 1, [""], [QHeaderView.ResizeToContents], timegrid_map,
            [lambda s : s], lambda obj, column : None, lambda obj, column : None, lambda id : None, lambda id, col, s : False
        )
        self.timegrid_table.setFixedWidth(40)
        self.timegrid_table.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout.addWidget(self.timegrid_table)

    def create_tables(self):
        self.tables = {}
        for employee in self.employees:
            if employee.id == self.employer.id:
                qcols_count = 4
                qcols_labels = ["Час", "Клиент", "Процедура", "Каса"]
                qcols_resize_modes = [QHeaderView.ResizeToContents, QHeaderView.Stretch, QHeaderView.Stretch, QHeaderView.ResizeToContents]
                viewer_callbacks = [
                    lambda reservation : reservation.date_time.time().toString("HH:mm"),
                    lambda reservation : self.database.get_client(reservation.client_id).name,
                    lambda reservation : reservation.procedure,
                    lambda reservation : str(reservation.kasa)
                ]
            else:
                qcols_count = 5
                qcols_labels = ["Час", "Клиент", "Процедура", "%", "Каса"]
                qcols_resize_modes = [QHeaderView.ResizeToContents, QHeaderView.Stretch, QHeaderView.Stretch, QHeaderView.ResizeToContents, QHeaderView.ResizeToContents]
                viewer_callbacks = [
                    lambda reservation : reservation.date_time.time().toString("HH:mm"),
                    lambda reservation : self.database.get_client(reservation.client_id).name,
                    lambda reservation : reservation.procedure,
                    lambda reservation : str(reservation.percent),
                    lambda reservation : str(reservation.kasa)
                ]

            self.tables[employee.id] = TableBase(
                employee.name,
                self.vrows_count[employee.id],
                self.vrows_sizes[employee.id],
                qcols_count,
                qcols_labels,
                qcols_resize_modes,
                self.schedule_handler.get_reservations_map(employee.id),
                viewer_callbacks,
                lambda obj, column : obj.bg_colors[column] if (column >= 0 and column < len(obj.bg_colors)) else None,
                lambda obj, column : obj.fg_colors[column] if (column >= 0 and column < len(obj.fg_colors)) else None,
                self.database.delete_reservation,
                lambda id, col, s : False
            )
            if employee.id != self.employees[-1].id:
                self.tables[employee.id].table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.layout.addWidget(self.tables[employee.id])

    def link_table_scrollbars(self):
        tables_list = [self.timegrid_table]
        for employee in self.employees[:3]:
            tables_list.append(self.tables[employee.id])

        scrollbar_0 = tables_list[0].table.verticalScrollBar()
        scrollbar_1 = tables_list[1].table.verticalScrollBar()
        scrollbar_2 = tables_list[2].table.verticalScrollBar()
        scrollbar_3 = tables_list[3].table.verticalScrollBar()

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