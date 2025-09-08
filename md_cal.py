from datetime import datetime
from itertools import chain
import calendar
import locale
import sys

DAYS_PER_WEEK = 7
DAY_CHAR_WIDTH = 3

def get_days_arr(month, year):
    cal = calendar.Calendar()
    days = []
    week = [DAY_CHAR_WIDTH * ' ' for _ in range(DAYS_PER_WEEK)]

    for (day, weekday) in cal.itermonthdays2(year=year, month=month):
        if day == 0:
            continue
        week[weekday] = str(day).ljust(DAY_CHAR_WIDTH)
        if weekday == calendar.SUNDAY:
            days.append(week)
            week = [DAY_CHAR_WIDTH * ' ' for _ in range(DAYS_PER_WEEK)]
    if any(cell != DAY_CHAR_WIDTH * ' ' for cell in week):
        days.append(week)

    return days

def gen_markdown_cal(month=datetime.now().month, year=datetime.now().year):
    header = '# ' + locale.nl_langinfo(getattr(locale, f"MON_{month}")) + ' ' + str(year) + 2 * '\n'

    weekdays = [locale.nl_langinfo(getattr(locale, f'ABDAY_{i}')) for i in chain(range(2, DAYS_PER_WEEK + 1), [1])]
    weekdays = '| ' + ' | '.join(weekdays) + ' |' + '\n'

    sep = '| ' + ' | '.join([DAY_CHAR_WIDTH * '-' for _ in range (DAYS_PER_WEEK)]) + ' |' + '\n'

    days = ['| ' + ' | '.join(week) + ' |'  for week in get_days_arr(month, year)]
    days = '\n'.join(days)

    cal = header + weekdays + sep + days

    return cal

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    argv = sys.argv

    if len(argv) == 1:
        cal = gen_markdown_cal()
    elif len(argv) == 2:
        cal = gen_markdown_cal(month=int(argv[1]))
    elif len(argv) == 3:
        cal = gen_markdown_cal(month=int(argv[1]), year=int(argv[2]))
    else:
        print("usage: md_cal [[month] year]")
        sys.exit(1)
    print(cal)

