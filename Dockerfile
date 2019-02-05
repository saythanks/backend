FROM python:3.6-alpine3.6

COPY . /app
WORKDIR /app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install pipenv

RUN pipenv install --system

ENTRYPOINT ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]
