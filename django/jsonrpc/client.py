import json
import requests

from bitcoin_monitor import settings
from . import RpcError


class RpcClientError(RpcError):
    pass


# pylint: disable=redefined-outer-name
class RpcClient:
    """ class to interact with bitcoind through
    its JSON-RPC API; essentially a substitute
    for bitcoin-cli """

    def __init__(self):
        self._rpc_url = settings.RPC_URL

        self._rpc_version = settings.RPC_VERSION
        self._rpc_id = settings.RPC_ID

        self._session = requests.Session()
        # TODO: have authentication come from settings file
        # needs to be sync-ed with bitcoin.conf in bitcoind
        self._session.auth = 'user', 'password'
        self._session.headers = settings.RPC_HEADERS

    def _call_method(self, rpc_method_name, rpc_params):
        params = {
            'jsonrpc': self._rpc_version,
            'id': self._rpc_id,
            'method': rpc_method_name,
            'params': rpc_params,
        }
        payload = json.dumps(params)
        response = self._session.post(
            self._rpc_url,
            headers=self._session.headers,
            data=payload,
        )
        return response

    def get_best_block_hash(self):
        response = self._call_method('getbestblockhash', rpc_params=[])
        response_json = response.json()
        return response_json['result']

    def get_block(self, block_hash, verbosity=1):
        if verbosity not in [1, 2]:
            raise RpcClientError(
                "verbosity must be 1 or 2; for verbosity 0, use 'get_raw_block' instead"
            )
        response = self._call_method(
            rpc_method_name='getblock',
            rpc_params=[block_hash, verbosity],
        )
        response_json = response.json()
        return response_json['result']

    def get_transactions(self, block_hash):
        block = self.get_block(block_hash, verbosity=2)
        transactions = block['tx']
        return transactions

    def get_block_transaction_value(self, block_hash):
        raise NotImplementedError('todo')


if __name__ == '__main__':
    client = RpcClient()
    block_hash = client.get_best_block_hash()
    block = client.get_block(block_hash)
    print(block)

