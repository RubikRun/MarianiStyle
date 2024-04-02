import sys
from PySide2.QtWidgets import QApplication

from database.database import Database

database = Database()
database.load_employees("data/employees.data")
database.load_packets("data/packets.data")
database.export_employees("data/employees.data")
database.export_packets("data/packets.data")
database.show_info()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # ...
    sys.exit(app.exec_())
