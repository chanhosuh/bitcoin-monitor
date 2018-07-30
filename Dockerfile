FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:bitcoin/bitcoin -y
RUN apt-get update
RUN apt-get install -y bitcoind

RUN mkdir /root/.bitcoin
RUN echo "maxconnections=15\n\
prune=5000\n\
dbcache=150\n\
maxmempool=150\n\
maxreceivebuffer=2500\n\
maxsendbuffer=500" > /root/.bitcoin/bitcoin.conf

CMD ["bitcoind", "-printtoconsole"]
