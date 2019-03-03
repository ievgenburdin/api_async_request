FROM python:3.5
ENV PYTHONUNBUFFERED 1

COPY ./docker/python/requirements.txt /requirements/requirements.txt
COPY ./docker/python/entrypoint.sh /entrypoint.sh

RUN pip install --upgrade pip
RUN pip install -r /requirements/requirements.txt

ENV TZ=America/Tijuana

COPY ./project /app

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
