from ui.calendar_window import CalendarWindow

from PySide2.QtCore import Qt, QSize
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide2.QtGui import QFont, QIcon

from ui.font_changer_widget import FontGlobal

class ScheduleDateNavigatorWidget(QWidget):
    def __init__(self, date, left_callback, right_callback, date_changed_callback):
        super().__init__()
        self.date = date
        self.left_callback = left_callback
        self.right_callback = right_callback
        self.date_changed_callback = date_changed_callback
        self.calendar_window = None

        self.create_ui()

    def create_ui(self, delete_old_layout = False):
        if delete_old_layout:
            # Create a temporary QWidget object and set its layout to be the current old layout.
            # That way, the temporary object is immediately deleted and it deletes the layout and all of its children widgets
            QWidget().setLayout(self.layout)
            # After that we can just create a new layout
        self.layout = QHBoxLayout(self)

        self.left_button = QPushButton()
        self.left_button.clicked.connect(self.left_pressed)
        self.left_button.setIcon(QIcon("icons/date_arrow_left.png"))
        self.left_button.setIconSize(QSize(40,40))
        self.left_button.setFixedWidth(100)
        self.layout.addWidget(self.left_button)

        self.date_button = QPushButton(self.date.toString("dd.MM.yyyy"))
        self.date_button.setFont(FontGlobal.font)
        self.date_button.clicked.connect(self.date_pressed)
        self.date_button.setFixedWidth(100)
        self.date_button.setFixedHeight(40)
        self.layout.addWidget(self.date_button)

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

    @Slot()
    def date_pressed(self):
        self.calendar_window = CalendarWindow(self.date_changed_callback)
        self.calendar_window.show()
