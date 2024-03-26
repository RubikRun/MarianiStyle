from logger import Logger
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy, QAbstractScrollArea, QLabel
from PySide2.QtGui import QFont

schedule_font = QFont("Verdana", 12)
header_font = QFont("Verdana", 16, QFont.Bold)

class PacketsTableWidget(QWidget):
    def __init__(self, packets):
        super().__init__()
        self.packets = packets

        self.table_items_count = 0

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 10)
        self.layout.setSpacing(10)

        self.label = QLabel("Пакети")
        self.label.setFont(header_font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.label)

        self.create_table()
        self.fill_table()

    def create_table(self):
        # Create a table
        self.table = QTableWidget()
        # Handle properties of rows and columns and their headers
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Име", "Цена", "Брой ползвания", "Месеци валидност"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.verticalHeader().hide()
        # Set style sheet for the table
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f0f0f0;
                alternate-background-color: #e0e0e0;
                selection-background-color: #a0a0a0;
            }
            QHeaderView::section {
                background-color: #606060;
                color: white;
                font-size: """ + str(schedule_font.pointSize()) + """pt;
            }
        """)
        # Change the font of the table
        self.table.setFont(schedule_font)
        # Add table to layout
        self.layout.addWidget(self.table)

    def fill_table(self):
        for packet in self.packets:
            self.table.insertRow(self.table_items_count)
            # Handle name
            name_widget_item = QTableWidgetItem(packet.name)
            name_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(self.table_items_count, 0, name_widget_item)
            # Handle price
            price_widget_item = QTableWidgetItem(str(packet.price))
            price_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(self.table_items_count, 1, price_widget_item)
            # Handle uses
            uses_widget_item = QTableWidgetItem(str(packet.uses))
            uses_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(self.table_items_count, 2, uses_widget_item)
            # Handle validity
            validity_widget_item = QTableWidgetItem(str(packet.validity))
            validity_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(self.table_items_count, 3, validity_widget_item)
            self.table_items_count += 1
        self.table.setRowCount(self.table_items_count)

        #self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
