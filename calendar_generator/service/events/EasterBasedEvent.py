from calendar import monthrange
from datetime import date, timedelta
import math

from .AbstractEvent import AbstractEvent
from .enums import Weekday

class EasterBasedEvent(AbstractEvent):
    def __init__(self, name: str, offset: int = 0, baseIsFridayBefore: bool = False):
        super().__init__(name)
        self.offset = offset
        self.baseIsFridayBefore = baseIsFridayBefore

    def get_date(self, year: int):
    
        return self.cached(
            [year, self.offset, self.baseIsFridayBefore], 
            lambda: self._get_date(year, self.offset, self.baseIsFridayBefore)
        )
    
    def _get_date(self, Y: int, offset: int, baseIsFridayBefore: bool):
        # All calculations done on the basis of "Gauss Easter Algorithm"
        A = Y % 19
        B = Y % 4
        C = Y % 7
        
        P = math.floor(Y / 100)
        Q = math.floor((13 + 8 * P) / 25)
        M = (15 - Q + P - P // 4) % 30
        N = (4 + P - P // 4) % 7
        D = (19 * A + M) % 30
        E = (2 * B + 4 * C + 6 * D + N) % 7
        days = (22 + D + E)
    
        rYear = Y
        rMonth = -1
        rDay = -1

        if ((D == 29) and (E == 6)):
            # A corner case, when D is 29
            rMonth = 4; rDay = 19        
        elif ((D == 28) and (E == 6)):
            # Another corner case, when D is 28
            rMonth = 4; rDay = 18        
        else:            
            if (days > 31):
                # If days > 31, move to April, April = 4th Month
                rMonth = 4; rDay = days - 31
            else:                
                # Otherwise, stay on March, March = 3rd Month
                rMonth = 3; rDay = days

        r = date(rYear, rMonth, rDay)

        if baseIsFridayBefore:
            while r.isoweekday() != Weekday.FRIDAY.value: r -= timedelta(days=1)
            
        if offset:
            r += timedelta(days=offset)

        return r
