from logger import Logger

# Class that holds the schedule for a single date.
# It retrieves the reservations for that date from the database,
# organizes them per employee and per hour,
# and has convenient API for retrieving the reservations of a given employee at a given hour
class ScheduleHandler:
    def __init__(self, date, hour_begin, hour_end, database):
        self.date = date
        self.hour_begin = hour_begin
        self.hour_end = hour_end
        self.database = database

        self.init_data()

    # Initializes the self.data dictionary with the organized reservations
    def init_data(self):
        # Get reservations for date
        reservations = []
        for reservation in self.database.reservations:
            if reservation.date_time.date() == self.date:
                reservations.append(reservation)
        employees = self.database.employees
        # Initialize self.data with empty lists for all employees and hours
        self.data = {}
        for employee in employees:
            self.data[employee.id] = {}
            for hour in range(self.hour_begin, self.hour_end + 1):
                self.data[employee.id][hour] = []
        # Organize reservations into the dictionary
        for reservation in reservations:
            if reservation.date_time.date() != self.date:
                Logger.log_error(
                    "Creating Schedule but reservations retrieved from database for the given date contain a reservation with a different date. This reservation will be skipped."
                )
                continue
            self.data[reservation.employee_id][reservation.date_time.time().hour()].append(reservation)

    # Returns a list of reservations for the given employee in the given hour
    def get_reservations(self, employee_id, hour):
        return self.data[employee_id][hour]

    # Returns a map of reservations for the given employee.
    # It maps from vrow indices to reservations that should be put on that vrow in the table
    def get_reservations_map(self, employee_id):
        rmap = {}
        vrow = 0
        for hour in range(self.hour_begin, self.hour_end + 1):
            rlist = self.get_reservations(employee_id, hour)
            if len(rlist) > 0:
                for reservation in rlist:
                    rmap[vrow] = reservation
                    vrow += 1
            else:
                vrow += 1
        return rmap

    def get_percent_sum(self, employee_id):
        psum = 0
        for hour in range(self.hour_begin, self.hour_end + 1):
            rlist = self.get_reservations(employee_id, hour)
            for reservation in rlist:
                psum += reservation.percent
        return psum * 0.4

    def get_kasa_sum(self, employee_id):
        ksum = 0
        for hour in range(self.hour_begin, self.hour_end + 1):
            rlist = self.get_reservations(employee_id, hour)
            for reservation in rlist:
                ksum += reservation.kasa
        return ksum