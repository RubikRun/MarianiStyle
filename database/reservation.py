class Reservation:
    def __init__(self, id, employee_id, client_id, date_time, procedure, packet_instance_id, percent, kasa, bg_colors, fg_colors):
        self.id = id
        self.employee_id = employee_id
        self.client_id = client_id
        self.date_time = date_time
        self.procedure = procedure
        self.packet_instance_id = packet_instance_id
        self.percent = percent
        self.kasa = kasa
        self.bg_colors = bg_colors
        self.fg_colors = fg_colors
