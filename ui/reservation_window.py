from ui.reservation_form import ReservationForm

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QWidget, QVBoxLayout

class ReservationWindow(QDialog):
    def __init__(self, date, database, update_home_widget_callback):
        super().__init__()
        self.date = date
        self.database = database
        self.update_home_widget_callback = update_home_widget_callback

        self.setWindowTitle("Резервация")
        self.setGeometry(20, 40, 500, 300)

        self.create_ui()

    def create_ui(self, deleteOldLayout = False):
        if deleteOldLayout:
            # Create a temporary QWidget object and set its layout to be the current old layout.
            # That way, the temporary object is immediately deleted and it deletes the layout and all of its children widgets
            QWidget().setLayout(self.layout)
            # After that we can just create a new layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.reservation_form = ReservationForm(self.date, self.database, self.reservation_made)
        self.layout.addWidget(self.reservation_form)

    def reservation_made(self):
        self.update_home_widget_callback()
        self.create_ui(True)