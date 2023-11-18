from web3 import Web3
import pandas as pd

connection = Web3()
def gen_keys(name):
    list_of_dicts = []
    account = connection.eth.account.create()
    address = account.address
    private_key = account.key.hex()

    print('Account', name, '\n',
            'Public:', address, '\n',
            'Private_key:', private_key, '\n',
            '--------------------------')

    dictionary = dict()
    dictionary['address'] = address
    dictionary['private_key'] = private_key

    list_of_dicts.append(dictionary)
    return list_of_dicts