from logger import Logger
from ui.color_buttons_widget import ColorButtonsWidget

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QGridLayout

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.create_ui()

    def create_ui(self):
        self.layout = QGridLayout(self)

        # TODO: Connect the correct 2 functions here
        self.color_buttons_widget = ColorButtonsWidget(None, None)
        self.layout.addWidget(self.color_buttons_widget, 0, 0, 1, 1)
        self.layout.setAlignment(self.color_buttons_widget, Qt.AlignLeft)
