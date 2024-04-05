from logger import Logger

class VouchersSoldHandler:
    def __init__(self, date, database):
        self.date = date
        self.database = database

        self.init_data()

    # Initializes the self.data dictionary with the organized vouchers sold
    def init_data(self):
        # Get vouchers for date and sort them by time
        vouchers = []
        for voucher in self.database.vouchers:
            if voucher.bought_on.date() == self.date:
                vouchers.append(voucher)
        vouchers = sorted(vouchers, key=lambda voucher : voucher.bought_on.time())
        employees = self.database.employees
        # Organize vouchers by employee and insert them in a dictionary with vrow keys to be used directly by a TableBase
        self.data = {}
        for employee in employees:
            self.data[employee.id] = {}
            vrow = 0
            for voucher in vouchers:
                if voucher.employee_id != employee.id:
                    continue
                self.data[employee.id][vrow] = voucher
                vrow += 1

    # Returns a map of vouchers for the given employee
    def get_vouchers_map(self, employee_id):
        return self.data[employee_id]
