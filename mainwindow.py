from home_widget import HomeWidget

import sys
from PySide6.QtWidgets import QMainWindow, QApplication

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Мариани Стайл")
        self.home_widget = HomeWidget()
        self.setCentralWidget(self.home_widget)

    def closeEvent(self, event):
        self.home_widget.schedule.export("database/schedule.data")
        self.home_widget.export_clients("TODO")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1900, 800)
    window.show()
    sys.exit(app.exec())
