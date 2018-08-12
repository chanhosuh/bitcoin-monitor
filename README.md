# bitcoin-monitor
Monitor and persist Bitcoin on-chain data to Postgres.

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
- check RPC client works:
  - start the containers if they aren't running (`make up`)
  - `make bash` (will drop you in a bash shell inside the `django` container)
  - `python -m jsonrpc.client` (runs the "main" code in the `jsonrpc.client` module)
  - you should see JSON output of a block's contents
    - if not, you can debug with [pdb][pdb guide] by putting a `import ipdb; ipdb.set_trace()` line inside the main code in the client module and running the script again.

[pdb guide]: https://pymotw.com/3/pdb/

## References
[Mastering Bitcoin, chapter 3](https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch03.asciidoc), intro to `bitcoind`
