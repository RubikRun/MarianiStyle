from schedule_widget import ScheduleWidget

import sys
from PySide6.QtWidgets import QMainWindow, QApplication

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Мариани Стайл")
        schedule_widget = ScheduleWidget()
        self.setCentralWidget(schedule_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1600, 900)
    window.show()
    sys.exit(app.exec())
