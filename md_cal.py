from datetime import datetime
from itertools import chain
import argparse
import calendar
import locale
import sys

DAYS_PER_WEEK = 7
DAY_CHAR_WIDTH = 3

def get_days_num(month, year):
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

def get_days_dot(month, year):
    cal = calendar.Calendar()
    days = []
    week = [DAY_CHAR_WIDTH * ' ' for _ in range(DAYS_PER_WEEK)]

    for (day, weekday) in cal.itermonthdays2(year=year, month=month):
        if day == 0:
            continue
        week[weekday] = '*'.ljust(DAY_CHAR_WIDTH)
        if weekday == calendar.SUNDAY:
            days.append(week)
            week = [DAY_CHAR_WIDTH * ' ' for _ in range(DAYS_PER_WEEK)]
    if any(cell != DAY_CHAR_WIDTH * ' ' for cell in week):
        days.append(week)

    return days

def gen_markdown_cal(month, year, get_days=get_days_num):
    header = '# ' + locale.nl_langinfo(getattr(locale, f"MON_{month}")) + ' ' + str(year) + 2 * '\n'

    weekdays = [locale.nl_langinfo(getattr(locale, f'ABDAY_{i}')) for i in chain(range(2, DAYS_PER_WEEK + 1), [1])]
    weekdays = '| ' + ' | '.join(weekdays) + ' |' + '\n'

    sep = '| ' + ' | '.join([DAY_CHAR_WIDTH * '-' for _ in range (DAYS_PER_WEEK)]) + ' |' + '\n'

    days = ['| ' + ' | '.join(week) + ' |'  for week in get_days(month, year)]
    days = '\n'.join(days)

    cal = header + weekdays + sep + days

    return cal

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')

    parser = argparse.ArgumentParser(
            prog="md_cal",
            description="md_cal displays a calendar in the format of a markdown table",
    )
    parser.add_argument('month', type=int, nargs='?', default=datetime.now().month)
    parser.add_argument('year', type=int, nargs='?', default=datetime.now().year)
    parser.add_argument("-d", "--dots", action='store_true', help="display dots instead of day numbers")
    args = parser.parse_args()

    year = args.year
    month = args.month

    if args.dots:
        cal = gen_markdown_cal(month=month, year=year, get_days=get_days_dot)
    else:
        cal = gen_markdown_cal(month=month, year=year)

    print(cal)

