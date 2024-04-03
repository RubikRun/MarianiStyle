from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PySide2.QtGui import QColor, QFont

class ColorButtonsWidget(QWidget):
    def __init__(self, paint_cells_bg_callback, paint_cells_fg_callback):
        super().__init__()
        self.init_constants()

        self.paint_cells_bg_callback = paint_cells_bg_callback
        self.paint_cells_fg_callback = paint_cells_fg_callback

        self.create_ui()

    def init_constants(self):
        self.FONT = QFont("Verdana", 10)

    def create_ui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(10)

        self.bg_label = QLabel("Клетка")
        self.bg_label.setFont(self.FONT)
        self.bg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.bg_label)

        # TODO: this member should be loaded from a config file
        self.bg_colors = [
            (255, 0, 0, 255),
            (0, 255, 0, 255),
            (0, 0, 255, 255)
        ]
        self.bg_style_sheets = {}
        self.bg_buttons = {}
        for color in self.bg_colors:
            self.bg_style_sheets[color] = "background-color: rgba({}, {}, {}, {});".format(str(color[0]), str(color[1]), str(color[2]), str(color[3]))
            self.bg_buttons[color] = QPushButton()
            self.bg_buttons[color].setFixedSize(24, 24)
            self.bg_buttons[color].setStyleSheet(self.bg_style_sheets[color])
            self.bg_buttons[color].clicked.connect(self.bg_pushed_wrapper(color))
            self.layout.addWidget(self.bg_buttons[color])

        self.fg_label = QLabel("Текст")
        self.fg_label.setFont(self.FONT)
        self.fg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.fg_label)

        # TODO: this member should be loaded from a config file
        self.fg_colors = [
            (255, 0, 0, 255),
            (0, 255, 0, 255),
            (0, 0, 255, 255)
        ]
        self.fg_style_sheets = {}
        self.fg_buttons = {}
        for color in self.fg_colors:
            self.fg_style_sheets[color] = "background-color: rgba({}, {}, {}, {});".format(str(color[0]), str(color[1]), str(color[2]), str(color[3]))
            self.fg_buttons[color] = QPushButton()
            self.fg_buttons[color].setFixedSize(24, 24)
            self.fg_buttons[color].setStyleSheet(self.fg_style_sheets[color])
            self.fg_buttons[color].clicked.connect(self.fg_pushed_wrapper(color))
            self.layout.addWidget(self.fg_buttons[color])

    def bg_pushed_wrapper(self, color):
        def pushed():
            self.paint_cells_bg_callback(QColor(color[0], color[1], color[2], color[3]))
        return pushed

    def fg_pushed_wrapper(self, color):
        def pushed():
            self.paint_cells_fg_callback(QColor(color[0], color[1], color[2], color[3]))
        return pushed