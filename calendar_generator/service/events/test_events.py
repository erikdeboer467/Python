from datetime import date
from unittest import TestCase, main
from calendar_events import CalendarEvents
from Events import Events
from enums import Month, Weekday

class ExtTestCase(TestCase):
    def assertDate(self, first: date, second: date) -> None:
        self.assertEqual(first.year, second.year)
        self.assertEqual(first.day, second.day)
        self.assertEqual(first.month, second.month)


class TestEvent(ExtTestCase):
    
    def test_TestMonthEnum(self):
        a = Month(3)        

        self.assertEqual(a, Month.MARCH)
        self.assertEqual(a.value, 3)    
        self.assertEqual(a.name, 'MARCH')  
        self.assertEqual(Month.MARCH, Month.from_date(date(2024,3,19)))

    def test_WeekdayEnum(self):
        a = Weekday(1)
        self.assertEqual(a, Weekday.MONDAY)
        self.assertEqual(a.value, 1)    
        self.assertEqual(a.name, 'MONDAY')  
        self.assertEqual(Weekday.TUESDAY, Weekday.from_date(date(2024,1,30)))

    def test_DayMonthEvent(self):
        event1 = Events.MonthDay('test', 3, 19)        
        self.assertEqual('test', event1.name)
        self.assertDate(            
            event1.get_date(2024),
            date(2024, 3, 19)
        )

        event2 = Events.MonthDay('test',  Month.MARCH, 19)
        self.assertDate(
            event2.get_date(2024),
            date(2024, 3, 19)
        )

        self.assertTrue(event2.get_date(2024).__hash__ == event2.get_date(2024).__hash__)

    def test_LastDayOfMonthEvent(self):
        event1 = Events.LastDayOfMonth("Begin zomertijd", Weekday.SUNDAY, Month.MARCH)
        d1 = event1.get_date(2024)
        self.assertDate(d1, date(2024, 3, 31))

        event2 = Events.LastDayOfMonth("Begin wintertijd", Weekday.SUNDAY, Month.OCTOBER)
        d2 = event2.get_date(2024)
        self.assertDate(d2, date(2024, 10, 27))

        d3 = event2.get_date(2024)
        self.assertDate(d3, date(2024, 10, 27))

        self.assertTrue(d2.__hash__ == d3.__hash__)

    def test_XedOccurrenceOfDayInMonth(self):
        e1 = Events.XedOccurrenceOfDayInMonth("Moederdag", 2, Weekday.SUNDAY, Month.MAY)
        d1 = e1.get_date(2024)
        self.assertDate(d1, date(2024, 5, 12))
        self.assertEqual(d1.isoweekday(), Weekday.SUNDAY.value)

        e2 = Events.XedOccurrenceOfDayInMonth("Vaderdag", 3, Weekday.SUNDAY, Month.JUNE)
        self.assertDate(e2.get_date(2024), date(2024, 6, 16))

        e3 = Events.XedOccurrenceOfDayInMonth("Prinsjesdag", 3, Weekday.TUESDAY, Month.SEPTEMBER)
        self.assertDate(e3.get_date(2024), date(2024, 9, 17))

    def test_EasterBased(self):
        self.assertDate(Events.EasterBased('1ste paasdag').get_date(2024), date(2024, 3, 31))
        self.assertDate(Events.EasterBased('1ste paasdag').get_date(2025), date(2025, 4, 20))
        self.assertDate(Events.EasterBased('1ste paasdag').get_date(2030), date(2030, 4, 21))

        self.assertDate(Events.EasterBased('1ste paasdag').get_date(2285), date(2285, 3, 22))
        self.assertDate(Events.EasterBased('2de paasdag', 1).get_date(2285), date(2285, 3, 23))
        self.assertDate(Events.EasterBased('Goede vrijdag', baseIsFridayBefore=True).get_date(2285), date(2285, 3, 20))
        self.assertTrue(Weekday.FRIDAY.value == date(2285, 3, 20).isoweekday())

    # only visual inspected
    def test_CalendarEvents(self):       
        c = CalendarEvents()
        events = c.getEvents(2024)

        for month, dayDic in events.items():
            print(month)
            for day, dayEvents in dayDic.items():
                for ee in dayEvents:
                    print('> ', day, ' * ', ee.color, '-', ee.name)
                

