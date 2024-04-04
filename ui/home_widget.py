from logger import Logger
from ui.text_button import TextButton
from ui.color_buttons_widget import ColorButtonsWidget
from ui.schedule_tables_widget import ScheduleTablesWidget
from ui.schedule_date_navigator_widget import ScheduleDateNavigatorWidget
from ui.reservation_form import ReservationForm
from ui.clients_window import ClientsWindow


from PySide2.QtCore import Qt, QDate
from PySide2.QtWidgets import QWidget, QGridLayout
from PySide2.QtGui import QFont

class HomeWidget(QWidget):
    def __init__(self, database):
        super().__init__()

        self.database = database
        self.date = QDate(2024, 4, 8)
        self.clients_window = None

        self.init_constants()
        self.create_ui()

    def init_constants(self):
        self.FONT = QFont("Verdana", 12)

    def create_ui(self, delete_old_layout = False):
        if delete_old_layout:
            # Create a temporary QWidget object and set its layout to be the current old layout.
            # That way, the temporary object is immediately deleted and it deletes the layout and all of its children widgets
            QWidget().setLayout(self.layout)
            # After that we can just create a new layout
        self.layout = QGridLayout(self)

        self.schedule_tables_widget = ScheduleTablesWidget(self.date, self.database)
        self.color_buttons_widget = ColorButtonsWidget(self.schedule_tables_widget.color_selected_cells)
        self.clients_button = TextButton("Клиенти", self.FONT, 100, 40, self.clients_button_pressed)
        self.schedule_date_navigator_widget = ScheduleDateNavigatorWidget(self.date, self.do_prev_date, self.do_next_date, self.do_change_date)
        self.reservation_form = ReservationForm(self.date, self.database, self.create_ui, None, None)

        self.layout.addWidget(self.color_buttons_widget, 0, 0, 1, 1)
        self.layout.setAlignment(self.color_buttons_widget, Qt.AlignLeft)
        self.layout.addWidget(self.clients_button, 0, 1, 1, 1)
        self.layout.setAlignment(self.clients_button, Qt.AlignRight)
        self.layout.addWidget(self.schedule_tables_widget, 1, 0, 1, 1)
        self.layout.addWidget(self.schedule_date_navigator_widget, 3, 0, 1, 1)
        self.layout.setAlignment(self.schedule_date_navigator_widget, Qt.AlignCenter)
        self.reservation_form.setFixedWidth(600)
        self.layout.addWidget(self.reservation_form, 4, 0, 1, 1)
        self.layout.setAlignment(self.reservation_form, Qt.AlignLeft)

    def do_next_date(self):
        self.date = self.date.addDays(1)
        self.create_ui(True)

    def do_prev_date(self):
        self.date = self.date.addDays(-1)
        self.create_ui(True)

    def do_change_date(self, date):
        self.date = date
        self.create_ui(True)

    def on_client_register(self):
        self.create_ui(True)

    def clients_button_pressed(self):
        self.clients_window = ClientsWindow(self, self.database, self.on_client_register)
        self.clients_window.show()