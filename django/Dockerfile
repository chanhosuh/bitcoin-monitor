FROM python:3.7.0-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /tmp

RUN apt-get update
RUN apt-get install --no-install-recommends -y \
    vim-tiny \
    && \
    pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /code

WORKDIR /code/
ENV PATH /code:$PATH

