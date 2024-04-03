from PySide2.QtWidgets import QMainWindow, QHeaderView
from ui.home_widget import HomeWidget

class MainWindow(QMainWindow):
    def __init__(self, database):
        super().__init__()
        self.setWindowTitle("Мариани Стайл")

        self.home_widget = HomeWidget(database)
        self.setCentralWidget(self.home_widget)
