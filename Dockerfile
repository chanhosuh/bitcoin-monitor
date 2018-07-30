FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:bitcoin/bitcoin -y
RUN apt-get update
RUN apt-get install -y bitcoind

RUN mkdir /root/.bitcoin
RUN echo "\
# keep full transaction index, useful for getrawtransaction\
# txindex=1\n\
# max size in MB, deleting old blocks\
prune=5000\n\
# max number of nodes to accept connections from\
maxconnections=15\n\
# UTXO cache size in MiB, 300 is default\
dbcache=150\n\
# max size of mempool in MiB\
maxmempool=150\n\
# max buffer size per connection, as multiples of 1K bytes\
maxreceivebuffer=2500\n\
maxsendbuffer=500\n\
" > /root/.bitcoin/bitcoin.conf

CMD ["bitcoind", "-printtoconsole"]
