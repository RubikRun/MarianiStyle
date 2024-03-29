from logger import Logger
from PySide2.QtCore import QDate, QTime
from PySide2.QtGui import QColor

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
    def __init__(self, employee, date, time_interval, client, procedure, percent, kasa, colors = [None, None, None, None, None, None, None, None]):
        self.employee = employee
        self.date = date
        self.time_interval = time_interval
        self.client = client
        self.procedure = procedure
        self.percent = percent
        self.kasa = kasa
        self.colors = colors

    # Deserializes a reservation from a declaration string. Returns the reservation.
    def deserialize(decl, clients):
        if decl is None or decl == "":
            Logger.log_error("Reservation declaration is empty. Reservation will be skipped")
            return None
        decl_parts = decl.split(';')
        if len(decl_parts) not in [12, 16, 20, 24, 28, 32, 36, 40, 44]:
            Logger.log_error("Reservation declaration is invalid, should have 12/16/20/24/28/32/36/40/44 parts. Reservation will be skipped")
            return None
        employee = decl_parts[0].strip()
        if employee == "":
            Logger.log_error("Employee part of a reservation is empty. Reservation will be skipped")
            return None
        date = Reservation.deserialize_date_parts(decl_parts[1].strip(), decl_parts[2].strip(), decl_parts[3].strip())
        if date is None:
            return None
        time_begin = Reservation.deserialize_time(decl_parts[4].strip(), decl_parts[5].strip())
        if time_begin is None:
            return None
        time_end = Reservation.deserialize_time(decl_parts[6].strip(), decl_parts[7].strip())
        if time_end is None:
            return None
        client_name = decl_parts[8].strip()
        if client_name == "":
            Logger.log_error("Client part of a reservation is empty. Reservation will be skipped")
            return None
        client_exists = False
        for cl in clients:
            if client_name == cl.name:
                client = cl
                client_exists = True
                break
        if not client_exists:
            Logger.log_error("Client in reservation does not exist. Reservation will be skipped")
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

        colors = [None] * 8
        for col in range(8):
            color_part_idx = 12 + 4 * col
            if color_part_idx >= len(decl_parts):
                break
            color = Reservation.deserialize_color(decl_parts[color_part_idx], decl_parts[color_part_idx+1], decl_parts[color_part_idx+2], decl_parts[color_part_idx+3])
            colors[col] = color

        reservation = Reservation(employee, date, TimeInterval(time_begin, time_end), client, procedure, percent, kasa, colors)
        return reservation

    def serialize(self):
        s = ""
        s += self.employee + ";"
        s += str(self.date.year()) + ";"
        s += str(self.date.month()) + ";"
        s += str(self.date.day()) + ";"
        s += str(self.time_interval.time_begin.hour()) + ";"
        s += str(self.time_interval.time_begin.minute()) + ";"
        s += str(self.time_interval.time_end.hour()) + ";"
        s += str(self.time_interval.time_end.minute()) + ";"
        s += self.client.name + ";"
        s += self.procedure + ";"
        s += str(self.percent) + ";"
        s += str(self.kasa)
        for color in self.colors:
            if color is None:
                s += ";None;None;None;None"
            else:
                s += ";" + str(color.red())
                s += ";" + str(color.green())
                s += ";" + str(color.blue())
                s += ";" + str(color.alpha())

        return s

    def deserialize_color(s0, s1, s2, s3):
        if s0 == "None" or s1 == "None" or s2 == "None" or s3 == "None":
            return None
        color = None
        try:
            red = int(s0)
            try:
                green = int(s1)
                try:
                    blue = int(s2)
                    try:
                        alpha = int(s3)
                        color = QColor(red, green, blue, alpha)
                    except ValueError:
                        Logger.log_error("Alpha part of a reservation is not an integer. Color will be skipped")
                except ValueError:
                    Logger.log_error("Blue part of a reservation is not an integer. Color will be skipped")
            except ValueError:
                Logger.log_error("Green part of a reservation is not an integer. Color will be skipped")
        except ValueError:
            Logger.log_error("Red part of a reservation is not an integer. Color will be skipped")
        return color

    def deserialize_date(s):
        s_parts = s.split(";")
        if len(s_parts) != 3:
            Logger.log_error("Invalid date. Date should have exactly 3 parts")
            return None
        return Reservation.deserialize_date_parts(s_parts[0].strip(), s_parts[1].strip(), s_parts[2].strip())

    def deserialize_date_parts(y_str, m_str, d_str):
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

    def deserialize_time(h_str, m_str):
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
