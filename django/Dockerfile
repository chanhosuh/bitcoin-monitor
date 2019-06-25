FROM python:3.7.0-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install --no-install-recommends -y \
    gcc \
    procps \
    vim-tiny \
    && \
    pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

COPY . /code
WORKDIR /code

RUN pip install -r requirements.txt

ENV PATH /code:$PATH
