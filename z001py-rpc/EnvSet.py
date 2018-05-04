# coding:utf-8
from web3 import Web3, HTTPProvider, IPCProvider
from web3.contract import ConciseContract
import json
import sys

web3 = Web3(HTTPProvider('http://localhost:8545'))
# web3 = Web3(IPCProvider())

def howToUse():
    print("--- how to use ---")
    print("1. deposit: python3 InstrToken.py 1 \"deposit value\"")
    print("2. withdraw: python3 InstrToken.py 2 \"withdraw value\"")
    print("3. send: python3 InstrToken.py 3 \"send address\" \"send value\"")
    print("4. display local node's accounts's value: python3 InstrToken.py 4")
    sys.exit(1)

# creating contract object
f = open("../build/contracts/ucodeRegistrar.json")
contract_json = json.load(f)
f.close()
addr = contract_json["networks"]["10"]["address"]
abi  = contract_json["abi"]
contract = web3.eth.contract(abi, addr)

# open account.dat
f = open("account.dat", "r")
defaultAccount = ""
for defaultAccount in f:
    defaultAccount.strip()
f.close()

amount =  web3.toWei(10, "ether")
# unlock default account
web3.personal.unlockAccount(web3.eth.accounts[0], "", 3600)
print(web3.eth.sendTransaction({
    "from": web3.eth.accounts[0],
    "to":defaultAccount,
    "value": amount}))

