FROM python:alpine 

RUN apk add gcc musl-dev

RUN pip install flask metric_time pytz python-dateutil convertdate

COPY . /src/

EXPOSE 5000

WORKDIR /src

ENTRYPOINT ["python", "/src/flask_app.py"]