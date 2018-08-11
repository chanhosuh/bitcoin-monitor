# some useful links:
# https://kryptomusing.wordpress.com/2017/06/12/bitcoin-rpc-via-python/

import requests
import json

jsonrpc_version = '2.0'
headers = {'content-type': 'application/json'}

rpc_id = 'bitcoin-monitor'

rpc_method = 'getblock'
# --- get best block hash -----
# $ make bash
# Dropping into bash inside bitcoind container.
# root@efa0de6df53b:/# bitcoin-cli -rpcuser=user -rpcpassword=password getbestblockhas
# 0000000000000000088321525a33f3838d973077375875ba733985ff4a92abcb
# -----------------------------
block_hash = '0000000000000000088321525a33f3838d973077375875ba733985ff4a92abcb'
rpc_params = [block_hash]

params = {
    'jsonrpc': jsonrpc_version,
    'id': rpc_id,
    'method': rpc_method,
    'params': rpc_params,
}
payload = json.dumps(params)
response = requests.post(
    'http://user:password@bitcoind:8332',
    headers=headers,
    data=payload,
)
print(response)
response_json = response.json()
print(response_json['result'])
# import ipdb; ipdb.set_trace()

transaction_ids = response_json['result']['tx']
