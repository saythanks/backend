FROM python:3.6-alpine
LABEL maintainer Oscar Newman

RUN apk update && \
    apk add \
    bash \
    postgresql-dev \
    gcc \
    python3-dev \
    build-base linux-headers pcre-dev \
    musl-dev \
    alpine-sdk \
    supervisor

RUN pip install pipenv uwsgi


# Create a group and user
RUN addgroup -S app && adduser -S app -G app

# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY uwsgi.ini /etc/uwsgi/
# Custom Supervisord config
COPY supervisord.conf /etc/supervisord.conf

COPY . /app
WORKDIR /app

RUN pipenv install --deploy --system
# RUN pipenv lock -r > requirements.txt
# RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "/usr/bin/supervisord" ]
