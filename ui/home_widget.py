from logger import Logger
from ui.color_buttons_widget import ColorButtonsWidget
from ui.schedule_tables_widget import ScheduleTablesWidget

from PySide2.QtCore import Qt, QDate
from PySide2.QtWidgets import QWidget, QGridLayout

class HomeWidget(QWidget):
    def __init__(self, database):
        super().__init__()

        self.database = database

        self.create_ui()

    def create_ui(self):
        self.layout = QGridLayout(self)

        # TODO: Connect the correct 2 functions here
        self.color_buttons_widget = ColorButtonsWidget(None, None)
        self.layout.addWidget(self.color_buttons_widget, 0, 0, 1, 1)
        self.layout.setAlignment(self.color_buttons_widget, Qt.AlignLeft)

        self.schedule_tables_widget = ScheduleTablesWidget(QDate(2024, 4, 8), self.database)
        self.layout.addWidget(self.schedule_tables_widget, 1, 0, 1, 1)
        self.layout.setAlignment(self.color_buttons_widget, Qt.AlignLeft)
