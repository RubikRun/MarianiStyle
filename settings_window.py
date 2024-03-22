# This Python file uses the following encoding: utf-8

from packet_form import PacketForm

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QWidget, QGridLayout

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройки")
        self.setGeometry(200, 200, 1400, 800)

        self.packet_form = PacketForm(None)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 600)
        self.layout.addWidget(self.packet_form, 0, 0, 1, 1)

    def closeEvent(self, event):
        pass