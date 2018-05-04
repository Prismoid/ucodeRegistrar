# coding:utf-8
from web3 import Web3, HTTPProvider, IPCProvider
from web3.contract import ConciseContract
import json
import sys
import time
import datetime

web3 = Web3(HTTPProvider('http://localhost:8545'))
# web3 = Web3(IPCProvider())

def howToUse():
    print("--- how to use ---")
    print("1. ID information: python3 CheckStateOfBC.py 1 \"ID Space's key (120bit)\"")
    print("2. Default Account Information: python3 CheckStateOfBC.py 2")
    sys.exit()

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

if (len(sys.argv) < 2):
    howToUse()
    
instr = sys.argv[1] 

if (instr == "1" and len(sys.argv) == 3):
    IDKey = sys.argv[2] 
    addr = contract.call({'from': defaultAccount}).getAddr(int(IDKey, 16))
    timestamp = contract.call({'from': defaultAccount}).getTimestamp(int(IDKey, 16))
    print("--- ID Space's key: " + IDKey + " ---");
    print("owner: " + addr.capitalize());
    print("timestamp: " + str(timestamp));
elif (instr == "2" and len(sys.argv) == 2):
    hashData = contract.call({'from': defaultAccount}).getPreOrderHash(defaultAccount)
    blockHeight = contract.call({'from': defaultAccount}).getPreOrderBlockHeight(defaultAccount)
    print("--- Default Account User Info ---");
    print("pre-order hash: " + web3.toHex(hashData))
    print("pre-order blockHeight: " + str(blockHeight))
    
else:
    howToUse()
