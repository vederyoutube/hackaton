from web3 import Web3
import json
import pandas as pd
from typing import Optional
from hexbytes import HexBytes
from web3.middleware import geth_poa_middleware
from time import sleep



binance_testnet_rpc_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
web3 = Web3(Web3.HTTPProvider(binance_testnet_rpc_url))

ERC20_ABI = json.loads('''[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')
token = 0
token_address = 0
User_address = 0
def remittance(Radd, Pkey, amount):
    dict_transaction = {
  'chainId': web3.eth.chain_id,
  'from': User_address,
  'gasPrice': web3.eth.gas_price,
  'nonce': web3.eth.get_transaction_count(User_address),
    }
    usdt_decimals = token.functions.decimals().call()
    one_TRD = amount * 10 ** usdt_decimals  # отправляем TDR

    # создаём транзакцию
    transaction = token.functions.transfer(
        Radd, one_TRD
    ).build_transaction(dict_transaction)

    # подписываем
    signed_txn = web3.eth.account.sign_transaction(transaction, Pkey)

    # Отправляем, смотрим тут https://testnet.bscscan.com/
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(txn_hash.hex())
    sleep(1)
    print(web3.eth.get_transaction_receipt(txn_hash))
    return txn_hash.hex(), web3.eth.get_transaction_receipt(txn_hash)
def gen_keys(name): #принимает значение имени профиля и возвращает публичный и приватный ключ
    list_of_dicts = []
    account = web3.eth.account.create() # генерируем новые ключи и после присваиваем их переменным
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
def checkGasPrice():
    print(f"gas price: {web3.eth.gas_price} BNB")  # кол-во Wei за единицу газа
    return web3.eth.gas_price
def checkConnecction():
    print(f"Is connected: {web3.is_connected()}")  # Is connected: True
    return web3.is_connected()
def checkBlockNum():
    print(f"current block number: {web3.eth.block_number}")
    return web3.eth.block_number
def checkChain():
    print(f"number of current chain is {web3.eth.chain_id}")  # 97
    return web3.eth.chain_id
def initToken(Tadress, Uadress):
    global token_address, User_address, token    
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    web3.eth.account.enable_unaudited_hdwallet_features()
    token = web3.eth.contract(address=Tadress, abi=ERC20_ABI)
    token_address = Tadress
    User_address = Uadress
    # wallet_address = Uadress  # ваш адрес
    # all_functions = token.all_functions()
    # token_name = token.functions.name().call()
    # token_symbol = token.functions.symbol().call()
    # print(f"все функции {token_name} {token_symbol}:\n{all_functions}")
    # token_ballance = token.functions.balanceOf(wallet_address).call()
    # print(token_ballance)
    # token_decimals = token.functions.decimals().call()
    # ether_balance = token_ballance/ 10 ** token_decimals
    # print(f"Balance of {token_name}({token_symbol}) is {ether_balance}")
    # allowance = token.functions.allowance(Tadress, Uadress).call()
    # print(f"Allowance for {Tadress} is {allowance}")

def checkName():
    token_name = token.functions.name().call()
    return token_name
def checkSym():
    token_symbol = token.functions.symbol().call()
    return token_symbol
def checkBallance():
    global User_address
    token_ballance = token.functions.balanceOf(User_address).call()
    token_decimals = token.functions.decimals().call()
    ether_balance = token_ballance/ 10 ** token_decimals
    return ether_balance
def checkAllowance():
    allowance = token.functions.allowance(token_address, User_address).call()
    return allowance

    
# initToken("0x50bed58Fb07fe2de42D6DA99b4e97ABA883B273D", "0xfa8DdE9Ed11042FBF156b6f62760794ec56F3226")
# checkGasPrice()
# checkConnecction()
# checkBlockNum()
# checkChain()
# print(checkName())
# print(checkSym())
# print(checkBallance())
# print(checkAllowance())