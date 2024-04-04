from logger import Logger

class PacketsSoldHandler:
    def __init__(self, date, database):
        self.date = date
        self.database = database

        self.init_data()

    # Initializes the self.data dictionary with the organized packets sold
    def init_data(self):
        # Get packet instances for date and sort them by time
        packet_instances = []
        for packet_instance in self.database.packet_instances:
            if packet_instance.bought_on.date() == self.date:
                packet_instances.append(packet_instance)
        packet_instances = sorted(packet_instances, key=lambda packet_instance : packet_instance.bought_on.time())
        employees = self.database.employees
        # Organize packet instances by employee and insert them in a dictionary with vrow keys to be used directly by a TableBase
        self.data = {}
        for employee in employees:
            self.data[employee.id] = {}
            vrow = 0
            for packet_instance in packet_instances:
                if packet_instance.employee_id != employee.id:
                    continue
                self.data[employee.id][vrow] = packet_instance
                vrow += 1

    # Returns a map of packet instances for the given employee
    def get_packet_instances_map(self, employee_id):
        return self.data[employee_id]
