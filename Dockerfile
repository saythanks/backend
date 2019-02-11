FROM python:3.6-alpine3.6

LABEL maintainer Oscar Newman


RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev alpine-sdk
RUN pip install pipenv

COPY . /app
WORKDIR /app


RUN pipenv install --system

EXPOSE 5000

ENTRYPOINT ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]
