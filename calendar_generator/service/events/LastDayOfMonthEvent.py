from calendar import monthrange
from datetime import date, timedelta
from .AbstractEvent import AbstractEvent
from .enums import Month, Weekday

class LastDayOfMonthEvent(AbstractEvent):
    def __init__(self, name: str, day: Weekday|int, month: Month|int):
        super().__init__(name)
        self.day = day
        self.month = month

    def get_date(self, year: int):
        month = self.month.value if isinstance(self.month, Month) else self.month
        day = self.day.value if isinstance(self.day, Weekday) else self.day

        return self.cached(
            [year, month, day], 
            lambda: self._get_date(year, month, day)
        )       
    
    def _get_date(self, year: int, month: int, day: int):
        lastDayInMonth = monthrange(year, month)[1]
        r = date(year, month, lastDayInMonth)
        while r.isoweekday() != day: r -= timedelta(days=1)
        return r
