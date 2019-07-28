import metric_time
import datetime
from dateutil.parser import isoparse
import pytz

from convertdate import french_republican, gregorian

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
    def daily(self):
        return "{}.{:02d}.{:02d}".format(self.year, self.month, self.day)

    @property
    def hourly(self):
        return "{}.{:02d}.{:02d}-{}{:02d}".format(
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
        date = french_republican.from_gregorian(
            iso_date.year, iso_date.month, iso_date.day)

        year = int(date[0]) + year_offset

        revolver = Revolver(
            year, date[1], date[2], None,
            time.hours, time.minutes)
        return revolver

    @staticmethod
    def now():
        now = datetime.datetime.now(pytz.timezone('UTC'))
        return Revolver.from_iso(now)

    @property
    def iso_date(self):
        republican_year = self.year - year_offset
        temp_date = french_republican.to_gregorian(
            republican_year, self.month, self.day)

        # Compute the time (accurate to 1 minute because we don't keep the
        # seconds in the format)
        minutes = (self.hour * 2.4 * 60) + (self.minute * 1.44)
        hour = int(minutes / 60)
        minutes = int(minutes) % 60
        date = datetime.datetime(
            year=temp_date[0], month=temp_date[1], day=temp_date[2],
            hour=hour, minute=minutes, tzinfo=datetime.timezone.utc)
        return date.isoformat()
