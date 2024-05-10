# region csv format
# Subject,Start Date,End Date,All Day Event
# test1,12/15/2024,12/15/2024,True
# test2,12/25/2024,12/25/2024,True
# test3,12/30/2024,12/30/2024,True
# endregion

# create import file voor google calendar.

import os
from service.events.enums import Month, Weekday
from service.events.Events import Events

fs = [
    {
        "name": "Feestdag_vrij.csv",
        "events": [
            ("Feestdag (vrij) - 1ste Paasdag", Events.EasterBased("1ste Paasdag")),
            ("Feestdag (vrij) - 2de Paasdag", Events.EasterBased("1ste Paasdag", 1)),
            ("Feestdag (vrij) - Bevrijdingsdag", Events.MonthDay("Bevrijdingsdag", Month.MAY, 5, lambda d: d.year % 5 == 0)),
            ("Feestdag (vrij) - Hemelvaartsdag", Events.EasterBased("1ste Paasdag", 39)),
            ("Feestdag (vrij) - 1ste Pinksterdag", Events.EasterBased("1ste Pinksterdag", 49)),
            ("Feestdag (vrij) - 2de Pinksterdag", Events.EasterBased("2de Pinksterdag", 50)),
        ]
    },
    {
        "name": "Feestdag.csv",
        "events": [
            ("Feestdag (vrij) - Goede vrijdag", Events.EasterBased("Goede vrijdag", baseIsFridayBefore=True)),
        ]
    },
    {
        "name": "SpecialeDagen.csv",
        "events": [
            ("Speciale dagen - Moederdag", Events.XedOccurrenceOfDayInMonth("Moederdag", 2, Weekday.SUNDAY, Month.MAY)),
            ("Speciale dagen - Vaderdag", Events.XedOccurrenceOfDayInMonth("Vaderdag", 3, Weekday.SUNDAY, Month.JUNE)),
            ("Speciale dagen - Begin zomertijd (klok +1 uur)", Events.LastDayOfMonth('Begin zomertijd (klok +1 uur)', Weekday.SUNDAY, Month.MARCH)),
            ("Speciale dagen - Begin wintertijd (klok -1 uur)", Events.LastDayOfMonth('Begin wintertijd (klok -1 uur)', Weekday.SUNDAY, Month.OCTOBER)),
        ]
    },
    {
        "name": "NietTriviaal.csv",
        "events": [
            ("Niet triviaal - Carnaval (3 dagen)", Events.EasterBased("Carnaval (3 dagen)", -49)),
            ("Niet triviaal - Prinsjesdag", Events.XedOccurrenceOfDayInMonth("Prinsjesdag", 3, Weekday.TUESDAY, Month.SEPTEMBER)),
        ]
    }
]

for f in fs:
    print(f["name"])
    with open(os.path.join('temp', f["name"]), 'w') as ff:
        ff.write(f"Subject,Start Date,End Date,All Day Event\n")
        for y in range(2024, 2074+1):
            for e in f["events"]:    
                dd = e[1].get_date(y)
                if e[1].isValid(dd):
                    dt = dd.strftime("%m/%d/%Y")    
                    ff.write(f"{e[0]},{dt},{dt},True\n")
    
    

