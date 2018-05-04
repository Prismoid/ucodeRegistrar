# coding:utf-8
from web3 import Web3, HTTPProvider, IPCProvider
from web3.contract import ConciseContract
import json
import sys

web3 = Web3(HTTPProvider('http://localhost:8545'))

def howToUse():
    print("--- how to use ---")
    print("1. configure defualt account: python3 AccountConfig.py 1 \"Account Index\"")
    sys.exit(1)

# arguments
if (len(sys.argv) < 2): 
    howToUse()

instr = sys.argv[1]
address = ""
accountIndex = 0
if (instr == "1" and len(sys.argv) == 3): #and len(sys.argv) == 3):
    accountIndex = int(sys.argv[2])
    if (len(web3.eth.accounts) <= accountIndex):
        print("This index exceeds the list of \"accounts\"")
        howToUse()
    address = (web3.eth.accounts[accountIndex]).capitalize()
    if (not (web3.isAddress(address))):
        howToUse()
else:
    howToUse()

# open account.dat
f = open("account.dat", "w")
f.write(address)
print("Setting default account: " + address)
f.close()







