# This Python file uses the following encoding: utf-8

from PySide2.QtWidgets import QDialog

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройки")
        self.setGeometry(200, 200, 1400, 800)
