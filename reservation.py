from logger import Logger
from PySide6.QtCore import QDate, QTime

class TimeInterval:
    def __init__(self, time_begin, time_end):
        self.time_begin = time_begin
        self.time_end = time_end

    # Methods needed to make this class hashable, to be used for key in a dictionary
    def __hash__(self):
        return hash((self.time_begin, self.time_end))
    def __eq__(self, other):
        return (self.time_begin, self.time_end) == (other.time_begin, other.time_end)
    def __ne__(self, other):
        return not(self == other)

class Reservation:
    def __init__(self, employee, date, time_interval, client, procedure, percent, kasa):
        self.employee = employee
        self.date = date
        self.time_interval = time_interval
        self.client = client
        self.procedure = procedure
        self.percent = percent
        self.kasa = kasa

    # Parses a reservation from a declaration string. Returns the reservation.
    def parse(decl):
        if decl is None or decl == "":
            Logger.log_error("Reservation declaration is empty. Reservation will be skipped")
            return None
        decl_parts = decl.split(';')
        if len(decl_parts) != 12:
            Logger.log_error("Reservation declaration is invalid, should have 12 parts. Reservation will be skipped")
            return None
        employee = decl_parts[0].strip()
        if employee == "":
            Logger.log_error("Employee part of a reservation is empty. Reservation will be skipped")
            return None
        date = Reservation.parse_date_parts(decl_parts[1].strip(), decl_parts[2].strip(), decl_parts[3].strip())
        if date is None:
            return None
        time_begin = Reservation.parse_time(decl_parts[4].strip(), decl_parts[5].strip())
        if time_begin is None:
            return None
        time_end = Reservation.parse_time(decl_parts[6].strip(), decl_parts[7].strip())
        if time_end is None:
            return None
        client = decl_parts[8].strip()
        if client == "":
            Logger.log_error("Client part of a reservation is empty. Reservation will be skipped")
            return None
        procedure = decl_parts[9].strip()
        if procedure == "":
            Logger.log_error("Procedure part of a reservation is empty. Reservation will be skipped")
            return None
        percent_str = decl_parts[10].strip()
        try:
            percent = int(percent_str)
        except ValueError:
            Logger.log_error("Percent part of a reservation is not an integer. Reservation will be skipped")
            return None
        kasa_str = decl_parts[11].strip()
        try:
            kasa = int(kasa_str)
        except ValueError:
            Logger.log_error("Kasa part of a reservation is not an integer. Reservation will be skipped")
            return None

        reservation = Reservation(employee, date, TimeInterval(time_begin, time_end), client, procedure, percent, kasa)
        return reservation

    def parse_date(s):
        s_parts = s.split(";")
        if len(s_parts) != 3:
            Logger.log_error("Invalid date. Date should have exactly 3 parts")
            return None
        return Reservation.parse_date_parts(s_parts[0].strip(), s_parts[1].strip(), s_parts[2].strip())

    def parse_date_parts(y_str, m_str, d_str):
        try:
            year = int(y_str)
        except ValueError:
            Logger.log_error("Year part of a reservation is not an integer. Reservation will be skipped")
            return None
        try:
            month = int(m_str)
        except ValueError:
            Logger.log_error("Month part of a reservation is not an integer. Reservation will be skipped")
            return None
        try:
            day = int(d_str)
        except ValueError:
            Logger.log_error("Day part of a reservation is not an integer. Reservation will be skipped")
            return None
        return QDate(year, month, day)

    def parse_time(h_str, m_str):
        try:
            hour = int(h_str)
        except ValueError:
            Logger.log_error("Hour part of a reservation is not an integer. Reservation will be skipped")
            return None
        try:
            minute = int(m_str)
        except ValueError:
            Logger.log_error("Minute part of a reservation is not an integer. Reservation will be skipped")
            return None
        return QTime(hour, minute)
