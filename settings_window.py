# This Python file uses the following encoding: utf-8

from packet_form import PacketForm
from packets_table_widget import PacketsTableWidget

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QWidget, QGridLayout

class SettingsWindow(QDialog):
    def __init__(self, parent, packets, add_packet_callback):
        super().__init__(parent)
        self.packets = packets
        self.add_packet_callback = add_packet_callback

        self.setWindowTitle("Настройки")
        self.setGeometry(200, 200, 800, 800)

        self.create_ui()

    def closeEvent(self, event):
        pass

    def create_ui(self, deleteOldLayout = False, packets = None):
        print("create_ui()", deleteOldLayout, packets)
        if packets is not None:
            self.packets = packets
        if deleteOldLayout:
            # Create a temporary QWidget object and set its layout to be the current old layout.
            # That way, the temporary object is immediately deleted and it deletes the layout and all of its children widgets
            QWidget().setLayout(self.layout)
            # After that we can just create a new layout
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 400)

        self.packet_form = PacketForm(self.add_packet_callback)
        self.layout.addWidget(self.packet_form, 0, 0, 1, 1)

        self.packets_table_widget = PacketsTableWidget(self.packets)
        self.layout.addWidget(self.packets_table_widget, 1, 0, 1, 1)
