from PySide2.QtCore import Qt, QLocale
from PySide2.QtWidgets import QDialog, QHBoxLayout, QCalendarWidget

class CalendarWindow(QDialog):
    def __init__(self, date_changed_callback):
        super().__init__()
        self.date_changed_callback = date_changed_callback

        self.setWindowTitle("Избери дата")
        self.setGeometry(600, 600, 300, 300)

        self.create_ui()

    def create_ui(self):
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.setFirstDayOfWeek(Qt.Monday)
        self.calendar_widget.setLocale(QLocale(QLocale.Bulgarian))
        self.calendar_widget.selectionChanged.connect(self.on_date_selected)

        self.layout.addWidget(self.calendar_widget)

    def on_date_selected(self):
        selected_date = self.calendar_widget.selectedDate()
        self.date_changed_callback(selected_date)
        # No need to close the CalendarWindow here because calling the date_changed_callback will update the whole schedule UI
        # creating a new layout which will delete all children of the old layout including this CalendarWindow here.
        # If we close it here, it will be also deleted later and it will crash because it will already be deleted.