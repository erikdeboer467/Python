from datetime import date, timedelta
from typing import Callable
from .AbstractEvent import AbstractEvent
from .enums import Month, Weekday

class MonthDayEvent(AbstractEvent):
    def __init__(self, name: str, month: Month|int, day: int, isValid: Callable[[date], bool] = lambda d: True):
        super().__init__(name, isValid)
        self.month = month
        self.day = day

    def get_date(self, year: int):
        month = self.month.value if isinstance(self.month, Month) else self.month        
        return self.cached(
            [year, month, self.day], 
            lambda: self._get_date(year, month, self.day)
        )

    def _get_date(self, year: int, month: int, day: int):        
        return date(year, month, day)
    