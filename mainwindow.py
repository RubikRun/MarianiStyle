# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QFont, QFontDatabase

class ScheduleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.items_count = 0

        # Example schedule
        self.schedule = {"Иван": 12, "Пешо": 13, "Борис": 14,
                      "Мишо": 14, "Георги": 15, "Станимир": 17,
                      "Таня": 17, "Мария": 17, "Спас": 18}

        # Left
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Клиент", "Час"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Set styles for the table
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f0f0f0;
                alternate-background-color: #e0e0e0;
                selection-background-color: #a0a0a0;
            }
            QHeaderView::section {
                background-color: #606060;
                color: white;
            }
        """)
        # Change the font of the table
        self.table.setFont(QFont("Verdana", 12))

        # QWidget Layout
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.table)

        # Fill example data
        self.fill_table()

    def fill_table(self, schedule=None):
        schedule = self.schedule if not schedule else schedule
        for client, hour in schedule.items():
            self.table.insertRow(self.items_count)
            self.table.setItem(self.items_count, 0, QTableWidgetItem(client))
            self.table.setItem(self.items_count, 1, QTableWidgetItem(str(hour)))
            self.items_count += 1

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Мариани Стайл")
        schedule_widget = ScheduleWidget()
        self.central_widget = schedule_widget
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(900, 700)
    window.show()
    sys.exit(app.exec())
