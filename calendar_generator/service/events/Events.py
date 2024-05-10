from datetime import date
from typing import Callable
from .EasterBasedEvent import EasterBasedEvent
from .enums import Month, Weekday
from .MonthDayEvent import MonthDayEvent
from .LastDayOfMonthEvent import LastDayOfMonthEvent
from .WeekDayInMonthEvent import XedOccurrenceOfDayInMonthEvent

class Events:

    @staticmethod
    def MonthDay(name: str, month: Month|int, day: int, isValid: Callable[[date], bool] = lambda d: True):
        return MonthDayEvent(name, month, day, isValid)

    @staticmethod
    def LastDayOfMonth(name: str, day: Weekday|int, month: Month|int):
        return LastDayOfMonthEvent(name, day, month)

    @staticmethod
    def XedOccurrenceOfDayInMonth(name: str, occurance: int, weekday: Weekday|int, month: Month|int):
        return XedOccurrenceOfDayInMonthEvent(name, occurance, weekday, month)

    @staticmethod
    def EasterBased(name: str, offset: int = 0, baseIsFridayBefore: bool = False):
        return EasterBasedEvent(name, offset, baseIsFridayBefore)
