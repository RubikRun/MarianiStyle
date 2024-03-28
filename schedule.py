from PySide2.QtCore import QDate
from reservation import Reservation
from logger import Logger

class Schedule:
    def __init__(self, clients):
        self.data = {}
        self.default_date = QDate(2000, 1, 1)
        self.clients = clients

    def load(self, filepath):
        try:
            file = open(filepath, 'r', encoding = "utf-8")
        except FileNotFoundError:
            Logger.log_error("Requested schedule file not found - {}".format(filepath))
            return

        for line in file:
            line = line.strip()
            if line == "":
                continue
            if line.startswith('$'):
                self.handle_variable_assignment(line)
                continue
            reservation = Reservation.deserialize(line, self.clients)
            self.add_reservation(reservation)

    def export(self, filepath):
        try:
            file = open(filepath, 'w', encoding = "utf-8")
        except PermissionError:
            Logger.log_error("You don't have permission to export schedule to this file - {}".format(filepath))
            return
        if file is None:
            Logger.log_error("Cannot open file to export schedule - {}".format(filepath))

        file.write("$DEFAULT_DATE=" + str(self.default_date.year()) + ";" + str(self.default_date.month()) + ";" + str(self.default_date.day()) + "\n")
        for date, day_schedule in self.data.items():
            for employee, reservations in day_schedule.items():
                for reservation in reservations:
                    file.write(reservation.serialize() + "\n")

    def add_reservation(self, reservation):
        if reservation.date not in self.data:
            self.data[reservation.date] = {}
        if reservation.employee not in self.data[reservation.date]:
            self.data[reservation.date][reservation.employee] = []
        self.data[reservation.date][reservation.employee].append(reservation)

    # Returns the schedule for the requested date.
    # A list with employees from the previous date should be provided
    # in case the requested date doesn't exist in the schedule.
    def get_for_date(self, date, prev_employees):
        if date not in self.data:
            self.data[date] = {}
            for employee in prev_employees:
                self.data[date][employee] = []
        return self.data[date]

    def get_employees(self, date = None):
        # TODO: maybe make this be loaded from a config file, so that new employees can be added
        return ["Мариана", "Мери", "Валя"]

    def handle_variable_assignment(self, assignment):
        if not assignment.startswith('$'):
            Logger.log_error("Trying to assign a variable, but variable assignment string doesn't begin with $")
            return
        assignment = assignment[1:]
        assignment_parts = assignment.split('=')
        if len(assignment_parts) != 2:
            Logger.log_error("Trying to assign a variable, but variable assignment string should be of form $*=*")
            return
        var_name = assignment_parts[0].strip()
        var_value = assignment_parts[1].strip()
        self.set_variable(var_name, var_value)

    def set_variable(self, var_name, var_value):
        if var_name == "DEFAULT_DATE":
            self.default_date = Reservation.deserialize_date(var_value)
