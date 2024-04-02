from logger import Logger
from database.employee import Employee
from database.packet import Packet
from database.packet_instance import PacketInstance
from database.client import Client
from database.reservation import Reservation

class Database:
    def load_employees(self, filepath):
        # TODO: Should load employees from file into a list self.employees of Employee objects
        # TODO: Should also read employer's ID or use the default one to set self.employer_id
        pass

    def load_packets(self, filepath):
        # TODO: Should load packets from file into a list self.packets of Packet objects
        pass

    def load_packet_instances(self, filepath):
        # TODO: Should load packet instances from file into a list self.packet_instances of PacketInstance objects
        pass

    def load_clients(self, filepath):
        # TODO: Should load clients from file into a list self.clients of Client objects
        pass

    def load_reservations(self, filepath):
        # TODO: Should load reservations from file into a list self.reservations of Reservation objects
        pass

