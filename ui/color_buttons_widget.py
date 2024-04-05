from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PySide2.QtGui import QColor, QFont

from ui.font_changer_widget import FontGlobal

class ColorButtonsWidget(QWidget):
    def __init__(self, paint_cells_callback):
        super().__init__()

        self.paint_cells_callback = paint_cells_callback

        self.create_ui()

    def create_ui(self, delete_old_layout = False):
        if delete_old_layout:
            # Create a temporary QWidget object and set its layout to be the current old layout.
            # That way, the temporary object is immediately deleted and it deletes the layout and all of its children widgets
            QWidget().setLayout(self.layout)
            # After that we can just create a new layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(10)

        self.bg_label = QLabel("Клетка")
        self.bg_label.setFont(FontGlobal.font)
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
        self.fg_label.setFont(FontGlobal.font)
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
            self.paint_cells_callback(QColor(color[0], color[1], color[2], color[3]), True)
        return pushed

    def fg_pushed_wrapper(self, color):
        def pushed():
            self.paint_cells_callback(QColor(color[0], color[1], color[2], color[3]), False)
        return pushed