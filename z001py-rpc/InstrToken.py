# coding:utf-8
from web3 import Web3, HTTPProvider, IPCProvider
from web3.contract import ConciseContract
import json
import sys

web3 = Web3(HTTPProvider('http://localhost:8545'))
# web3 = Web3(HTTPProvider('https://ropsten.infura.io/liHdCRDQJCZoWgvxadDd'))
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

if (len(sys.argv) < 2):
    howToUse()
    
instr         = sys.argv[1] # 1: deposit, 2: withdraw, 3: send, 4: balance infomation 
depoistMoney  = 0
withdrawMoney = 0
sendMoney     = 0 

if (instr == "1" and len(sys.argv) == 3):
    try:  
        depositMoney = float(sys.argv[2])
        result = contract.call({'from': defaultAccount, 'to': addr, 'value': web3.toWei(depositMoney, "ether")}).deposit()
        if (result):
            result = contract.transact({'from': defaultAccount, 'to': addr, 'value': web3.toWei(depositMoney, "ether")}).deposit()
            print("Deposit " + str(depositMoney) + " ether")
            print("Tx Hash: " + result)
        else:
            print("This Tx will not be verified under this condition")
            howToUse()
    except: 
        import traceback
        traceback.print_exc()
elif (instr == "2" and len(sys.argv) == 3):
    try:
        withdrawMoney = float(sys.argv[2])
        result = contract.call({'from': defaultAccount}).withdraw(web3.toWei(withdrawMoney, "ether"))
        if (result):
            result = contract.transact({'from': defaultAccount}).withdraw(web3.toWei(withdrawMoney, "ether"))
            print("Withdraw " + str(withdrawMoney) + " token")
            print("Tx Hash: " + result)
        else:
            print("This Tx will not be verified under this condition")
            howToUse()
    except:
        import traceback
        traceback.print_exc()
elif (instr == "3" and len(sys.argv) == 4):
    try:
        to = sys.argv[2]
        if (not (web3.isAddress(to))):
            print("Receiver's Address is not valid")
            howToUse()
        sendMoney = float(sys.argv[3])
        result = contract.call({'from': defaultAccount}).payExcute(to, web3.toWei(sendMoney, "ether"))
        if (result):
            result = contract.transact({'from': defaultAccount}).payExcute(to, web3.toWei(sendMoney, "ether"))
            print("Send " + str(sendMoney) + " token to " + to)
            print("Tx Hash: " + result)
        else:
            print("This Tx will not be verified under this condition")
            howToUse()
    except: 
        import traceback
        traceback.print_exc()
elif (instr == "4" and len(sys.argv) == 2):
    print("--- Displaying local node's accounts's deposit data ---")
    if (len(web3.eth.accounts) == 0):
        print("There are no accounts on local node")
        howToUse()
    for i in range(len(web3.eth.accounts)):
        print("*** user[" + str(i) + "]: " + web3.eth.accounts[i].capitalize())
        print("unlock: " + str(web3.fromWei(contract.call({'from': defaultAccount}).getBalance(web3.eth.accounts[i], 1), 'ether')) + " token");
        print("lock:   " + str(web3.fromWei(contract.call({'from': defaultAccount}).getBalance(web3.eth.accounts[i], 2), 'ether')) + " token");
        print("ether:   " + str(web3.fromWei(web3.eth.getBalance(web3.eth.accounts[i]), 'ether')) + " ether");
else:
    howToUse()
