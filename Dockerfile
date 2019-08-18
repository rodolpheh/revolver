FROM python:alpine 

RUN apk add gcc musl-dev uwsgi linux-headers

COPY ./requirements.txt /

RUN pip install -r requirements.txt
RUN pip install uwsgi

COPY . /src/

EXPOSE 5000

WORKDIR /src

ENTRYPOINT ["uwsgi", "--http-socket", "0.0.0.0:5000", "--wsgi-file", "flask_app.py", "--callable", "app", "--mount", "/revolver/api=flask_app.py"]
