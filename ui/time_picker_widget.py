from PySide2.QtCore import Qt, QTime
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QLineEdit

class TimePickerWidget(QWidget):
    def __init__(self, hour_begin, hour_end, label_font):
        super().__init__()
        self.hour_begin = hour_begin
        self.hour_end = hour_end
        self.label_font = label_font

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 150, 0)
        self.layout.setSpacing(0)

        self.hour_cbox = QComboBox(self)
        self.hour_cbox.addItems(["{:02d}".format(hour) for hour in range(self.hour_begin, self.hour_end + 1)])
        self.hour_cbox.setCurrentIndex(1)
        self.hour_cbox.setFont(self.label_font)
        self.hour_cbox.setFixedSize(50, int(self.label_font.pointSize() * 2.3))
        self.layout.addWidget(self.hour_cbox)

        self.colon_label = QLabel(" : ")
        self.colon_label.setFont(self.label_font)
        self.colon_label.setFixedWidth(20)
        self.layout.addWidget(self.colon_label)

        self.minute_cbox = QComboBox(self)
        self.minute_cbox.addItems(["{:02d}".format(minute) for minute in range(0, 65, 5)])
        self.minute_cbox.setFont(self.label_font)
        self.minute_cbox.setFixedSize(50, int(self.label_font.pointSize() * 2.3))
        self.layout.addWidget(self.minute_cbox)

    def get_time(self):
        time = QTime(
            int(self.hour_cbox.currentText()),
            int(self.minute_cbox.currentText())
        )
        return time

class TimePickerInputWidget(QWidget):
    def __init__(self, label_str, label_font, hour_begin, hour_end, fixed_width = None, fixed_height = None,  widgets_list = None):
        super().__init__()
        self.label_str = label_str
        self.label_font = label_font
        self.hour_begin = hour_begin
        self.hour_end = hour_end
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height
        self.widgets_list = widgets_list

        self.create_ui()

    def create_ui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self.label_str)
        self.label.setFont(self.label_font)
        self.time_picker_widget = TimePickerWidget(self.hour_begin, self.hour_end, self.label_font)
        self.time_picker_widget.setFixedSize(self.fixed_width, self.fixed_height)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.time_picker_widget)
        if self.widgets_list is not None:
            self.widgets_list.append(self)
