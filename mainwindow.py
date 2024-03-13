from schedule_widget import ScheduleWidget
from schedule import Schedule
from PySide6.QtCore import QDate

import sys
from PySide6.QtWidgets import QMainWindow, QApplication

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Мариани Стайл")

        self.schedule = Schedule()
        self.schedule.load_example_data()
        self.date = QDate(2024, 4, 9)

        schedule_widget = ScheduleWidget(self.schedule, self.date)
        self.setCentralWidget(schedule_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1400, 600)
    window.show()
    sys.exit(app.exec())
