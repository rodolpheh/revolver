from flask import Flask, abort
from revolver.revolver import Revolver
import revolver.binary_clock
import metric_time as mt
import datetime as dt
import math
from flasgger import Swagger

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'RevolVer API',
    'uiversion': 3,
    "version": "0.0.1",
    "title": "RevolVer API",
    "description": 'This is the API for RevolVer',
    'hide_top_bar': True
}
swagger = Swagger(app)

year_offset = 11792


@app.route('/')
def hello_world():
    return "Site in construction"


@app.route('/now')
def now():
    """Returns the current date as a RevolVer version number.
    ---
    tags:
      - Revolver
    responses:
      200:
        description: A RevolVer version number
      403:
        description: It is the sans-culottides, you shouldn't work
    """
    revolver = Revolver.now()
    return str(revolver)

@app.route('/now/<format>')
def now_with_format(format):
    """Returns the current date in different RevolVer formats
    Four formats are disponible :
      * hourly: YYYYY.MM.DD-HMM, equivalent to the /now endpoint
      * daily: YYYYY.MM.DD
      * monthly: YYYYY.MM
      * yearly: YYYYY
    ---
    tags:
      - Revolver
    parameters:
      - name: format
        in: path
        type: string
        required: true
        description: The format of the RevolVer
        enum: ['hourly', 'daily', 'monthly', 'yearly']
    responses:
      200:
        description: A RevolVer version number
      403:
        description: It is the sans-culottides, you shouldn't work
    """
    revolver = Revolver.now()
    choices = {
        "hourly": revolver.hourly,
        "daily": revolver.daily,
        "monthly": revolver.monthly,
        "yearly": revolver.yearly
    }
    try:
        return choices[format]
    except KeyError:
        return "Not a valid format"


@app.route('/republican/now')
def republican_now():
    """Give the republican date of the day
    ---
    tags:
      - Republican calendar
    responses:
      200:
        description: The date of today in the republican calendar
    """
    date = Revolver.republican_now()
    # date = mt.RepublicanCalendar().republican_date(
    #     dt.datetime.now(dt.timezone.utc))
    return "{} {} {}".format(date["day"], date["month"], math.ceil(date["year"]))


@app.route('/from_iso/<date_str>')
def from_iso(date_str):
    """Convert an ISO date to a RevolVer version number.
    ---
    tags:
      - Revolver
    parameters:
      - name: date_str
        in: path
        type: string
        required: true
        description: A date in ISO format
    responses:
      200:
        description: A RevolVer version number
      403:
        description: It is the sans-culottides, you shouldn't work
    """
    revolver = Revolver.from_iso_str(date_str)
    return str(revolver)


@app.route('/to_iso/<revolver>')
def to_iso(revolver):
    """Convert RevolVer version number into an ISO date
    ---
    tags:
      - Revolver
    parameters:
      - name: revolver
        in: path
        type: string
        required: true
        description: A RevolVer version number
    responses:
      200:
        description: The converted date in ISO format
    """
    # Parse the good stuff
    date_str, time_str = revolver.split('-')
    year_str, month_str, day_str = date_str.split('.')
    hour, minute = int(time_str[0]), int(time_str[1:])
    return Revolver(
        int(year_str), int(month_str), int(day_str),
        None, hour, minute).iso_date


@app.route('/ansi_clock')
def ansi_clock():
    """Display the current metric time in a visual binary format
    ---
    tags:
      - Time
    responses:
      200:
        description: The current metric time in a visual binary format
    """
    return revolver.binary_clock.ansi_clock(Revolver.now())


@app.errorhandler(403)
def not_allowed(e):
    return str(e)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
