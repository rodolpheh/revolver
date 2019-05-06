
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import metric_time
import datetime
from dateutil.parser import isoparse
import pytz

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Site in construction"

@app.route('/convert/<date>')
def convert(date):
    return date

@app.route('/now')
def now():
    now = datetime.datetime.now(pytz.timezone('Europe/Paris'))
    return to_revolver(now)

@app.route('/from_iso/<date_str>')
def from_iso(date_str):
    iso_date = isoparse(date_str)
    return to_revolver(iso_date)

@app.route('/to_iso/<revolver>')
def to_iso(revolver):
    date_str, time_str = revolver.split('-')
    year_str, month_str, day_str = date_str.split('.')
    year = int(year_str) - 10000
    month = 1
    day = 1
    all_minutes = (int(time_str[0]) * 2.4 * 60) + (int(time_str[1:]) * 1.44)
    hour = int(all_minutes / 60)
    minutes = int(all_minutes) % 60
    full = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minutes)
    full = pytz.timezone('Europe/Paris').localize(full)
    return full.isoformat()

def to_revolver(iso_date):
    #now = datetime.datetime.now(pytz.timezone('Europe/Paris'))
    if iso_date.tzinfo is None or iso_date.tzinfo.utcoffset(iso_date) is None:
        iso_date = iso_date.replace(tzinfo=pytz.timezone('Europe/Paris'))
    else:
        iso_date = iso_date.astimezone(pytz.timezone('Europe/Paris'))
    time = metric_time.DecimalTime().decimal_time(iso_date)
    date = metric_time.RepublicanCalendar().republican_date(iso_date)
    year = iso_date.year + 10000
    month = metric_time.RepublicanCalendar().MONTHS.index(date.month)
    date_str = "{}.{:02d}.{:02d}".format(year, month, date.day)
    time_str = "{}{:02d}".format(time.hours, time.minutes)
    return "{}-{}".format(date_str, time_str)

