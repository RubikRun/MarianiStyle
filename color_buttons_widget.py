from PySide2.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide2.QtGui import QColor

class ColorButtonsWidget(QWidget):
    def __init__(self, paint_cells_callback):
        super().__init__()
        self.paint_cells_callback = paint_cells_callback

        self.create_ui()

    def create_ui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(10)

        # TODO: these 2 members should be loaded from a config file
        self.color_names = ["red", "green", "blue"]
        self.colors = {
            "red": QColor(255, 0, 0, 255),
            "green": QColor(0, 255, 0, 255),
            "blue": QColor(0, 0, 255, 255)
        }
        self.style_sheets = {}
        self.buttons = {}
        for color_name in self.color_names:
            color = self.colors[color_name]
            self.style_sheets[color_name] = "background-color: rgba({}, {}, {}, {});".format(str(color.red()), str(color.green()), str(color.blue()), str(color.alpha()))
            self.buttons[color_name] = QPushButton()
            self.buttons[color_name].setFixedSize(25, 25)
            self.buttons[color_name].setStyleSheet(self.style_sheets[color_name])
            self.buttons[color_name].clicked.connect(self.pushed_wrapper(color_name))
            self.layout.addWidget(self.buttons[color_name])

    def pushed_wrapper(self, color_name):
        def pushed():
            self.paint_cells_callback(self.colors[color_name])
        return pushed