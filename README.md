# bitcoin-monitor
Monitor and persist Bitcoin on-chain data to Postgres.

## Quickstart guide
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

## References
[Mastering Bitcoin, chapter 3](https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch03.asciidoc), intro to `bitcoind`
