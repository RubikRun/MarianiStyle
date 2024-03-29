from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PySide2.QtGui import QColor, QFont

smaller_font = QFont("Verdana", 10)

class ColorButtonsWidget(QWidget):
    def __init__(self, paint_cells_bg_callback, paint_cells_fg_callback):
        super().__init__()
        self.paint_cells_bg_callback = paint_cells_bg_callback
        self.paint_cells_fg_callback = paint_cells_fg_callback

        self.create_ui()

    def create_ui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(10)

        self.bg_label = QLabel("Клетка")
        self.bg_label.setFont(smaller_font)
        self.bg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.bg_label)

        # TODO: these 2 members should be loaded from a config file
        self.bg_color_names = ["red", "green", "blue"]
        self.bg_colors = {
            "red": QColor(255, 0, 0, 255),
            "green": QColor(0, 255, 0, 255),
            "blue": QColor(0, 0, 255, 255)
        }
        self.bg_style_sheets = {}
        self.bg_buttons = {}
        for color_name in self.bg_color_names:
            color = self.bg_colors[color_name]
            self.bg_style_sheets[color_name] = "background-color: rgba({}, {}, {}, {});".format(str(color.red()), str(color.green()), str(color.blue()), str(color.alpha()))
            self.bg_buttons[color_name] = QPushButton()
            self.bg_buttons[color_name].setFixedSize(24, 24)
            self.bg_buttons[color_name].setStyleSheet(self.bg_style_sheets[color_name])
            self.bg_buttons[color_name].clicked.connect(self.bg_pushed_wrapper(color_name))
            self.layout.addWidget(self.bg_buttons[color_name])

        self.fg_label = QLabel("Текст")
        self.fg_label.setFont(smaller_font)
        self.fg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.fg_label)

        # TODO: these 2 members should be loaded from a config file
        self.fg_color_names = ["red", "green", "blue"]
        self.fg_colors = {
            "red": QColor(255, 0, 0, 255),
            "green": QColor(0, 255, 0, 255),
            "blue": QColor(0, 0, 255, 255)
        }
        self.fg_style_sheets = {}
        self.fg_buttons = {}
        for color_name in self.fg_color_names:
            color = self.fg_colors[color_name]
            self.fg_style_sheets[color_name] = "background-color: rgba({}, {}, {}, {});".format(str(color.red()), str(color.green()), str(color.blue()), str(color.alpha()))
            self.fg_buttons[color_name] = QPushButton()
            self.fg_buttons[color_name].setFixedSize(24, 24)
            self.fg_buttons[color_name].setStyleSheet(self.fg_style_sheets[color_name])
            self.fg_buttons[color_name].clicked.connect(self.fg_pushed_wrapper(color_name))
            self.layout.addWidget(self.fg_buttons[color_name])

    def bg_pushed_wrapper(self, color_name):
        def pushed():
            self.paint_cells_bg_callback(self.bg_colors[color_name])
        return pushed

    def fg_pushed_wrapper(self, color_name):
        def pushed():
            self.paint_cells_fg_callback(self.fg_colors[color_name])
        return pushed