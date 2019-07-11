FROM python:alpine 

RUN pip install flask metric_time pytz python-dateutil

COPY . /src/

EXPOSE 5000

ENTRYPOINT ["python", "/src/flask_app.py"]