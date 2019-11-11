# bitcoin-monitor
Bitcoin block explorer, using Django to persist blocks from the bitcoin node (`bitcoind`) into Postgres, and displaying through a React frontend.

Celery is used for the persist tasks and Channels is used to notify the frontend of new blocks.  Redis is used as the persistence store for both.

Docker is used to encapsulate the separate pieces.  Nginx is used for the production setup (see `docker-compose.prod.yml`) and omitted for the dev setup (`docker-compose.yml`).

## Quickstart guide

### Setup
- install Docker: [Mac](https://www.docker.com/docker-mac) | [Ubuntu](https://www.docker.com/docker-ubuntu)
- clone the repo and change working directory to it
- `make help` will show available `make` commands

### Run Docker

- start the containers:
  - `make up` (first time this will also build the images)
  - ctrl-c will detach you from the logging output; container will still be running in the background
  - `make logs` will re-attach you to logging
  - `bitcoind` logging drowns out the others.  So `make log name=django` will show output only from the `django` container.  Other container names are `celery` (worker tasks), `redis`, `db` (postgres), `bitcoind`, and in prod setup: `nginx`, `daphne`. 
- stop the containers:
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
  
### Persisting blocks into Postgres

To run the Celery tasks that read block data from `bitcoind` and persist to Postgres (`db` container):
- `make bash` (defaults to bash in `django` container)
- `./manage.py process_blockchain`

You should see rpc calls in stdout and `celery` log output for the tasks.

### Block explorer frontend

For dev setup, just `cd django/frontend` and then `npm start`.  Then visit `localhost:3000` in your browser.  You should see the initial list of blocks and as each celery task completes, the websocket will pick up the block message and prepend to the list.

For prod setup, you should build the static files first:
- `cd django/frontend`
- `npm run build`
- `cd ../../`
- `make bash`
- `./manage.py collectstatic`

Then visit `localhost:80` in your browser.

## References
* [Mastering Bitcoin, chapter 3](https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch03.asciidoc): intro to `bitcoind`
* [ChainQuery](http://chainquery.com/bitcoin-api): useful web interface to learn about `bitcoin-cli`
