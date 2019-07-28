from flask import Flask, abort
from revolver.revolver import Revolver
import metric_time as mt
import datetime as dt
import math

app = Flask(__name__)

year_offset = 11792


@app.route('/')
def hello_world():
    return "Site in construction"


@app.route('/now')
def now():
    revolver = Revolver.now()
    if revolver.month is None:
        abort(403, description=revolver.day_of_the_week)
    return str(revolver)


@app.route('/republican/now')
def republican_now():
    date = mt.RepublicanCalendar().republican_date(
        dt.datetime.now(dt.timezone.utc))
    return "{} {} {}".format(date.day, date.month, math.ceil(date.year))


@app.route('/from_iso/<date_str>')
def from_iso(date_str):
    revolver = Revolver.from_iso_str(date_str)
    if revolver.month is None:
        abort(403, description=revolver.day_of_the_week)
    return str(revolver)


@app.route('/to_iso/<revolver>')
def to_iso(revolver):
    # Parse the good stuff
    date_str, time_str = revolver.split('-')
    year_str, month_str, day_str = date_str.split('.')
    hour, minute = int(time_str[0]), int(time_str[1:])
    return Revolver(
        int(year_str), int(month_str), int(day_str),
        None, hour, minute).iso_date


@app.errorhandler(403)
def not_allowed(e):
    return str(e)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
