FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --no-cache \
        postgresql-dev \
        libjpeg \
        build-base \
        python3-dev \
        libffi-dev \
        jpeg-dev \
        zlib-dev \
        lcms2-dev \
        openjpeg-dev \
        gcc \
        wget \
		zlib \
        tzdata

COPY ./source/ /source

WORKDIR /source

RUN pip install --upgrade pip && \
    pip install -r requirements.txt


COPY ./docker/docker-entrypoint.sh /entrypoint.sh

ARG POSTGRES_USER=''
ARG POSTGRES_PASSWORD=''
ARG POSTGRES_HOST=''
ARG POSTGRES_PORT='0'
ARG POSTGRES_DB=''
ARG CLINICS_BEARER=''
ARG PHYSICIANS_BEARER=''
ARG PATIENTS_BEARER=''
ARG METRICS_BEARER=''
ARG CLINICS_HOST=''
ARG PHYSICIANS_HOST=''
ARG PATIENTS_HOST=''
ARG METRICS_HOST=''


ENTRYPOINT ["/entrypoint.sh"]