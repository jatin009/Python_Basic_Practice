import datetime
import calendar
import enum


class DateFormat(enum.Enum):
    YEAR_MON_DAY = 1,
    DAY_MON_YEAR = 2,
    MON_YEAR = 3


def date_input(date_str, date_enum = DateFormat.DAY_MON_YEAR):
    try:
        day, month, year = 0, 0, 0
        if date_enum == DateFormat.YEAR_MON_DAY:
            year, month, day = map(int, date_str.split('-'))
        else:
            day, month, year = map(int, date_str.split('/'))
        date_obj = datetime.date(year, month, day)
        if date_obj > datetime.date.today():
            raise ValueError
        
    except ValueError:
        print("Invalid date provided.")
        
    else:
        return date_obj


def date_conversion(date_enum, date_obj):
    if date_enum == DateFormat.YEAR_MON_DAY:
        return date_obj.strftime("%Y-%m-%d")
    elif date_enum == DateFormat.DAY_MON_YEAR:
        return date_obj.strftime("%d/%m/%Y")
    elif date_enum == DateFormat.MON_YEAR:
        return date_obj.strftime("%b, %Y")


def add_month(date1, months):
    """ Add months to a date """
    new_year = months//12 + date1.year
    new_month = months%12 + date1.month

    if new_month > 12:
        new_year += 1
        new_month -= 12

    last_day_of_month = calendar.monthrange(new_year, new_month)[1]
    new_day = min(date1.day, last_day_of_month)
        
    return datetime.date(new_year, new_month, new_day)


def month_diff(date1, date2):
    """ To find the difference between two dates in terms of months """
    return (date1.year - date2.year)*12 + (date1.month - date2.month)
