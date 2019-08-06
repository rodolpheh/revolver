FROM python:alpine 

RUN apk add gcc musl-dev

COPY ./requirements.txt /

RUN pip install -r requirements.txt

COPY . /src/

EXPOSE 5000

ENTRYPOINT ["python", "/src/flask_app.py"]