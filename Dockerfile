FROM python:3.6-alpine3.6

COPY . /app
WORKDIR /app

RUN pip install pipenv

RUN pipenv install --system

ENTRYPOINT ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]