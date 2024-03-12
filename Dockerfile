FROM python:3.12-alpine3.19

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# required to install mysqlclient
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev


RUN pip install --upgrade setuptools
RUN pip install pipenv 
COPY Pipfile* .
RUN pipenv install --system --dev

COPY ./app .

RUN addgroup app && adduser -S -G app app
USER app

EXPOSE 8000