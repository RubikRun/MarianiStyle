from PySide2.QtWidgets import QMainWindow, QHeaderView
from ui.home_widget import HomeWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мариани Стайл")

        self.home_widget = HomeWidget()
        self.setCentralWidget(self.home_widget)
