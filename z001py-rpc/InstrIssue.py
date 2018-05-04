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
    print("1. increment: python3 InstrIssue.py 1")
    print("2. pre-order1: python3 InstrIssue.py 2 \"target ucode's prefix key(80bit)\" \"nonce\"")
    print("3. pre-order2: python3 InstrIssue.py 3 \"target ucode's prefix key(80bit)\" \"nonce\"")
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

if (len(sys.argv) < 2):
    howToUse(-1)
    
instr = sys.argv[1] # 1: increment issue, 2: pow issue 

if (instr == "1" and len(sys.argv) == 2):
    finFlag = 0
    try:  
        result = contract.call({'from': defaultAccount}).incrReg()
        if (result > 0):
            result = contract.transact({'from': defaultAccount, 'gas': 4500000}).incrReg()
            print("Sending Increment Tx")
            print("Tx Hash: " + result)
        else:
            print("This Tx will not be verified under this condition")
            howToUse(result)            
    except: 
        import traceback
        traceback.print_exc()
elif (instr == "2" and len(sys.argv) == 4):
    key = sys.argv[2] # 80 bit strings
    nonce = sys.argv[3]
    timestamp = contract.call({'from': defaultAccount}).getTimestamp(int(key, 16))
    print("pre-order Hash: " + web3.soliditySha3(['uint80', 'uint64'], [int(key, 16), int(nonce, 16)]))    
    result = contract.call({'from': defaultAccount}).preOrderReg1(web3.toBytes(hexstr=web3.soliditySha3(['uint80', 'uint64'], [int(key, 16), int(nonce, 16)])))
    if (result > 0):
        result = contract.transact({'from': defaultAccount}).preOrderReg1(web3.toBytes(hexstr=web3.soliditySha3(['uint80', 'uint64'], [int(key, 16), int(nonce, 16)])))
        print("Sending pre-order1 Tx")
        print("Tx Hash: " + result)

    else:
            print("This Tx will not be verified under this condition")
            howToUse(result)
elif (instr == "3" and len(sys.argv) == 4):
    key = sys.argv[2] # 80 bit strings
    nonce = sys.argv[3]
    result = contract.call({'from': defaultAccount}).preOrderReg2(int(key, 16), int(nonce, 16))
    print(result)
    if (result > 0):
        result = contract.transact({'from': defaultAccount, 'gas': 4500000}).preOrderReg2(int(key, 16), int(nonce, 16))
        print("Sending pre-order2 Tx")
        print("Tx Hash: " + result)

    else:
            print("This Tx will not be verified under this condition")
            howToUse(result)
else:
    howToUse(-3)
