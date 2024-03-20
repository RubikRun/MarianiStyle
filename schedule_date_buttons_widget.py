from PySide2.QtCore import Qt, QSize
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide2.QtGui import QFont, QIcon

schedule_font = QFont("Verdana", 12)

class ScheduleDateButtonsWidget(QWidget):
    def __init__(self, date, left_callback, right_callback):
        super().__init__()
        self.date = date
        self.left_callback = left_callback
        self.right_callback = right_callback

        self.layout = QHBoxLayout(self)

        self.layout.setContentsMargins(500, 0, 500, 0)
        self.layout.setSpacing(0)

        self.left_button = QPushButton()
        self.left_button.clicked.connect(self.left_pressed)
        self.left_button.setIcon(QIcon("icons/date_arrow_left.png"))
        self.left_button.setIconSize(QSize(40,40))
        self.left_button.setFixedWidth(100)
        self.layout.addWidget(self.left_button)

        self.date_label = QLabel(self.date.toString("dd.MM.yyyy"))
        self.date_label.setFont(schedule_font)
        self.date_label.setFixedWidth(schedule_font.pointSize() * 10)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.date_label)

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
