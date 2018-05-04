# coding:utf-8
from web3 import Web3, HTTPProvider, IPCProvider
from web3.contract import ConciseContract
import json
import sys
import time

web3 = Web3(HTTPProvider('http://localhost:8545'))
# web3 = Web3(IPCProvider())

def howToUse(result):
    print("--- how to use ---")
    print("1. revokeSLD  : python3 InstrMgt.py 1 key(80bit)")
    print("2. changeOwner: python3 InstrMgt.py 2 key(80bit) validHeight(64bit) toAddr(160bit) v(8bit) r(32Bytes) s(32Bytes)")
    sys.exit(result)

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
    howToUse(-1)
    
instr = sys.argv[1] # 1: setowner

if (instr == "1" and len(sys.argv) == 3):
    key = sys.argv[2]
    print(key)
    result = contract.call({'from': defaultAccount}).revokeSLD(int(key, 16));
    if (result > 0):
        result = contract.transact({'from': defaultAccount, 'gas': 4500000}).revokeSLD(int(key, 16));
        print("Sending revokeSLD Tx")
        print("Tx Hash: " + result)
    else:
        print("This Tx will not be verified under this condition")
        howToUse(result)
elif (instr == "2" and len(sys.argv) == 8):
    key = sys.argv[2]
    validTime = sys.argv[3]
    to = sys.argv[4]
    v = sys.argv[5]
    r = sys.argv[6]
    s = sys.argv[7]
    result = contract.call({'from': defaultAccount}).changeOwner(int(key,16),int(validTime,10),to,int(v, 10), web3.toBytes(hexstr=r), web3.toBytes(hexstr=s));
    if (result > 0):
        result = contract.transact({'from': defaultAccount, 'gas': 4500000}).changeOwner(int(key, 16),int(validTime,10),
                                                                                         to,int(v, 10), web3.toBytes(hexstr=r), web3.toBytes(hexstr=s));
        print("Sending setOwner Tx")
        print("Tx Hash: " + result)
    else:
        print("This Tx will not be verified under this condition")
        howToUse(result)
else:
    howToUse(-3)
