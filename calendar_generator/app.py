import subprocess, sys

from calendergenerator import CalenderGenerator, DayCell, HeaderCell, InactiveDayCell, WeekCell
from service.events.calendar_events import CalendarEvents

year = 2025
#month = 4

content = ''
for month in range(1,12+1):

    calendar = CalenderGenerator(year, month)
    events = CalendarEvents().getEvents(year)

    cellBase = lambda text, style, center = True: f'''
    <td style='border-style:solid;border-color:#A3A3A3;border-width:1pt;vertical-align:top;padding:4pt 4pt 4pt 4pt;width:.6673in;{style}'>
    <p style='margin:0in;font-family:Calibri;font-size:10.0pt;{"text-align:center" if center else ""}' lang=nl>{text}</p>
    </td>
    '''

    cellbgBold = lambda bgColor, text: cellBase(text, f'background-color:{bgColor};font-weight:bold')
    cellbg = lambda bgColor, text: cellBase(text, f'background-color:{bgColor}')
    cellfg = lambda fgColor, text: cellBase(text, f'color:{fgColor}')
    # <p style='margin:0in;font-family:Calibri;font-size:11.0pt;color:#F2F2F2'
    # lang=en-US><!--StartFragment-->test<!--EndFragment--></p>

    def cell(text: str, bgColor: str, eventsForWeek: list[str]):
        if text == "&nbsp;":
            return cellBase('<br>'.join(eventsForWeek), '', False)
        else:
            if bgColor:
                return cellbg(bgColor, text)                       
            return cellBase(text, '')

    rowsContent = ''
    for row in calendar.rows():
        rowsContent += "<tr>"

        eventsForWeek = []
        for cel in row:
            if isinstance(cel, HeaderCell):
                rowsContent += cellbgBold('#E0E0E0', cel.value)
            elif isinstance(cel, WeekCell):
                rowsContent += cellbgBold('#F0F0F0', cel.value)
            elif isinstance(cel, DayCell):
                if cel.value != "&nbsp;":
                    color = None
                    if cel.month in events and cel.day in events[cel.month]:
                        x = events[cel.month][cel.day]
                        color = x[0].color
                        for e in x: eventsForWeek.append(f'{cel.day}: {e.name}')

                rowsContent += cell(cel.value, color, eventsForWeek)
            elif isinstance(cel, InactiveDayCell):
                rowsContent += cellfg('#BFBFBF', cel.value)
            else:
                rowsContent += '<td>.</td>' 
        
        rowsContent += "</tr>"


    content += f'''
    <p style='margin:0in'>{calendar.label}</p>
    <table border=1 cellpadding=0 cellspacing=0 valign=top style='border-collapse:collapse'>
    {rowsContent}
    </table>                 
    '''

# region wrap and save and execute
def crlf(v: str, **kwargs: any): return '\r\n'.join(v.split('\n'))

html = crlf(f'''
<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:dt="uuid:C2F41010-65B3-11d1-A29F-00AA00C14882" xmlns="http://www.w3.org/TR/REC-html40">
<head>
   <meta http-equiv=Content-Type content="text/html; charset=utf-8">
   <meta name=ProgId content=OneNote.File>
   <meta name=Generator content="Microsoft OneNote 15">
</head>   
   <body lang=en-NL style='font-family:Calibri;font-size:11.0pt'>
      <!--StartFragment-->
      @@@{content}@!@      
      <!--EndFragment-->
   </body>
</html>
''').strip()

offset = 105+2 #wellicht + 2 klopt niet meer vanweg strip
startHtml = offset + 0
startFragment = offset + html.find("@@@"); html = html.replace("@@@", "") 
endFragment = offset + html.find("@!@"); html = html.replace("@!@", "")
endHtml = offset + len(html)+1
header = f'''
Version:1.0
StartHTML:{startHtml:010}
EndHTML:{endHtml:010}
StartFragment:{startFragment:010}
EndFragment:{endFragment:010}
'''.strip()
meta = crlf(header) + '\r\n' + '\r\n'

with open('test.htm', 'wb') as f:
    f.write((meta + html).encode())
# print(html)

p = subprocess.Popen(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "D:\Data\Documents\_DEVELOPMENT\Python\set.ps1"], stdout=sys.stdout)
p.communicate()
# endregion




