from datetime import date, timedelta
from typing import Generator

days = ['Week', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
months = ['januari', 'februari', 'maart', 'april', 'mei', 'juni',
          'juli', 'augustus', 'september', 'oktober', 'november', 'december']

class Cell:
    def __init__(self, value: str):
        self.value = "&nbsp;" if not value else value
    def __str__(self) -> str:
        return f"{type(self).__name__}: {self.value}"

class NumberCell(Cell):
    def __init__(self, value: int):
        super().__init__("" if value == 0 else str(value))

class HeaderCell(Cell): pass
class WeekCell(NumberCell): pass
class DayCell(NumberCell): 
    def __init__(self, value: int, d: date):
        super().__init__(value)
        self.year = d.year
        self.month = d.month
        self.day = d.day    
class InactiveDayCell(NumberCell): pass
    

class CalenderGenerator:
    def __init__(self, year, month):
        self.year = year
        self.month = month

    @property
    def label(self):
        m = self.month
        return f'{m}: {months[m-1].capitalize()}'
    
    def rows(self) -> Generator[Generator[Cell, any, any], any, any] :
        yield [HeaderCell(day) for day in days] + [HeaderCell("")]
        
        dd = date(self.year, self.month, 1)
        m = dd.month
        cal = dd.isocalendar()
        while cal.weekday != 1: #1 = maandag
            dd = dd + timedelta(days=-1)
            cal = dd.isocalendar()

        week = cal.week
        while True:   
           line = [ WeekCell(str(week)) ]
        
           while week == cal.week:      
              if dd.month != self.month:
                 line.append(InactiveDayCell(str(dd.day)))
              else:
                 line.append(DayCell(str(dd.day), dd))

              dd = dd + timedelta(days=1)
              cal = dd.isocalendar()
           line.append(DayCell("", dd))
           yield line
           week = cal.week
                
           if self.month != dd.month: 
              break



