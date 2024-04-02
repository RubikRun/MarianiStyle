from database.data_io import DataIO
from logger import Logger

class Employee:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def deserialize(decl):
        data = DataIO.parse_declaration(decl, "is")

        if data[0] is None or data[0] < 1:
            Logger.log_error("Employee has invalid ID. It will be created with ID = 1")
            data[0] = 1

        employee = Employee(data[0], data[1])
        return employee

    def serialize(self):
        decl = DataIO.create_declaration([self.id, self.name], "is")
        return decl