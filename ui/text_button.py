from PySide2.QtWidgets import QWidget, QHBoxLayout, QPushButton

from ui.font_changer_widget import FontGlobal

class TextButton(QWidget):
    def __init__(self, label_str, label_font, fixed_width, fixed_height, on_press_callback, widgets_list = None):
        super().__init__()
        self.label_str = label_str
        self.label_font = label_font
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height
        self.on_press_callback = on_press_callback
        self.widgets_list = widgets_list

        self.create_ui()

    def create_ui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.button = QPushButton(self.label_str)
        self.button.setFont(self.label_font)
        self.button.setFixedSize(self.fixed_width, self.fixed_height)
        self.button.clicked.connect(self.on_press_callback)
        self.layout.addWidget(self.button)
        if self.widgets_list is not None:
            self.widgets_list.append(self)

    def update_font_size(self):
        self.button.font().setPixelSize(FontGlobal.font_size)
