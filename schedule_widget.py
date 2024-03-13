from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QPushButton
from PySide6.QtGui import QFont, QIcon

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

class ScheduleDateButtonsWidget(QWidget):
    def __init__(self, left_callback, right_callback):
        super().__init__()
        self.left_callback = left_callback
        self.right_callback = right_callback

        self.layout = QHBoxLayout(self)

        self.left_button = QPushButton()
        self.left_button.clicked.connect(self.left_pressed)
        self.left_button.setIcon(QIcon("icons/date_arrow_left.png"))
        self.left_button.setIconSize(QSize(40,40))
        self.left_button.setFixedWidth(100)
        self.layout.addWidget(self.left_button)

        self.right_button = QPushButton()
        self.right_button.clicked.connect(self.right_pressed)
        self.right_button.setIcon(QIcon("icons/date_arrow_right.png"))
        self.right_button.setIconSize(QSize(40,40))
        self.right_button.setFixedWidth(100)
        self.layout.addWidget(self.right_button)

    @Slot()
    def left_pressed(self):
        self.left_callback()

    @Slot()
    def right_pressed(self):
        self.right_callback()

class ScheduleWidget(QWidget):
    def __init__(self, schedule, date):
        super().__init__()
        self.schedule = schedule
        self.date = date

        self.create_ui()

    def create_ui(self, deleteOldLayout = False):
        self.employees = self.schedule.get_employees(self.date)

        self.employees_widget = ScheduleEmployeesWidget(self.employees)
        self.tables_widget = ScheduleTablesWidget(self.schedule.data[self.date], self.employees)
        self.date_buttons_widget = ScheduleDateButtonsWidget(self.do_prev_date, self.do_next_date)

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
