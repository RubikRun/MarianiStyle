from ui.input_field import InputField, ComboBoxInputField, ComboBox
from ui.time_picker_widget import TimePickerInputWidget
from ui.text_button import TextButton

from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QCompleter

class ReservationForm(QWidget):
    def __init__(self, date, database, reserve_callback, buy_packet_callback):
        super().__init__()
        self.date = date
        self.database = database
        self.reserve_callback = reserve_callback
        self.buy_packet_callback = buy_packet_callback
        self.init_constants()

        self.employees = self.database.employees
        self.clients = self.database.clients
        self.packets = self.database.packets

        self.create_ui()

    def init_constants(self):
        self.FONT = QFont("Verdana", 12)
        self.FONT_HEADER = QFont("Verdana", 16, QFont.Bold)
        self.HOUR_BEGIN = 8
        self.HOUR_END = 20

    def create_ui(self, delete_old_layout = False):
        if delete_old_layout:
            # Create a temporary QWidget object and set its layout to be the current old layout.
            # That way, the temporary object is immediately deleted and it deletes the layout and all of its children widgets
            QWidget().setLayout(self.layout)
            # After that we can just create a new layout
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.reserve_label = QLabel("Запазване на час")
        self.reserve_label.setFont(self.FONT_HEADER)
        self.reserve_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.reserve_label, 0, 0, 1, 2)

        self.employee_cbox = ComboBox(self.FONT, 100, int(self.FONT.pointSize() * 2.5), [employee.name for employee in self.employees])
        self.layout.addWidget(self.employee_cbox, 1, 0, 1, 2)
        self.layout.setAlignment(self.employee_cbox, Qt.AlignLeft)

        self.client_input_field = InputField("Клиент", self.FONT, None, [client.get_view() for client in self.clients], self.update_with_packet_instances_of_client)
        self.layout.addWidget(self.client_input_field, 2, 0, 1, 2)

        self.packet_mode_cbox = ComboBox(self.FONT, 250, int(self.FONT.pointSize() * 2.5), ["Без пакет", "С пакет", "Купуване на пакет"], self.packet_mode_changed)
        self.layout.addWidget(self.packet_mode_cbox, 3, 0, 1, 2)
        self.layout.setAlignment(self.packet_mode_cbox, Qt.AlignLeft)

        self.create_widgets_for_packet_mode()

    # Create the widgets specific to the currently selected packet mode
    def create_widgets_for_packet_mode(self):
        packet_mode_index = self.packet_mode_cbox.index()

        self.widgets_of_current_packet_mode = []

        if packet_mode_index == 0:
            self.time_picker_input_widget = TimePickerInputWidget("Време", self.FONT, self.HOUR_BEGIN, self.HOUR_END,
                                                                  290, int(self.FONT.pointSize() * 2.3), self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.time_picker_input_widget, 4, 0, 1, 2)
            self.layout.setAlignment(self.time_picker_input_widget, Qt.AlignLeft)

            self.procedure_input_field = InputField("Процедура", self.FONT, self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.procedure_input_field, 5, 0, 1, 2)

            self.price_input_field = InputField("Цена", self.FONT, self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.price_input_field, 6, 0, 1, 2)

            self.reserve_button = TextButton("Запази", self.FONT, 100, 40, self.reserve_pressed, self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.reserve_button, 7, 0, 1, 1)
            self.layout.setAlignment(self.reserve_button, Qt.AlignLeft)
        elif packet_mode_index == 1:
            self.time_picker_input_widget = TimePickerInputWidget("Време", self.FONT, self.HOUR_BEGIN, self.HOUR_END,
                                                                  290, int(self.FONT.pointSize() * 2.3), self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.time_picker_input_widget, 4, 0, 1, 2)
            self.layout.setAlignment(self.time_picker_input_widget, Qt.AlignLeft)

            self.packet_cbox_input_field = ComboBoxInputField("Пакет", self.FONT, 350, int(self.FONT.pointSize() * 2.5), None, self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.packet_cbox_input_field, 5, 0, 1, 2)
            self.layout.setAlignment(self.packet_cbox_input_field, Qt.AlignLeft)
            self.update_with_packet_instances_of_client()

            self.reserve_button = TextButton("Запази", self.FONT, 100, 40, self.reserve_pressed, self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.reserve_button, 6, 0, 1, 1)
            self.layout.setAlignment(self.reserve_button, Qt.AlignLeft)
        else:
            self.packet_cbox_input_field = ComboBoxInputField("Пакет", self.FONT, 350, int(self.FONT.pointSize() * 2.5),
                                                              [packet.name + " (" + str(packet.price) + "лв.)" for packet in self.packets], self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.packet_cbox_input_field, 4, 0, 1, 2)
            self.layout.setAlignment(self.packet_cbox_input_field, Qt.AlignLeft)

            self.reserve_button = TextButton("Купи", self.FONT, 100, 40, self.reserve_pressed, self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.reserve_button, 5, 0, 1, 1)
            self.layout.setAlignment(self.reserve_button, Qt.AlignLeft)

    # Deletes a given list of widgets from the layout
    def delete_widgets(self, widgets):
        for widget in widgets:
            index = self.layout.indexOf(widget)
            if index != -1:
                widget.setParent(None)
                widget.deleteLater()

    # Called when the packet mode is changed.
    # When this happens we need to delete all widgets of the current packet mode
    # and then create the widgets of the new packet mode
    @Slot()
    def packet_mode_changed(self):
        self.delete_widgets(self.widgets_of_current_packet_mode)
        self.create_widgets_for_packet_mode()

    # To be called when clients are updated from the outside.
    # Then we need to recreate the UI here to make the QCompleter
    # know about the new/updated clients
    def update_clients(self, new_clients):
        self.clients = new_clients
        self.create_ui(True)

    # If packet mode is 1, we have a combo box which shows the packet instances
    # of the currently selected client, if there is one.
    # This function updates the combo box items with the views of the packet instances
    # of the selected client. To be called whenever the selected client changes.
    def update_with_packet_instances_of_client(self):
        if self.packet_mode_cbox.index() != 1:
            return

        client_view = self.client_input_field.get_text()
        if client_view == "":
            self.packet_cbox_input_field.clear()
            return
        client_exists = False
        for cl in self.clients:
            if client_view == cl.get_view():
                client = cl
                client_exists = True

        self.packet_cbox_input_field.clear()
        if client_exists:
            self.packet_cbox_input_field.set_items(client.get_packet_instances_views(self.database))

    # Called when the reserve/buy button is pressed
    @Slot()
    def reserve_pressed(self):
        # TODO
        print("reserve_pressed()")