from logger import Logger

from PySide2.QtCore import Qt, QSize
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PySide2.QtGui import QFont, QIcon

from handlers.font_global import FontGlobal, export_font_size

class FontChangerWidget(QWidget):
    def __init__(self, update_font_size_callback):
        super().__init__()
        self.update_font_size_callback = update_font_size_callback

        self.create_ui()

    def create_ui(self):
        self.layout = QHBoxLayout(self)

        self.left_button = QPushButton()
        self.left_button.clicked.connect(self.left_pressed)
        self.left_button.setIcon(QIcon("icons/date_arrow_left.png"))
        self.left_button.setIconSize(QSize(15,15))
        self.left_button.setFixedWidth(30)
        self.layout.addWidget(self.left_button)

        self.register_label = QLabel("Шрифт {}".format(FontGlobal.font_size))
        self.register_label.setFont(QFont("Verdana", FontGlobal.font_size))
        self.layout.addWidget(self.register_label)

        self.right_button = QPushButton()
        self.right_button.clicked.connect(self.right_pressed)
        self.right_button.setIcon(QIcon("icons/date_arrow_right.png"))
        self.right_button.setIconSize(QSize(15,15))
        self.right_button.setFixedWidth(30)
        self.layout.addWidget(self.right_button)

    def update_font_of_label(self):
        self.register_label.setText("Шрифт {}".format(FontGlobal.font_size))
        self.register_label.font().setPixelSize(FontGlobal.font_size)

    @Slot()
    def left_pressed(self):
        FontGlobal.font_size -= 1
        FontGlobal.font = QFont("Verdana", FontGlobal.font_size)
        FontGlobal.font_header = QFont("Verdana", int(FontGlobal.font_size * 1.2))
        export_font_size()
        self.update_font_size_callback()

    @Slot()
    def right_pressed(self):
        FontGlobal.font_size += 1
        FontGlobal.font = QFont("Verdana", FontGlobal.font_size)
        FontGlobal.font_header = QFont("Verdana", int(FontGlobal.font_size * 1.2))
        export_font_size()
        self.update_font_size_callback()
