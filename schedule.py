from PySide6.QtCore import QDate
from reservation import Reservation
from logger import Logger

class Schedule:
    def __init__(self):
        self.data = {}
        self.default_date = QDate(2000, 1, 1)

    def load(self, filepath):
        try:
            file = open(filepath, 'r', encoding = "utf-8")
        except FileNotFoundError:
            Logger.log_error("Requested schedule file not found - {}".format(filepath))
            return

        for _, line in enumerate(file):
            line = line.strip()
            if line == "":
                continue
            if line.startswith('$'):
                self.handle_variable_assignment(line)
                continue
            reservation = Reservation.parse(line)
            self.add_reservation(reservation)

    def add_reservation(self, reservation):
        if reservation.date not in self.data:
            self.data[reservation.date] = {}
        if reservation.employee not in self.data[reservation.date]:
            self.data[reservation.date][reservation.employee] = []
        self.data[reservation.date][reservation.employee].append(reservation)

    def get_employees(self, date = None):
        if date is None:
            date = self.default_date
        return list(self.data[date].keys())

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
            self.default_date = Reservation.parse_date(var_value)
