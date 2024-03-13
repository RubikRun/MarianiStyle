from home_widget import HomeWidget

import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Мариани Стайл")
        home_widget = HomeWidget()
        self.setCentralWidget(home_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1700, 800)
    window.show()
    sys.exit(app.exec())
