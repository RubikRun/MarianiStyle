from PySide6.QtCore import QTime, QDate
from reservation import Reservation, TimeInterval

class Schedule:
    def __init__(self):
        self.data = {}

    def load_example_data(self):
        self.data = {
            QDate(2024, 4, 8): {
                "Мариана": [
                    Reservation("Мариана", QDate(2024, 4, 8), TimeInterval(QTime(12, 0), QTime(13, 0)), "Иван", "Масаж", 25, 0),
                    Reservation("Мариана", QDate(2024, 4, 8), TimeInterval(QTime(13, 50), QTime(14, 20)), "Борис", "Масаж", 15, 0),
                    Reservation("Мариана", QDate(2024, 4, 8), TimeInterval(QTime(14, 0), QTime(15, 0)), "Мишо", "Подстригване", 15, 75),
                    Reservation("Мариана", QDate(2024, 4, 8), TimeInterval(QTime(15, 20), QTime(16, 0)), "Таня", "Педикюр", 20, 0)
                ],
                "Мери": [
                    Reservation("Мери", QDate(2024, 4, 8), TimeInterval(QTime(14, 0), QTime(14, 40)), "Станимир", "Масаж", 25, 100),
                    Reservation("Мери", QDate(2024, 4, 8), TimeInterval(QTime(15, 0), QTime(17, 0)), "Мария", "Педикюр", 25, 0)
                ],
                "Валя": [
                    Reservation("Валя", QDate(2024, 4, 8), TimeInterval(QTime(12, 30), QTime(13, 0)), "Пешо", "Масаж", 25, 100),
                    Reservation("Валя", QDate(2024, 4, 8), TimeInterval(QTime(13, 0), QTime(13, 45)), "Георги", "Маникюр", 15, 0),
                    Reservation("Валя", QDate(2024, 4, 8), TimeInterval(QTime(14, 30), QTime(15, 30)), "Михаела", "Маникюр", 35, 0)
                ]
            },
            QDate(2024, 4, 9): {
                "Мариана": [
                    Reservation("Мариана", QDate(2024, 4, 9), TimeInterval(QTime(9, 0), QTime(10, 30)), "Петър", "Масаж", 25, 0),
                    Reservation("Мариана", QDate(2024, 4, 9), TimeInterval(QTime(16, 50), QTime(17, 20)), "Милена", "Маникюр", 35, 130)
                ],
                "Мери": [
                    Reservation("Мери", QDate(2024, 4, 9), TimeInterval(QTime(10, 0), QTime(11, 00)), "Димитър", "Подстригване", 15, 0),
                    Reservation("Мери", QDate(2024, 4, 9), TimeInterval(QTime(11, 0), QTime(11, 30)), "Иван", "Масаж", 25, 75),
                    Reservation("Мери", QDate(2024, 4, 9), TimeInterval(QTime(12, 30), QTime(13, 30)), "Станислава", "Маникюр", 15, 0),
                    Reservation("Мери", QDate(2024, 4, 9), TimeInterval(QTime(13, 30), QTime(15, 0)), "Петя", "Педикюр", 25, 0)
                ],
                "Валя": [
                    Reservation("Валя", QDate(2024, 4, 9), TimeInterval(QTime(11, 30), QTime(13, 0)), "Мариана", "Масаж", 25, 0),
                    Reservation("Валя", QDate(2024, 4, 9), TimeInterval(QTime(13, 40), QTime(14, 30)), "Георги", "Масаж", 35, 100),
                    Reservation("Валя", QDate(2024, 4, 9), TimeInterval(QTime(15, 0), QTime(16, 0)), "Дара", "Маникюр", 15, 0),
                    Reservation("Валя", QDate(2024, 4, 9), TimeInterval(QTime(16, 30), QTime(18, 0)), "Дара", "Масаж", 35, 0)
                ]
            },
        }

    def add_reservation(self, reservation):
        self.data[reservation.date][reservation.employee].append(reservation)

    def get_employees(self, date):
        return list(self.data[date].keys())
