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
