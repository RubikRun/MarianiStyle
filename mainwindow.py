# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Qt Table Example")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.create_table()

    def create_table(self):
            # Create a QTableWidget instance
            self.tableWidget = QTableWidget(self)

            # Set the number of rows and columns
            self.tableWidget.setRowCount(4)
            self.tableWidget.setColumnCount(3)

            # Set table headers
            self.tableWidget.setHorizontalHeaderLabels(["Name", "Age", "Occupation"])

            # Populate the table with data
            data = [("John Doe", 30, "Engineer"),
                    ("Jane Smith", 25, "Designer"),
                    ("Bob Johnson", 40, "Manager"),
                    ("Alice Brown", 35, "Developer")]

            for row, rowData in enumerate(data):
                for col, value in enumerate(rowData):
                    item = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row, col, item)

            # Set styles for the table
            self.tableWidget.setStyleSheet("""
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
            font = QFont("Arial", 20)
            self.tableWidget.setFont(font)

            # Add the table to the main layout
            self.layout.addWidget(self.tableWidget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(900, 700)
    window.show()
    sys.exit(app.exec())
