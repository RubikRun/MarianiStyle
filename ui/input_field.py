from logger import Logger

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QCompleter, QComboBox

class InputField(QWidget):
    def __init__(self, label_str, label_font, widgets_list = None, completer_strings = None, on_text_change_callback = None):
        super().__init__()
        self.label_str = label_str
        self.label_font = label_font
        self.widgets_list = widgets_list
        self.completer_strings = completer_strings
        self.on_text_change_callback = on_text_change_callback

        self.create_ui()

    def create_ui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self.label_str)
        self.label.setFont(self.label_font)
        self.line_edit = QLineEdit(self)
        self.line_edit.setFont(self.label_font)
        if self.completer_strings is not None:
            self.completer = QCompleter(self.completer_strings, self)
            self.completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.line_edit.setCompleter(self.completer)
        if self.on_text_change_callback is not None:
            self.line_edit.textChanged.connect(self.on_text_change_callback)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)
        if self.widgets_list is not None:
            self.widgets_list.append(self)

    def get_text(self):
        return self.line_edit.text().strip()

    def get_int(self):
        try:
            value = int(self.get_text())
            return value
        except ValueError:
            Logger.log_error("Trying to get_int() from InputField but the input text is not an integer. Will use -1.")
            return -1

    def get_float(self):
        try:
            value = float(self.get_text())
            return value
        except ValueError:
            Logger.log_error("Trying to get_float() from InputField but the input text is not an integer. Will use -1.0")
            return -1.0

class ComboBox(QWidget):
    def __init__(self, label_font, fixed_width, fixed_height, items = None, on_index_change_callback = None, widgets_list = None):
        super().__init__()
        self.label_font = label_font
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height
        self.items = items
        self.on_index_change_callback = on_index_change_callback
        self.widgets_list = widgets_list

        self.create_ui()

    def create_ui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.cbox = QComboBox(self)
        if self.items is not None:
            self.cbox.addItems(self.items)
        self.cbox.setFont(self.label_font)
        self.cbox.setFixedSize(self.fixed_width, self.fixed_height)
        if self.on_index_change_callback is not None:
            self.cbox.currentIndexChanged.connect(self.on_index_change_callback)
        if self.widgets_list is not None:
            self.widgets_list.append(self)
        self.layout.addWidget(self.cbox)

    def set_items(self, items):
        self.items = items
        self.cbox.clear()
        self.cbox.addItems(self.items)

    def clear(self):
        self.cbox.clear()

    def get_index(self):
        return self.cbox.currentIndex()

    def get_text(self):
        return self.cbox.currentText()

class ComboBoxInputField(QWidget):
    def __init__(self, label_str, label_font, fixed_width, fixed_height, items = None, widgets_list = None):
        super().__init__()
        self.label_str = label_str
        self.label_font = label_font
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height
        self.items = items
        self.widgets_list = widgets_list

        self.create_ui()

    def create_ui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self.label_str)
        self.label.setFont(self.label_font)
        self.cbox = QComboBox(self)
        if self.items is not None:
            self.cbox.addItems(self.items)
        self.cbox.setFont(self.label_font)
        self.cbox.setFixedSize(self.fixed_width, self.fixed_height)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.cbox)
        if self.widgets_list is not None:
            self.widgets_list.append(self)

    def set_items(self, items):
        self.items = items
        self.cbox.clear()
        self.cbox.addItems(self.items)

    def clear(self):
        self.cbox.clear()

    def get_index(self):
        return self.cbox.currentIndex()

    def get_text(self):
        return self.cbox.currentText()