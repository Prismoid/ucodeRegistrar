# coding:utf-8
from web3 import Web3, HTTPProvider, IPCProvider
from web3.contract import ConciseContract
import json
import sys

web3 = Web3(HTTPProvider('http://localhost:8545'))

def howToUse():
    print("--- how to use ---")
    print("1. unlock default account: python3 AccountUnlock.py \"passdword\" \"duration\"")
    sys.exit(1)

# arguments
if (len(sys.argv) !=  3): 
    howToUse()

# open account.dat
f = open("account.dat", "r")
defaultAccount = ""
for defaultAccount in f: 
    defaultAccount.strip()
f.close()

print(defaultAccount)
password = sys.argv[1]
duration = sys.argv[2]
if (not (duration.isdigit())):
    howToUse()
duration = int(duration, 10)
if (web3.personal.unlockAccount(defaultAccount, password, duration)):
    print("Unlock Default Account within " + str(duration) + " seconds")
else:
    print("Fail to unlock")
    howToUse()






