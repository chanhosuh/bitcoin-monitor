FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y software-properties-common
RUN add-apt-repository ppa:bitcoin/bitcoin -y
RUN apt-get update && \
    apt-get install -y bitcoind && \
    rm -rf /var/lib/apt/lists/*

# create data directory
ENV DATA_DIR /data
RUN mkdir "$DATA_DIR"

# install config
COPY bitcoin.conf /bitcoin.conf

CMD bitcoind -printtoconsole -conf="/bitcoin.conf" -datadir="$DATA_DIR"
