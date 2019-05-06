
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import metric_time
import datetime
import pytz

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'This is the page for revolver'

@app.route('/convert/<date>')
def convert(date):
    return date

@app.route('/now')
def now():
    now = metric_time.get_local_now()
    year = now.year + 10000
    date = metric_time.RepublicanCalendar().now()
    month = metric_time.RepublicanCalendar().MONTHS.index(date.month)
    time = metric_time.DecimalTime().decimal_time(datetime.datetime.now(pytz.timezone('Europe/Paris')))
    date_str = "{}.{:02d}.{:02d}".format(year, month, date.day)
    time_str = "{}{:02d}".format(time.hours, time.minutes)
    return "{}-{}".format(date_str, time_str)
