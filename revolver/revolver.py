import metric_time
import datetime
from dateutil.parser import isoparse
import pytz

year_offset = 11792


class Revolver(object):

    def __init__(
            self, year, month, day, day_of_the_week,
            hour, minute, *args, **kwargs):
        self.year = year
        self.month = month
        self.day = day
        self.day_of_the_week = day_of_the_week

        self.hour = hour
        self.minute = minute

    @property
    def yearly(self):
        return str(self.year)

    @property
    def monthly(self):
        return "{}.{:02d}".format(self.year, self.month)

    @property
    def dayly(self):
        return "{}.{:02d}.{:02d}".format(self.year, self.month, self.day)

    @property
    def hourly(self):
        return "{}.{:02d}.{:02d}.{}{:02d}".format(
            self.year, self.month, self.day, self.hour, self.minute)

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

        time = metric_time.DecimalTime().decimal_time(iso_date)
        date = metric_time.RepublicanCalendar().republican_date(iso_date)
        year = int(date.year) + year_offset
        if date.month is not None:
            month = (
                metric_time.RepublicanCalendar().MONTHS.index(date.month) + 1)
        else:
            month = None

        revolver = Revolver(
            year, month, date.day, date.day_of_the_week,
            time.hours, time.minutes)
        return revolver

    @staticmethod
    def now():
        now = datetime.datetime.now(pytz.timezone('UTC'))
        return Revolver.from_iso(now)

    @property
    def iso_date(self):
        republican_year = self.year - year_offset
        year = self.year - year_offset + 1792

        # Calculations source :
        # https://fr.wikipedia.org/wiki/Concordance_des_dates_des_calendriers_r%C3%A9publicain_et_gr%C3%A9gorien

        temp_date = datetime.datetime(
            year=year, month=9, day=21, tzinfo=datetime.timezone.utc)

        # If the date is between Ventose 1st and Nivose 11th, subtract one year
        if self.month < 4 or (self.month == 4 and self.day <= 11):
            temp_date.year -= 1

            # If the year is a multiple of 4, add a day
            if republican_year % 4 == 0:
                temp_date += datetime.timedelta(days=1)

        time_since_sans_culottides = (self.month - 1) * 30 + (self.day - 1)

        temp_date += datetime.timedelta(days=time_since_sans_culottides)

        for century in range(18, int(temp_date.year / 100)):
            if century % 4 == 0:
                continue
            if temp_date > datetime.datetime(
                    year=temp_date.year, month=2, day=28,
                    tzinfo=datetime.timezone.utc):
                temp_date += datetime.timedelta(days=1)

        # Compute the time (accurate to 1 minute because we don't keep the
        # seconds in the format)
        minutes = (self.hour * 2.4 * 60) + (self.minute * 1.44)
        hour = int(minutes / 60)
        minutes = int(minutes) % 60
        date = datetime.datetime(
            year=year, month=temp_date.month, day=temp_date.day,
            hour=hour, minute=minutes, tzinfo=datetime.timezone.utc)
        return date.isoformat()
