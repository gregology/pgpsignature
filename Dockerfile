FROM python:3.10-slim-buster

WORKDIR /app

ENV APP_SETTINGS config.ProductionConfig

RUN apt-get update
RUN apt-get install -y postgresql
RUN apt-get install -y libpq-dev gcc

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]