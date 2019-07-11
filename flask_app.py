from flask import Flask
import datetime
import pytz

from revolver.revolver import Revolver

app = Flask(__name__)

year_offset = 11792

@app.route('/')
def hello_world():
    return "Site in construction"

@app.route('/now')
def now():
    return str(Revolver.now())

@app.route('/from_iso/<date_str>')
def from_iso(date_str):
    return str(Revolver.from_iso_str(date_str))

@app.route('/to_iso/<revolver>')
def to_iso(revolver):
    # Parse the good stuff
    date_str, time_str = revolver.split('-')
    year_str, month_str, day_str = date_str.split('.')
    hour, minute = int(time_str[0]), int(time_str[1:])
    return Revolver(int(year_str), int(month_str), int(day_str), hour, minute).iso_date

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

