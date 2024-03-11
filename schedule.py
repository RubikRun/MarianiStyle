from PySide6.QtCore import QTime, QDate
from reservation import Reservation

class Schedule:
    def __init__(self):
        self.data = {}

    def load_example_data(self):
        self.data = {
            QDate(2024, 4, 8): {
                12: [Reservation("Иван", QTime(12, 0), QTime(13, 0)), None, Reservation("Пешо", QTime(12, 30), QTime(13, 0))],
                13: [Reservation("Борис", QTime(13, 50), QTime(14, 20)), None, Reservation("Пешо", QTime(13, 0), QTime(13, 45))],
                14: [Reservation("Мишо", QTime(14, 0), QTime(15, 0)), Reservation("Станимир", QTime(14, 0), QTime(14, 40)), Reservation("Георги", QTime(14, 30), QTime(15, 30))],
                15: [Reservation("Таня", QTime(15, 20), QTime(16, 0)), Reservation("Мария", QTime(15, 0), QTime(17, 0)), None],
                16: [None, None, Reservation("Спас", QTime(16, 0), QTime(17, 0))]
            },
            QDate(2024, 4, 9): {
                12: [Reservation("Зорница", QTime(12, 10), QTime(13, 0)), None, None],
                13: [Reservation("Иван", QTime(13, 20), QTime(14, 0)), None, Reservation("Милена", QTime(13, 0), QTime(13, 30))],
                14: [None, Reservation("Станимир", QTime(14, 0), QTime(14, 40)), Reservation("Илия", QTime(14, 10), QTime(15, 30))],
                15: [None, Reservation("Мария", QTime(15, 0), QTime(17, 0)), None],
                16: [Reservation("Пешо", QTime(12, 30), QTime(13, 0)), None, Reservation("Лъчезар", QTime(16, 30), QTime(17, 0))]
            }
        }
