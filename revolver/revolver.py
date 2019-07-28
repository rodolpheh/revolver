import metric_time as mt
import datetime as dt
from dateutil.parser import isoparse
import pytz
import math

# Year I started in 1792 so the year 0 is 1791
# Adding 10000 to make the year in Holocene time
year_offset = 11791


class Revolver(object):

    class RepublicanDate(object):

        def __init__(self, year, month, day, week_day):
            self.year = year
            self.month = month
            self.day = day
            self.week_day = week_day

        def remove_one_day(self, year_is_leap):
            self.day -= 1
            if self.day == 0:
                self.day = 30
                self.month -= 1
            if self.month == 0:
                self.year -= 1
                self.month = 13
                self.day = 6 if year_is_leap else 5

        def __str__(self):
            return "{:02d}-{:02d}-{}".format(self.day, self.month, self.year)

    class MetricTime(object):

        def __init__(self, hour, minute):
            self.hour = hour
            self.minute = minute

    def __init__(
            self, year, month, day, day_of_the_week,
            hour, minute, *args, **kwargs):
        self.year = year
        self.month = month
        self.day = day
        self.day_of_the_week = day_of_the_week

        self.hour = hour
        self.minute = minute

        self.republican_date = None

    @property
    def yearly(self):
        return str(self.year)

    @property
    def monthly(self):
        return "{}.{:02d}".format(self.year, self.month)

    @property
    def daily(self):
        return "{}.{:02d}.{:02d}".format(self.year, self.month, self.day)

    @property
    def hourly(self):
        return "{}.{:02d}.{:02d}-{}{:02d}".format(
            self.year, self.month, self.day, self.hour, self.minute)

    @property
    def republican_year(self):
        return self.year - year_offset

    @property
    def republican_month(self):
        return (None if self.month is None else
                mt.RepublicanCalendar.MONTHS[self.month - 1])

    def __str__(self):
        return self.hourly

    def __repr__(self):
        return ("Revolver(year={}, month={}, day={}, hour={}, minute={})"
                .format(self.year, self.month, self.day,
                        self.hour, self.minute))

    @staticmethod
    def from_iso_str(date_str):
        iso_date = isoparse(date_str)
        return Revolver.from_iso(iso_date)

    @staticmethod
    def from_iso(iso_date):
        if (iso_date.tzinfo is None
                or iso_date.tzinfo.utcoffset(iso_date) is None):
            iso_date = iso_date.astimezone(pytz.timezone('UTC'))
        elif iso_date.tzinfo.utcoffset(iso_date) is not None:
            iso_date -= iso_date.tzinfo.utcoffset(iso_date)
        # else:
        #     iso_date = iso_date.astimezone(pytz.timezone('UTC'))

        time = mt.DecimalTime().decimal_time(iso_date)
        date = mt.RepublicanCalendar().republican_date(iso_date)

        # The year returned by metric_time is given as a float with the
        # year I starting at 0
        print(date.year)
        year = math.ceil(date.year) + year_offset

        # The day returned by metric_time start by the index 0
        day = date.day + 1

        if date.month is not None:
            month = (mt.RepublicanCalendar().MONTHS.index(date.month) + 1)
        else:
            month = None

        revolver = Revolver(
            year, month, day, date.day_of_the_week,
            time.hours, time.minutes)
        return revolver

    @staticmethod
    def now():
        now = dt.datetime.now(pytz.timezone('UTC'))
        return Revolver.from_iso(now)

    @property
    def iso_date(self):
        republican_year = self.year - year_offset
        year = self.year - year_offset + 1792

        # Calculations source :
        # https://fr.wikipedia.org/wiki/Concordance_des_dates_des_calendriers_r%C3%A9publicain_et_gr%C3%A9gorien

        temp_date = dt.datetime(
            year=year, month=9, day=21, tzinfo=dt.timezone.utc)

        # If the date is between Ventose 1st and Nivose 11th, subtract one year
        if self.month < 4 or (self.month == 4 and self.day <= 11):
            temp_date.year -= 1

            # If the year is a multiple of 4, add a day
            if republican_year % 4 == 0:
                temp_date += dt.timedelta(days=1)

        time_since_sans_culottides = (self.month - 1) * 30 + (self.day - 1)

        temp_date += dt.timedelta(days=time_since_sans_culottides)

        for century in range(18, int(temp_date.year / 100)):
            if century % 4 == 0:
                continue
            if temp_date > dt.datetime(
                    year=temp_date.year, month=2, day=28,
                    tzinfo=dt.timezone.utc):
                temp_date += dt.timedelta(days=1)

        # Compute the time (accurate to 1 minute because we don't keep the
        # seconds in the format)
        minutes = (self.hour * 2.4 * 60) + (self.minute * 1.44)
        hour = int(minutes / 60)
        minutes = int(minutes) % 60
        date = dt.datetime(
            year=year, month=temp_date.month, day=temp_date.day,
            hour=hour, minute=minutes, tzinfo=dt.timezone.utc)
        return date.isoformat()

    @staticmethod
    def iso_to_republican(date):
        # Remove 1792 to the temporary year
        year = date.year - 1792

        # In the republican calendar (Romme), leap years are multiple of 4
        republican_leap_year = (
            (year + 1) % 4 == 0 and (year + 1) != 0)
        previous_year_is_leap = (
            (year) % 4 == 0 and (year) != 0)

        new_republican_year = dt.datetime(
            date.year, 9, 23 if republican_leap_year else 22, 0, 0, 0,
            tzinfo=dt.timezone.utc)

        if date >= new_republican_year:
        #if date >= dt.datetime(date.year, 9, 22, tzinfo=dt.timezone.utc):
            year += 1
            # new_republican_year = dt.datetime(
            #     date.year, 9, 23 if republican_leap_year else 22, 0, 0, 0,
            #     tzinfo=dt.timezone.utc)
            new_republican_year = dt.datetime(
                date.year, 9, 22, tzinfo=dt.timezone.utc)
        else:
            # new_republican_year = dt.datetime(
            #     date.year - 1, 9, 23 if previous_year_is_leap else 22, 0, 0, 0,
            #     tzinfo=dt.timezone.utc)
            new_republican_year = dt.datetime(
                date.year - 1, 9, 22, tzinfo=dt.timezone.utc)

        # print(year)

        # previous_year_is_leap = (
        #     (year - 1) % 4 == 0 and (year - 1) != 0)

        days_since_new_year = date - new_republican_year
        # days_since_new_year = date - dt.datetime(
        #     new_republican_year.year, 9, 22, tzinfo=dt.timezone.utc)

        republican_leap_year = year % 4 == 0 and year != 0
        leap_year = (
            (date.year % 400 == 0) or (
                (date.year % 4 == 0) and (date.year % 100 != 0)))

        if leap_year:
            if (date >= dt.datetime(date.year, 3, 1, tzinfo=dt.timezone.utc)
                    and date <= dt.datetime(
                        date.year, 9, 21, tzinfo=dt.timezone.utc)):
                days_since_new_year -= dt.timedelta(days=1)

        month = math.floor(days_since_new_year.days / 30) + 1
        day = (days_since_new_year.days % 30) + 1

        republican_date = Revolver.RepublicanDate(year, month, day, day)

        if republican_leap_year:
            if (date < dt.datetime(date.year, 3, 1, tzinfo=dt.timezone.utc)
                    or date > dt.datetime(
                        date.year, 9, 21, tzinfo=dt.timezone.utc)):
                republican_date.remove_one_day(republican_leap_year)

        if date >= dt.datetime(1800, 3, 1, tzinfo=dt.timezone.utc):
            republican_date.remove_one_day(republican_leap_year)

        revolver = Revolver(
            republican_date.year, republican_date.month,
            republican_date.day, republican_date.day, 0, 0)
        revolver.republican_date = republican_date
        # if month == 13:
        # print("{}\t{}-{}-{}\t{}".format(
        #      date, day, month, year, days_since_new_year))
        return revolver

if __name__ == "__main__":
    print(Revolver.iso_to_republican(dt.datetime.now(dt.timezone.utc)))
    current_date = dt.datetime(1792, 9, 22, 0, 0, tzinfo=dt.timezone.utc)
    previous_revolver = None
    while current_date <= dt.datetime(1803, 9, 22, tzinfo=dt.timezone.utc):
        date = Revolver.iso_to_republican(current_date)
        print("{}\t{}\t{}".format(
            current_date,
            date.republican_date, date))
        current_date += dt.timedelta(days=1)
