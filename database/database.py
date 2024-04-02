from logger import Logger
from database.data_io import DataIO
from database.employee import Employee
from database.packet import Packet
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
        # Check if employer's ID exists
        employer_id_exists = False
        for employee in self.employees:
            if employee.id == self.employer_id:
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
        # TODO: Should load packet instances from file into a list self.packet_instances of PacketInstance objects
        pass

    def load_clients(self, filepath):
        # TODO: Should load clients from file into a list self.clients of Client objects
        pass

    def load_reservations(self, filepath):
        # TODO: Should load reservations from file into a list self.reservations of Reservation objects
        pass

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

    def add_employee(self, new_employee):
        # Check if ID is unique
        max_id = 0
        is_id_valid = True
        for employee in self.employees:
            if employee.id == new_employee.id:
                is_id_valid = False
            if employee.id > max_id:
                max_id = employee.id
        # If not unique, create a new ID
        if not is_id_valid:
            new_employee.id = max_id + 1
            Logger.log_error("New employee has a duplicate ID. Employee will be added with a new ID = {}".format(new_employee.id))
        # Add employee to list
        self.employees.append(new_employee)

    def add_packet(self, new_packet):
        # Check if ID is unique
        max_id = 0
        is_id_valid = True
        for packet in self.packets:
            if packet.id == new_packet.id:
                is_id_valid = False
            if packet.id > max_id:
                max_id = packet.id
        # If not unique, create a new ID
        if not is_id_valid:
            new_packet.id = max_id + 1
            Logger.log_error("New packet has a duplicate ID. Packet will be added with a new ID = {}".format(new_packet.id))
        # Add packet to list
        self.packets.append(new_packet)

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
            Logger.log_info(tab * 2 + "uses = {}".format(packet.uses))
            Logger.log_info(tab * 2 + "validity = {}".format(packet.validity))