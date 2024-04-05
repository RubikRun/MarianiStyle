from ui.packet_register_form import PacketRegisterForm
from ui.packets_table_widget import PacketsTableWidget

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QWidget, QGridLayout

class PacketsWindow(QDialog):
    def __init__(self, database, update_home_widget_callback):
        super().__init__()
        self.database = database
        self.update_home_widget_callback = update_home_widget_callback

        self.setWindowTitle("Пакети")
        self.setGeometry(20, 40, 1000, 600)

        self.create_ui()

    def create_ui(self, deleteOldLayout = False):
        if deleteOldLayout:
            # Create a temporary QWidget object and set its layout to be the current old layout.
            # That way, the temporary object is immediately deleted and it deletes the layout and all of its children widgets
            QWidget().setLayout(self.layout)
            # After that we can just create a new layout
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.packet_register_form = PacketRegisterForm(self.database, self.on_packets_update)
        self.layout.addWidget(self.packet_register_form, 0, 0, 1, 1)

        self.packets_table_widget = PacketsTableWidget(self.database, self.on_packets_update)
        self.layout.addWidget(self.packets_table_widget, 1, 0, 1, 1)

    def on_packets_update(self, do_update_table = True):
        if do_update_table:
            self.create_ui(True)
        else:
            self.packet_register_form.create_ui(True)
        self.update_home_widget_callback()
