from datetime import date
from .AbstractEvent import AbstractEvent
from .Events import Events
from .enums import Month, Weekday

class EventGroup:
	def __init__(self, name: str, color: str, events: list[AbstractEvent]):
		self.name = name
		self.color = color
		self.events = events
class EventDay:
	def __init__(self, name: str, color: str):
		self.name = name
		self.color = color

class CalendarEvents:
	def getEvents(self, year: int): # filter on month?
		r: dict[int, dict[int, list[EventDay]]] = {}

		for g in self.eventGroups:			
			for e in g.events:
				d: date = e.get_date(year)
				if not e.isValid(d): continue
				if not d.month in r: r[d.month] = {}
				if not d.day in r[d.month]: r[d.month][d.day] = []

				lbl = '';
				if g.name:
					lbl += g.name
				if e.name:
					if g.name: lbl += " - "
					lbl += e.name

				r[d.month][d.day].append(EventDay(lbl, g.color))
				# print(f'{g.name} - {e.name}')

		return r
	
 	# https://www.w3schools.com/colors/colors_groups.asp

	def __init__(self):
		self.eventGroups = [
			EventGroup("Verjaardag", "Pink", [
				Events.MonthDay("Name", Month.SEPTEMBER, 9),
				# ...
			]),
			EventGroup("Trouwdag", "LightSalmon", [
				Events.MonthDay("Papa en Mama (1969)", Month.JUNE, 20)
			]),
			EventGroup("Feestdag (vrij)", "LimeGreen", [
				Events.MonthDay("Nieuwjaarsdag", Month.JANUARY, 1),
				Events.EasterBased("1ste Paasdag"),
				Events.EasterBased("2de Paasdag", 1),				
				Events.MonthDay("Bevrijdingsdag", Month.MAY, 5, lambda d: d.year % 5 == 0), #enkel in lustrumjaren
				Events.MonthDay("Koningsdag", Month.APRIL, 27),
				Events.EasterBased("Hemelvaartsdag", 39),
				Events.EasterBased("1ste Pinksterdag", 49),
				Events.EasterBased("2de Pinksterdag", 50),
				Events.MonthDay("1ste Kerstdag", Month.DECEMBER, 25),
				Events.MonthDay("2de Kerstdag", Month.DECEMBER, 26)
			]),
			EventGroup("Feestdag", "PaleTurquoise", [
				Events.MonthDay("Bevrijdingsdag", Month.MAY, 5, lambda d: d.year % 5 != 0),
				Events.EasterBased("Goede vrijdag", baseIsFridayBefore=True),
				Events.MonthDay("Sint Maarten", Month.NOVEMBER, 11),
				Events.MonthDay("Sinterklaasavond", Month.DECEMBER, 5),
				Events.MonthDay("Kerstavond", Month.DECEMBER, 24),
				Events.MonthDay("Oudejaarsavond", Month.DECEMBER, 31)
			]),
			EventGroup("", "DodgerBlue", [
				Events.MonthDay("Valentijnsdag", Month.FEBRUARY, 14),
				Events.XedOccurrenceOfDayInMonth("Moederdag", 2, Weekday.SUNDAY, Month.MAY),
				Events.XedOccurrenceOfDayInMonth("Vaderdag", 3, Weekday.SUNDAY, Month.JUNE),
				Events.MonthDay("1 aprildag", Month.APRIL, 1),
				Events.MonthDay("Koninkrijksdag", Month.DECEMBER, 15),
				Events.EasterBased("Carnaval (3 dagen)", -49),
				Events.XedOccurrenceOfDayInMonth("Prinsjesdag", 3, Weekday.TUESDAY, Month.SEPTEMBER),
				Events.LastDayOfMonth('Begin zomertijd (klok +1 uur)', Weekday.SUNDAY, Month.MARCH),
				Events.LastDayOfMonth('Begin wintertijd (klok -1 uur)', Weekday.SUNDAY, Month.OCTOBER)
			]),
			EventGroup("Kofferbakmarkt (2024)", "Chocolate", [ # https://www.kofferbakmarktwijkaanzee.nl/
				Events.MonthDay("", Month.APRIL, 14),
				Events.MonthDay("", Month.MAY, 12),
				Events.MonthDay("", Month.JUNE, 9),
				Events.MonthDay("", Month.JULY, 14),
				Events.MonthDay("", Month.AUGUST, 11),
				Events.MonthDay("", Month.SEPTEMBER, 8),
				Events.MonthDay("", Month.OCTOBER, 13)				
			])
		]



