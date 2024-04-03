import sys
from PySide2.QtWidgets import QApplication

from database.database import Database
from ui.main_window import MainWindow

database = Database()
database.load_employees("data/employees.data")
database.load_packets("data/packets.data")
database.load_packet_instances("data/packet_instances.data")
database.load_clients("data/clients.data")
database.load_reservations("data/reservations.data")

database.show_info()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(database)
    window.resize(1800, 940)
    window.show()
    sys.exit(app.exec_())
