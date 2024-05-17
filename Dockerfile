FROM python:3.12.3-slim-bookworm

LABEL author="Egor Maksimov" contact="egor.maksimov.rtf@yandex.ru"

SHELL ["/bin/bash", "-c"]

WORKDIR /app

COPY requirements.txt .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set up the environment on a single docker layer
# GDAL library is needed for interacting with postgis Point class
RUN apt update && apt install -y python-is-python3 && pip install --upgrade pip && \
    apt install -y gdal-bin && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m pip uninstall -y pip setuptools

COPY . .
