from logger import Logger

from ui.input_field import InputField, ComboBoxInputField, ComboBox
from ui.time_picker_widget import TimePickerInputWidget
from ui.text_button import TextButton

from database.reservation import Reservation
from database.packet_instance import PacketInstance

from PySide2.QtCore import Qt, Slot, QDateTime
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QCompleter

class ReservationForm(QWidget):
    def __init__(self, date, database, update_schedule_callback):
        super().__init__()
        self.date = date
        self.database = database
        self.update_schedule_callback = update_schedule_callback
        self.init_constants()

        self.create_ui()

    def init_constants(self):
        self.FONT = QFont("Verdana", 12)
        self.FONT_HEADER = QFont("Verdana", 16, QFont.Bold)
        self.HOUR_BEGIN = 8
        self.HOUR_END = 20

    def create_ui(self, delete_old_layout = False):
        self.employees = self.database.employees
        self.clients = self.database.clients
        self.packets = self.database.packets
        self.vouchers = self.database.vouchers

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

        self.client_input_field = InputField("Клиент", self.FONT, None, [client.get_view() for client in self.clients], self.on_client_updated)
        self.layout.addWidget(self.client_input_field, 2, 0, 1, 2)

        self.packet_mode_cbox = ComboBox(self.FONT, 250, int(self.FONT.pointSize() * 2.5),
                                         ["Без пакет", "С пакет", "Купуване на пакет", "С ваучер", "Купуване на ваучер"], self.packet_mode_changed)
        self.layout.addWidget(self.packet_mode_cbox, 3, 0, 1, 2)
        self.layout.setAlignment(self.packet_mode_cbox, Qt.AlignLeft)

        self.create_widgets_for_packet_mode()

    # Create the widgets specific to the currently selected packet mode
    def create_widgets_for_packet_mode(self):
        packet_mode_index = self.packet_mode_cbox.get_index()

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
        elif packet_mode_index == 2:
            self.packet_cbox_input_field = ComboBoxInputField("Пакет", self.FONT, 350, int(self.FONT.pointSize() * 2.5),
                                                              [packet.get_view() for packet in self.packets], self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.packet_cbox_input_field, 4, 0, 1, 2)
            self.layout.setAlignment(self.packet_cbox_input_field, Qt.AlignLeft)

            self.reserve_button = TextButton("Купи", self.FONT, 100, 40, self.reserve_pressed, self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.reserve_button, 5, 0, 1, 1)
            self.layout.setAlignment(self.reserve_button, Qt.AlignLeft)
        elif packet_mode_index == 3:
            self.time_picker_input_widget = TimePickerInputWidget("Време", self.FONT, self.HOUR_BEGIN, self.HOUR_END,
                                                                  290, int(self.FONT.pointSize() * 2.3), self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.time_picker_input_widget, 4, 0, 1, 2)
            self.layout.setAlignment(self.time_picker_input_widget, Qt.AlignLeft)

            self.vouchers_label = QLabel()
            self.vouchers_label.setFont(self.FONT)
            self.vouchers_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(self.vouchers_label, 5, 0, 1, 2)
            self.widgets_of_current_packet_mode.append(self.vouchers_label)
            self.update_with_vouchers_of_client()

            self.procedure_input_field = InputField("Процедура", self.FONT, self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.procedure_input_field, 6, 0, 1, 2)

            self.price_input_field = InputField("Цена", self.FONT, self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.price_input_field, 7, 0, 1, 2)

            self.reserve_button = TextButton("Запази", self.FONT, 100, 40, self.reserve_pressed, self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.reserve_button, 8, 0, 1, 1)
            self.layout.setAlignment(self.reserve_button, Qt.AlignLeft)
        else:
            self.price_input_field = InputField("Стойност", self.FONT, self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.price_input_field, 4, 0, 1, 2)

            self.validity_cbox = ComboBoxInputField("Валидност", self.FONT, 60, int(self.FONT.pointSize() * 2.5),
                                                    [str(months) for months in range(1, 13)], self.widgets_of_current_packet_mode)
            self.validity_cbox.cbox.setCurrentIndex(4) # set default validity to be 5 months
            self.layout.addWidget(self.validity_cbox, 5, 0, 1, 2)
            self.layout.setAlignment(self.validity_cbox, Qt.AlignLeft)

            self.reserve_button = TextButton("Купи", self.FONT, 100, 40, self.reserve_pressed, self.widgets_of_current_packet_mode)
            self.layout.addWidget(self.reserve_button, 6, 0, 1, 1)
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

    # Retrieves the currently selected client from database
    def get_current_client(self):
        client_view = self.client_input_field.get_text()
        if client_view == "":
            return None
        for client in self.clients:
            if client_view == client.get_view():
                return client

    # Retrieves the currently selected employee from database
    def get_current_employee(self):
        employee_name = self.employee_cbox.get_text()
        for employee in self.employees:
            if employee_name == employee.name:
                return employee

    # Retrieves the currently selected packet instance for the given client
    def get_packet_instance(self, client):
        packet_instance_view = self.packet_cbox_input_field.get_text()
        if packet_instance_view is None or packet_instance_view == "":
            return None
        packet_instance = client.get_packet_instance_from_view(self.database, packet_instance_view)
        return packet_instance

    # Retrieves the currently selected packet from database
    def get_packet(self):
        packet_view = self.packet_cbox_input_field.get_text()
        if packet_view is None or packet_view == "":
            return None
        for packet in self.packets:
            if packet_view == packet.get_view():
                return packet

    def on_client_updated(self):
        self.update_with_packet_instances_of_client()
        self.update_with_vouchers_of_client()

    # If packet mode is 1, we have a combo box which shows the packet instances
    # of the currently selected client, if there is one.
    # This function updates the combo box items with the views of the packet instances
    # of the selected client. To be called whenever the selected client changes.
    def update_with_packet_instances_of_client(self):
        if self.packet_mode_cbox.get_index() != 1:
            return

        client = self.get_current_client()

        self.packet_cbox_input_field.clear()
        if client is not None:
            self.packet_cbox_input_field.set_items(client.get_packet_instances_views(self.database))

    # Same as above but for packet mode 3
    def update_with_vouchers_of_client(self):
        if self.packet_mode_cbox.get_index() != 3:
            return

        client = self.get_current_client()

        if client is None:
            self.vouchers_label.setText("(няма избран клиент)")
        else:
            self.vouchers_label.setText("Клиентът има ваучери на обща стойност: {}лв".format(int(client.get_vouchers_remaining_sum(self.database))))

    # Called when the reserve/buy button is pressed
    @Slot()
    def reserve_pressed(self):
        employee = self.get_current_employee()
        client = self.get_current_client()

        packet_mode_index = self.packet_mode_cbox.get_index()
        if packet_mode_index == 0:
            time = self.time_picker_input_widget.get_time()
            date_time = QDateTime(self.date, time)
            procedure = self.procedure_input_field.get_text()
            price = self.price_input_field.get_float()

            reservation = Reservation(-1, employee.id, client.id, date_time, procedure, -1, price, price, [], [])
            self.database.add_reservation(reservation)
        elif packet_mode_index == 1:
            time = self.time_picker_input_widget.get_time()
            date_time = QDateTime(self.date, time)
            packet_instance = self.get_packet_instance(client)
            if packet_instance is None:
                Logger.log_error("Invalid/No packet instance selected for selected client")
                return
            packet = self.database.get_packet(packet_instance.packet_id)
            if packet is None:
                Logger.log_error("Selected packet instance references a non-existing packet")
                return
            if packet_instance.use_count >= packet.uses:
                Logger.log_error("Selected packet instance is all used")
                return
            packet_instance.use_count += 1

            reservation = Reservation(-1, employee.id, client.id, date_time, packet_instance.get_view(self.database), packet_instance.id, packet.price_singular, 0, [], [])
            self.database.add_reservation(reservation)
        elif packet_mode_index == 2:
            packet = self.get_packet()
            if packet is None:
                Logger.log_error("Invalid/No packet selected")
                return
            new_packet_instance = PacketInstance(-1, packet.id, client.id, employee.id, QDateTime.currentDateTime(), 0)
            packet_instance_id = self.database.add_packet_instance(new_packet_instance)
            if packet_instance_id < 0:
                Logger.log_error("Could not create packet instance in database")
                return
            packet_instance = self.database.get_packet_instance(packet_instance_id)
            if packet_instance is None:
                Logger.log_error("Cannot retrieve newly created packet instance from database")
                return
            client.packet_instances.append(packet_instance.id)
        elif packet_mode_index == 3:
            time = self.time_picker_input_widget.get_time()
            date_time = QDateTime(self.date, time)
            procedure = self.procedure_input_field.get_text()
            price_str = self.price_input_field.get_text()
            try:
                price = float(price_str)
            except ValueError:
                Logger.log_error("Input price to be used from client's vouchers is not a float. Reservation will not be made.")
                return
            vouchers_rsum = client.get_vouchers_remaining_sum(self.database)
            if price > vouchers_rsum:
                Logger.log_error("Input price is higher than what client has in their vouchers. Reservation will not be made.")
                return

            if not client.use_amount_from_vouchers(price, self.database):
                Logger.log_error("Couldn't use the input amount from client's vouchers. Reservation will not be made.")
                return

            reservation = Reservation(-1, employee.id, client.id, date_time, "{} (с ваучер)".format(procedure), -1, price, 0, [], [])
            self.database.add_reservation(reservation)
        else:
            # TODO
            pass

        self.update_schedule_callback(True)
