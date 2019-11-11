FROM python:3.7.0-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --no-install-recommends -y \
    python3-dev \
    gcc \
    procps \
    vim-tiny \
    && \
    pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENV PATH /code:$PATH
