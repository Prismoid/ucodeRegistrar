# coding:utf-8
from web3 import Web3, HTTPProvider, IPCProvider
from web3.contract import ConciseContract
import json
import sys

web3 = Web3(HTTPProvider('http://localhost:8545'))

def howToUse():
    print("--- how to use ---")
    print("1. lock default account: python3 AccountLock.py")
    sys.exit(1)

# arguments
if (len(sys.argv) !=  1): 
    howToUse()

# open account.dat
f = open("account.dat", "r")
defaultAccount = ""
for defaultAccount in f: 
    defaultAccount.strip()
f.close()

if (web3.personal.lockAccount(defaultAccount)):
    print("Locking Default Account: " + defaultAccount)
else:
    print("Fail to lock: " + defualtAccount)
    howToUse()






