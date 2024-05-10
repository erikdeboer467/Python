from datetime import date, timedelta
from .AbstractEvent import AbstractEvent
from .enums import Month, Weekday

class XedOccurrenceOfDayInMonthEvent(AbstractEvent):
    def __init__(self, name: str, occurance: int, weekday: Weekday|int, month: Month|int):
        super().__init__(name)
        self.occurance = occurance
        self.weekday = weekday
        self.month = month

    def get_date(self, year: int):
        weekday = self.weekday.value if isinstance(self.weekday, Weekday) else self.weekday
        month = self.month.value if isinstance(self.month, Month) else self.month

        return self.cached(
            [year, month, weekday, self.occurance], 
            lambda: self._get_date(year, self.occurance, weekday, month)
        )       


    def _get_date(self, year: int, occurance: int, weekday: int, month: int):
        r = date(year, month, 1)

        while True:
            if r.isoweekday() == weekday:
                occurance -= 1
                if occurance == 0: return r
            r += timedelta(days=1)

