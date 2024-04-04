from logger import Logger
from database.data_io import DataIO
from database.employee import Employee
from database.packet import Packet
from database.voucher import Voucher
from database.packet_instance import PacketInstance
from database.client import Client
from database.reservation import Reservation

class Database:
    def load_employees(self, filepath):
        self.employees = []
        self.employer_id = None
        # Open file
        try:
            file = open(filepath, 'r', encoding = "utf-8")
        except FileNotFoundError:
            Logger.log_error("Requested employees file not found - {}. Loading of employees will be skipped".format(filepath))
            return
        # Load employees by deserializing each line of the file
        for line in file:
            line = line.strip()
            if line == "":
                continue
            employer_id = DataIO.parse_variable_assignment(line, "EMPLOYER_ID", 'i')
            if employer_id is not None:
                self.employer_id = employer_id
                continue
            employee = Employee.deserialize(line)
            self.add_employee(employee)
        # Check if employer's ID was defined
        if self.employer_id is None:
            Logger.log_error("Employer's ID was not assigned. Employer will be set to be the employee with the minimum ID")
            self.employer_id = min([employee.id for employee in self.employees])
        # Check if employer's ID exists and put employer first in the list
        employer_id_exists = False
        for idx, employee in enumerate(self.employees):
            if employee.id == self.employer_id:
                if idx != 0:
                    self.employees[0], self.employees[idx] = self.employees[idx], self.employees[0]
                employer_id_exists = True
                break
        if not employer_id_exists:
            Logger.log_error("Employer's ID doesn't exist. Employer will be set to be the employee with the minimum ID")
            self.employer_id = min([employee.id for employee in self.employees])

    def load_packets(self, filepath):
        self.packets = []
        # Open file
        try:
            file = open(filepath, 'r', encoding = "utf-8")
        except FileNotFoundError:
            Logger.log_error("Requested packets file not found - {}. Loading of packets will be skipped".format(filepath))
            return
        # Load packets by deserializing each line of the file
        for line in file:
            line = line.strip()
            if line == "":
                continue
            packet = Packet.deserialize(line)
            self.add_packet(packet)

    def load_packet_instances(self, filepath):
        self.packet_instances = []
        # Open file
        try:
            file = open(filepath, 'r', encoding = "utf-8")
        except FileNotFoundError:
            Logger.log_error("Requested packet instances file not found - {}. Loading of packet instances will be skipped".format(filepath))
            return
        # Load packet instances by deserializing each line of the file
        for line in file:
            line = line.strip()
            if line == "":
                continue
            packet_instance = PacketInstance.deserialize(line)
            self.add_packet_instance(packet_instance)

    def load_vouchers(self, filepath):
        self.vouchers = []
        # Open file
        try:
            file = open(filepath, 'r', encoding = "utf-8")
        except FileNotFoundError:
            Logger.log_error("Requested vouchers file not found - {}. Loading of vouchers will be skipped".format(filepath))
            return
        # Load vouchers by deserializing each line of the file
        for line in file:
            line = line.strip()
            if line == "":
                continue
            voucher = Voucher.deserialize(line)
            self.add_voucher(voucher)

    def load_clients(self, filepath):
        self.clients = []
        # Open file
        try:
            file = open(filepath, 'r', encoding = "utf-8")
        except FileNotFoundError:
            Logger.log_error("Requested clients file not found - {}. Loading of clients will be skipped".format(filepath))
            return
        # Load clients by deserializing each line of the file
        for line in file:
            line = line.strip()
            if line == "":
                continue
            client = Client.deserialize(line)
            self.add_client(client)

    def load_reservations(self, filepath):
        self.reservations = []
        # Open file
        try:
            file = open(filepath, 'r', encoding = "utf-8")
        except FileNotFoundError:
            Logger.log_error("Requested reservations file not found - {}. Loading of reservations will be skipped".format(filepath))
            return
        # Load reservations by deserializing each line of the file
        for line in file:
            line = line.strip()
            if line == "":
                continue
            reservation = Reservation.deserialize(line)
            self.add_reservation(reservation)

    def export_employees(self, filepath):
        # Open file
        try:
            file = open(filepath, 'w', encoding = "utf-8")
        except PermissionError:
            Logger.log_error("You don't have permission to export employees to this file - {}".format(filepath))
            return
        # Export employees by serializing each one and writing it as a line in the file
        for employee in self.employees:
            file.write(employee.serialize() + "\n")
        # Export employer's ID as a variable assignment
        employer_id_asgn = DataIO.create_variable_assignment("EMPLOYER_ID", self.employer_id, 'i')
        file.write(employer_id_asgn + "\n")

    def export_packets(self, filepath):
        # Open file
        try:
            file = open(filepath, 'w', encoding = "utf-8")
        except PermissionError:
            Logger.log_error("You don't have permission to export packets to this file - {}".format(filepath))
            return
        # Export packets by serializing each one and writing it as a line in the file
        for packet in self.packets:
            file.write(packet.serialize() + "\n")

    def export_packet_instances(self, filepath):
        # Open file
        try:
            file = open(filepath, 'w', encoding = "utf-8")
        except PermissionError:
            Logger.log_error("You don't have permission to export packet instances to this file - {}".format(filepath))
            return
        # Export packet instances by serializing each one and writing it as a line in the file
        for packet_instance in self.packet_instances:
            file.write(packet_instance.serialize() + "\n")

    def export_vouchers(self, filepath):
        # Open file
        try:
            file = open(filepath, 'w', encoding = "utf-8")
        except PermissionError:
            Logger.log_error("You don't have permission to export vouchers to this file - {}".format(filepath))
            return
        # Export vouchers by serializing each one and writing it as a line in the file
        for voucher in self.vouchers:
            file.write(voucher.serialize() + "\n")

    def export_clients(self, filepath):
        # Open file
        try:
            file = open(filepath, 'w', encoding = "utf-8")
        except PermissionError:
            Logger.log_error("You don't have permission to export clients to this file - {}".format(filepath))
            return
        # Export clients by serializing each one and writing it as a line in the file
        for client in self.clients:
            file.write(client.serialize() + "\n")

    def export_reservations(self, filepath):
        # Open file
        try:
            file = open(filepath, 'w', encoding = "utf-8")
        except PermissionError:
            Logger.log_error("You don't have permission to export reservations to this file - {}".format(filepath))
            return
        # Export reservations by serializing each one and writing it as a line in the file
        for reservation in self.reservations:
            file.write(reservation.serialize() + "\n")

    def add_employee(self, new_employee):
        # If ID is negative, create a new ID
        if new_employee.id < 0:
            new_employee.id = max([0] + [employee.id for employee in self.employees]) + 1
        # Check if ID is unique
        is_id_valid = True
        for employee in self.employees:
            if employee.id == new_employee.id:
                is_id_valid = False
        # If not unique, create a new ID
        if not is_id_valid:
            new_employee.id = max([0] + [employee.id for employee in self.employees]) + 1
            Logger.log_error("New employee has a duplicate ID. Employee will be added with a new ID = {}".format(new_employee.id))
        # Add employee to list
        self.employees.append(new_employee)
        return new_employee.id

    def add_packet(self, new_packet):
        # If ID is negative, create a new ID
        if new_packet.id < 0:
            new_packet.id = max([0] + [packet.id for packet in self.packets]) + 1
        # Check if ID is unique
        is_id_valid = True
        for packet in self.packets:
            if packet.id == new_packet.id:
                is_id_valid = False
        # If not unique, create a new ID
        if not is_id_valid:
            new_packet.id = max([0] + [packet.id for packet in self.packets]) + 1
            Logger.log_error("New packet has a duplicate ID. Packet will be added with a new ID = {}".format(new_packet.id))
        # Add packet to list
        self.packets.append(new_packet)
        return new_packet.id

    def add_packet_instance(self, new_packet_instance):
        # If ID is negative, create a new ID
        if new_packet_instance.id < 0:
            new_packet_instance.id = max([0] + [packet_instance.id for packet_instance in self.packet_instances]) + 1
        # Check if ID is unique
        is_id_valid = True
        for packet_instance in self.packet_instances:
            if packet_instance.id == new_packet_instance.id:
                is_id_valid = False
        # If not unique, create a new ID
        if not is_id_valid:
            new_packet_instance.id = max([0] + [packet_instance.id for packet_instance in self.packet_instances]) + 1
            Logger.log_error("New packet instance has a duplicate ID. Packet instance will be added with a new ID = {}".format(new_packet_instance.id))
        # Add packet instance to list
        self.packet_instances.append(new_packet_instance)
        return new_packet_instance.id

    def add_voucher(self, new_voucher):
        # If ID is negative, create a new ID
        if new_voucher.id < 0:
            new_voucher.id = max([0] + [voucher.id for voucher in self.vouchers]) + 1
        # Check if ID is unique
        is_id_valid = True
        for voucher in self.vouchers:
            if voucher.id == new_voucher.id:
                is_id_valid = False
        # If not unique, create a new ID
        if not is_id_valid:
            new_voucher.id = max([0] + [voucher.id for voucher in self.vouchers]) + 1
            Logger.log_error("New voucher has a duplicate ID. voucher will be added with a new ID = {}".format(new_voucher.id))
        # Add voucher to list
        self.vouchers.append(new_voucher)
        return new_voucher.id

    def add_client(self, new_client):
        # If ID is negative, create a new ID
        if new_client.id < 0:
            new_client.id = max([0] + [client.id for client in self.clients]) + 1
        # Check if ID is unique
        is_id_valid = True
        for client in self.clients:
            if client.id == new_client.id:
                is_id_valid = False
        # If not unique, create a new ID
        if not is_id_valid:
            new_client.id = max([0] + [client.id for client in self.clients]) + 1
            Logger.log_error("New client has a duplicate ID. Client will be added with a new ID = {}".format(new_client.id))
        # Add client to list
        self.clients.append(new_client)
        return new_client.id

    def add_reservation(self, new_reservation):
        # If ID is negative, create a new ID
        if new_reservation.id < 0:
            new_reservation.id = max([0] + [reservation.id for reservation in self.reservations]) + 1
        # Check if ID is unique
        is_id_valid = True
        for reservation in self.reservations:
            if reservation.id == new_reservation.id:
                is_id_valid = False
        # If not unique, create a new ID
        if not is_id_valid:
            new_reservation.id = max([0] + [reservation.id for reservation in self.reservations]) + 1
            Logger.log_error("New reservation has a duplicate ID. Reservation will be added with a new ID = {}".format(new_reservation.id))
        # Add reservation to list
        self.reservations.append(new_reservation)
        return new_reservation.id

    def get_employer(self):
        for employee in self.employees:
            if employee.id == self.employer_id:
                return employee

    def get_client(self, client_id):
        for client in self.clients:
            if client.id == client_id:
                return client
        Logger.log_error("Database cannot find client with requested ID = {}".format(client_id))

    def get_packet(self, packet_id):
        for packet in self.packets:
            if packet.id == packet_id:
                return packet
        Logger.log_error("Database cannot find packet with requested ID = {}".format(packet_id))

    def get_packet_instance(self, packet_instance_id):
        for packet_instance in self.packet_instances:
            if packet_instance.id == packet_instance_id:
                return packet_instance
        Logger.log_error("Database cannot find packet instance with requested ID = {}".format(packet_instance_id))

    def get_voucher(self, voucher_id):
        for voucher in self.vouchers:
            if voucher.id == voucher_id:
                return voucher
        Logger.log_error("Database cannot find voucher with requested ID = {}".format(voucher_id))

    def get_reservation(self, reservation_id):
        for reservation in self.reservations:
            if reservation.id == reservation_id:
                return reservation
        Logger.log_error("Database cannot find reservation with requested ID = {}".format(reservation_id))

    def delete_reservation(self, reservation_id):
        for ridx, reservation in enumerate(self.reservations):
            if reservation.id == reservation_id:
                if reservation.packet_instance_id >= 0:
                    packet_instance = self.get_packet_instance(reservation.packet_instance_id)
                    if packet_instance is not None:
                        if packet_instance.use_count >= 1:
                            packet_instance.use_count -= 1
                        else:
                            Logger.log_error(
                                "Database is deleting a reservation that uses a packet instance of a user. Trying to decrement the use_count of the packet instance but it's < 1"
                            )
                del self.reservations[ridx]

    def delete_packet_instance(self, packet_instance_id):
        for pidx, packet_instance in enumerate(self.packet_instances):
            if packet_instance.id != packet_instance_id:
                continue
            for client in self.clients:
                client.packet_instances = [piid for piid in client.packet_instances if piid != packet_instance_id]
            # Find all reservations referencing this packet instance and set their packet_instance_id to -1.
            # They don't really need it once they are created and once the packet instance is gone.
            # All the info is in string form in reservation.procedure anyway.
            for reservation in self.reservations:
                if reservation.packet_instance_id == packet_instance_id:
                    reservation.packet_instance_id = -1
            del self.packet_instances[pidx]
            return True
        return False

    def delete_packet(self, packet_id):
        for pidx, packet in enumerate(self.packets):
            if packet.id != packet_id:
                continue
            # Collect IDs of packet instances that reference this packet. They need to be deleted
            todelete_packet_instance_ids = [packet_instance.id for packet_instance in self.packet_instances if packet_instance.packet_id == packet.id]
            # Delete packet instances one by one using their IDs to avoid problems with traversing while deleting
            for packet_instance_id in todelete_packet_instance_ids:
                # This will delete the packet instance as well as remove it from clients and reservations that reference it
                self.delete_packet_instance(packet_instance_id)
            # Now we are safe to delete the packet
            del self.packets[pidx]
            return True
        return False

    def delete_client(self, client_id):
        for cidx, client in enumerate(self.clients):
            if client.id != client_id:
                continue
            self.packet_instances = [packet_instance for packet_instance in self.packet_instances if packet_instance.client_id != client_id]
            self.reservations = [reservation for reservation in self.reservations if reservation.client_id != client_id]
            del self.clients[cidx]
            return True
        return False

    def show_info(self):
        dashes = "-" * 10
        tab = "    "
        # Show info about employees
        Logger.log_info(dashes + " Employees " + dashes)
        Logger.log_info("There are {} employees loaded.".format(len(self.employees)))
        for idx, employee in enumerate(self.employees):
            Logger.log_info(tab + "Employee {}:".format(idx))
            Logger.log_info(tab * 2 + "id = {}".format(employee.id))
            Logger.log_info(tab * 2 + "name = {}".format(employee.name))
        Logger.log_info("Employer's ID is {}".format(self.employer_id))
        Logger.log_info("")
        # Show info about packets
        Logger.log_info(dashes + " Packets " + dashes)
        Logger.log_info("There are {} packets loaded.".format(len(self.packets)))
        for idx, packet in enumerate(self.packets):
            Logger.log_info(tab + "Packet {}:".format(idx))
            Logger.log_info(tab * 2 + "id = {}".format(packet.id))
            Logger.log_info(tab * 2 + "name = {}".format(packet.name))
            Logger.log_info(tab * 2 + "price = {}".format(packet.price))
            Logger.log_info(tab * 2 + "price_singular = {}".format(packet.price_singular))
            Logger.log_info(tab * 2 + "uses = {}".format(packet.uses))
            Logger.log_info(tab * 2 + "validity = {}".format(packet.validity))
        Logger.log_info("")
        # Show info about packet instances
        Logger.log_info(dashes + " Packet instances " + dashes)
        Logger.log_info("There are {} packet instances loaded.".format(len(self.packet_instances)))
        for idx, packet_instance in enumerate(self.packet_instances):
            Logger.log_info(tab + "Packet instance {}:".format(idx))
            Logger.log_info(tab * 2 + "id = {}".format(packet_instance.id))
            Logger.log_info(tab * 2 + "packet_id = {}".format(packet_instance.packet_id))
            Logger.log_info(tab * 2 + "client_id = {}".format(packet_instance.client_id))
            Logger.log_info(tab * 2 + "employee_id = {}".format(packet_instance.employee_id))
            Logger.log_info(tab * 2 + "bought_on = {}".format(packet_instance.bought_on))
            Logger.log_info(tab * 2 + "use_count = {}".format(packet_instance.use_count))
        Logger.log_info("")
        # Show info about vouchers
        Logger.log_info(dashes + " Vouchers " + dashes)
        Logger.log_info("There are {} vouchers loaded.".format(len(self.vouchers)))
        for idx, voucher in enumerate(self.vouchers):
            Logger.log_info(tab + "Voucher {}:".format(idx))
            Logger.log_info(tab * 2 + "id = {}".format(voucher.id))
            Logger.log_info(tab * 2 + "client_id = {}".format(voucher.client_id))
            Logger.log_info(tab * 2 + "employee_id = {}".format(voucher.employee_id))
            Logger.log_info(tab * 2 + "bought_on = {}".format(voucher.bought_on))
            Logger.log_info(tab * 2 + "validity = {}".format(voucher.validity))
            Logger.log_info(tab * 2 + "price = {}".format(voucher.price))
            Logger.log_info(tab * 2 + "spent = {}".format(voucher.spent))
        Logger.log_info("")
        # Show info about clients
        Logger.log_info(dashes + " Clients " + dashes)
        Logger.log_info("There are {} clients loaded.".format(len(self.clients)))
        for idx, client in enumerate(self.clients):
            Logger.log_info(tab + "Client {}:".format(idx))
            Logger.log_info(tab * 2 + "id = {}".format(client.id))
            Logger.log_info(tab * 2 + "name = {}".format(client.name))
            Logger.log_info(tab * 2 + "phone = {}".format(client.phone))
            Logger.log_info(tab * 2 + "packet_instances = {}".format(client.packet_instances))
        Logger.log_info("")
        # Show info about reservations
        Logger.log_info(dashes + " Reservation " + dashes)
        Logger.log_info("There are {} reservations loaded.".format(len(self.reservations)))
        for idx, reservation in enumerate(self.reservations):
            Logger.log_info(tab + "Reservation {}:".format(idx))
            Logger.log_info(tab * 2 + "id = {}".format(reservation.id))
            Logger.log_info(tab * 2 + "employee_id = {}".format(reservation.employee_id))
            Logger.log_info(tab * 2 + "client_id = {}".format(reservation.client_id))
            Logger.log_info(tab * 2 + "date_time = {}".format(reservation.date_time))
            Logger.log_info(tab * 2 + "procedure = {}".format(reservation.procedure))
            Logger.log_info(tab * 2 + "packet_instance_id = {}".format(reservation.packet_instance_id))
            Logger.log_info(tab * 2 + "percent = {}".format(reservation.percent))
            Logger.log_info(tab * 2 + "kasa = {}".format(reservation.kasa))
            Logger.log_info(tab * 2 + "bg_colors = {}".format(reservation.bg_colors))
            Logger.log_info(tab * 2 + "fg_colors = {}".format(reservation.fg_colors))
        Logger.log_info("")
