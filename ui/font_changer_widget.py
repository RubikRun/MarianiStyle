from logger import Logger

from PySide2.QtCore import Qt, QSize
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PySide2.QtGui import QFont, QIcon

def load_font_size():
    default_font_size = 10
    try:
        file = open("config/font_size.config", 'r')
    except FileNotFoundError:
        Logger.log_error("Config file of font size was not found. Default font size will be used.")
        return default_font_size
    font_size_str = file.read()
    try:
        font_size = int(font_size_str)
    except ValueError:
        Logger.log_error("Config file of font size should contain only a single integer. Default font size will be used.")
        return default_font_size
    if font_size < 4 or font_size > 30:
        Logger.log_error("Config file of font size contains font size out of range. Default font size will be used.")
        return default_font_size
    return font_size

class FontGlobal:
    font_size = load_font_size()
    font = QFont("Verdana", font_size)
    font_header = QFont("Verdana", int(font_size * 1.2))

def export_font_size():
    try:
        file = open("config/font_size.config", 'w', encoding = "utf-8")
    except PermissionError:
        Logger.log_error("You don't have permission to export font size to this config file.")
        return
    if FontGlobal.font_size is None:
        Logger.log_error("Cannot export None font size to config file.")
        return
    file.write(str(FontGlobal.font_size))

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
