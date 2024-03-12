from PySide6.QtCore import QTime, QDate

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

class Schedule:
    def __init__(self):
        self.data = {}

    def load_example_data(self):
        self.data = {
            QDate(2024, 4, 8): {
                "Мариана": {
                    TimeInterval(QTime(12, 0), QTime(13, 0)): "Иван",
                    TimeInterval(QTime(13, 50), QTime(14, 20)): "Борис",
                    TimeInterval(QTime(14, 0), QTime(15, 0)): "Мишо",
                    TimeInterval(QTime(15, 20), QTime(16, 0)): "Таня"
                },
                "Мери": {
                    TimeInterval(QTime(14, 0), QTime(14, 40)): "Станимир",
                    TimeInterval(QTime(15, 0), QTime(17, 0)): "Мария",
                },
                "Валя": {
                    TimeInterval(QTime(12, 30), QTime(13, 0)): "Пешо",
                    TimeInterval(QTime(13, 0), QTime(13, 45)): "Георги",
                    TimeInterval(QTime(14, 30), QTime(15, 30)): "Михаела",
                }
            },
            QDate(2024, 4, 9): {
                "Мариана": {
                    TimeInterval(QTime(9, 0), QTime(10, 30)): "Петър",
                    TimeInterval(QTime(16, 50), QTime(17, 20)): "Милена",
                },
                "Мери": {
                    TimeInterval(QTime(10, 0), QTime(11, 00)): "Димитър",
                    TimeInterval(QTime(11, 0), QTime(11, 30)): "Иван",
                    TimeInterval(QTime(12, 30), QTime(13, 30)): "Станислава",
                    TimeInterval(QTime(13, 30), QTime(15, 0)): "Петя",
                },
                "Валя": {
                    TimeInterval(QTime(11, 30), QTime(13, 0)): "Мариана",
                    TimeInterval(QTime(13, 40), QTime(14, 30)): "Георги",
                    TimeInterval(QTime(15, 0), QTime(16, 0)): "Дара",
                    TimeInterval(QTime(16, 30), QTime(18, 0)): "Дара",
                }
            },
        }

    def get_employees(self, date):
        return list(self.data[date].keys())
