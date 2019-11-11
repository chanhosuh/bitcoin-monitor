# bitcoin-monitor
Bitcoin block explorer, using Django to persist blocks from the bitcoin node (`bitcoind`) into Postgres, and displaying through a React frontend.

Celery is used for the persist tasks and Channels is used to notify the frontend of new blocks.  Redis is used as the persistence store for both.

Docker is used to encapsulate the separate pieces.  Nginx is used for the production setup (see `docker-compose.prod.yml`) and omitted for the dev setup (`docker-compose.yml`).

## Quickstart guide
- install Docker: [Mac](https://www.docker.com/docker-mac) | [Ubuntu](https://www.docker.com/docker-ubuntu)
- clone the repo
- build the Docker image:
  - `make build`
  - only needs to be done the first time or when docker-related files change
- start the container:
  - `make up` 
  - ctrl-c will detach you from the logging output; container will still be running in the background
  - `make logs` will re-attach you to logging
- stop the container:
  - `make down`
- check everything works:
  - start the containers if they aren't running (`make up`)
  - `make status` (should show local blockchain info)
- interactive usage of the python Rpc client:
  - `make ipython` (will drop you in an ipython shell inside the `django` container)
  - `from jsonrpc.client import RpcClient`\
    `client = RpcClient()`\
    `block_hash = client.get_best_block_hash()`\
    `client.get_block(block_hash)`
- direct usage of bitcoind's rpc client, `bitcoin-cli`:
  - `make bash name=bitcoind` (will drop you in a bash shell inside the `bitcoind` container)
  - `bitcoin-cli getbestblockhash` (should return a hash)
  - `bitcoin-cli help` (shows more commands)
- `make help` will show more `make` commands

## References
* [Mastering Bitcoin, chapter 3](https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch03.asciidoc): intro to `bitcoind`
* [ChainQuery](http://chainquery.com/bitcoin-api): useful web interface to learn about `bitcoin-cli`
