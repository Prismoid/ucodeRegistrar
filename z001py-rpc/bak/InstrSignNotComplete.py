# coding:utf-8
from web3 import Web3, HTTPProvider, IPCProvider
from web3.contract import ConciseContract
from eth_utils import decode_hex
import json
import sys
import time

web3 = Web3(HTTPProvider('http://localhost:8545'))
# web3 = Web3(IPCProvider())

def howToUse(result):
    print("--- how to use ---")
    print("1. setOwner(Sign): python3 InstrSign.py 1")
    sys.exit(result)

# creating contract object
f = open("../build/contracts/RangedIDRegistrar.json")
contract_json = json.load(f)
f.close()
addr = contract_json["networks"]["1"]["address"]
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
    
instr = sys.argv[1] # 1: 

if (instr == "1" and len(sys.argv) == 4):
    key = sys.argv[2] # 120 bit
    addTime = sys.argv[3] # 秒
    validTime = int(addTime) + int(time.time())
    validTime = '0x{:02x}'.format(validTime)    
    message = web3.soliditySha3(['uint120', 'uint64'], [int(key, 16), int(validTime, 16)])
    # print(str(web3.sha3(key, validTime)))
    signData = web3.eth.sign(defaultAccount, decode_hex(web3.sha3(key, validTime)))
    v = int(signData, 16) & int("0xff", 16)
    r = (int(signData, 16) >> 264) & int("0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 16)
    s = int(signData, 16 >> 8) & int("0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 16)

    v = v + 27 # 数値
    r = '0x{:02x}'.format(r)
    s = '0x{:02x}'.format(s)    

    print("key, time, addr, v, r, s: " + key + ", " + validTime + ", " + str(defaultAccount) + ", " + str(v) + ", " + r + ", " + s)
    
    '''
    result = contract.call({'from': defaultAccount}).preOrderReg1(web3.toBytes(hexstr=web3.soliditySha3(['uint64', 'uint64'], [int(key, 16), int(nonce, 16)])))
    if (result > 0):
        result = contract.transact({'from': defaultAccount}).preOrderReg1(web3.toBytes(hexstr=web3.soliditySha3(['uint64', 'uint64'], [int(key, 16), int(nonce, 16)])))
        print("Sending pre-order1 Tx")
        print("Tx Hash: " + result)

    else:
            print("This Tx will not be verified under this condition")
            howToUse(result)
    '''
else:
    howToUse(-3)
