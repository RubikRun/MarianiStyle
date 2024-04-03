from PySide2.QtWidgets import QMainWindow, QHeaderView
from ui.home_widget import HomeWidget

class MainWindow(QMainWindow):
    def __init__(self, database):
        super().__init__()
        self.database = database

        self.setWindowTitle("Мариани Стайл")

        self.home_widget = HomeWidget(database)
        self.setCentralWidget(self.home_widget)

    def closeEvent(self, event):
        self.database.export_employees("data/employees.data")
        self.database.export_packets("data/packets.data")
        self.database.export_packet_instances("data/packet_instances.data")
        self.database.export_clients("data/clients.data")
        self.database.export_reservations("data/reservations.data")
        event.accept()