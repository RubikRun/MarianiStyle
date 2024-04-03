from PySide2.QtWidgets import QMainWindow, QHeaderView
from ui.table_base import TableBase

from database.employee import Employee

def get_example_table():
    def employee_deleter_wrapper(employees):
        def employee_deleter(id):
            for idx, employee in enumerate(employees):
                if employee.id == id:
                    del employees[idx]
            print("employee_deleter() finished, now we have employees =", [employee.name for employee in employees])
        return employee_deleter

    def employee_updater_wrapper(employees):
        def employee_updater(id, col, str_val):
            updated = False
            for idx, employee in enumerate(employees):
                if employee.id == id:
                    if col == 1:
                        if len(str_val) >= 2:
                            employees[idx].name = str_val
                            updated = True
            print("employee_updater() finished, now we have employees =", [employee.name for employee in employees])
            return updated
        return employee_updater

    employees = [
        Employee(1, "Мариана"),
        Employee(2, "Мери"),
        Employee(3, "Валя")
    ]
    employees_map = {
        2: employees[0],
        4: employees[1],
        5: employees[2]
    }
    table = TableBase(
        8,
        [1, 3, 5, 2, 2, 1, 1, 1],
        2,
        ["ID", "Name"],
        [QHeaderView.ResizeToContents, QHeaderView.Stretch],
        employees_map,
        [
            lambda employee : str(employee.id),
            lambda employee : employee.name,
        ],
        employee_deleter_wrapper(employees),
        employee_updater_wrapper(employees)
    )

    return table

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мариани Стайл")

        self.table = get_example_table()

        self.setCentralWidget(self.table)
