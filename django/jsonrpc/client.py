import json
import requests

from bitcoin_monitor import settings
from . import RpcError
import functools


class RpcClientError(RpcError):
    pass


def jsonify_response(func):

    @functools.wraps(func)
    def inner(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code not in [200, 500]:
            raise RpcClientError(
                str(response.status_code) + ' error: ' + response.reason
            )
        response_json = response.json()
        if 'error' in response_json and response_json['error']:
            raise RpcClientError(response_json['error'])

        return response_json['result']

    return inner


# pylint: disable=redefined-outer-name
class RpcClient:
    """ class to interact with bitcoind through
    its JSON-RPC API; essentially a substitute
    for bitcoin-cli.

    The example code from this link was useful for
    getting started:
    https://kryptomusing.wordpress.com/2017/06/12/bitcoin-rpc-via-python/
    """

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
        """
        Posts a request using session and config data,
        passing the RPC method name and parameters.

        Returns a response object.
        """
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

    @jsonify_response
    def get_best_block_hash(self):
        return self._call_method('getbestblockhash', rpc_params=[])

    @jsonify_response
    def get_block(self, block_hash, verbosity=1):
        """
        :param block_hash: string, hash of the wanted block
        :param verbosity: int
            0: raw byte string
            1: JSON dict with 'tx' giving list of transaction hashes
            2: same as 1 except 'tx' gives list of JSON transactions
        :return: string,
            hash or JSON, depending on 'verbosity' argument
        """
        return self._call_method(
            rpc_method_name='getblock',
            rpc_params=[block_hash, verbosity],
        )

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
