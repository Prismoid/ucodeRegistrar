# coding:utf-8
from web3 import Web3, HTTPProvider, IPCProvider
from web3.contract import ConciseContract
import json
import sys
import time
from multiprocessing import Pool
from multiprocessing import Process

web3 = Web3(HTTPProvider('http://localhost:8545'))

inputKey = 0x01100b0000000001
curHash  = "0x0001020304050607080910111213141516171819202122232425262728293031"
defaultAccount = "0xcd669c440a31f6f54a0fa583abf76fd2badeede7"

# python multicore: https://qiita.com/yotayokuto/items/23798d5fc75017d5a8b3
def PoW(nonce):
    if (int(web3.soliditySha3(['uint64', 'bytes32', 'address', 'uint64'], [inputKey, curHash, defaultAccount, nonce]), 16) <= 0xf0000000000000000000000000000000000000000000000000000000000):
        return nonce
    else:
        return 0

def multi(start, end):
    p = Pool(12)
    result = p.map(PoW, range(start, end + 1, 1))
    return result
    


web3 = Web3(IPCProvider())
start = time.time()
result = multi(0, 1000000)
for i in result:
    if (result[i] != 0):
        print(result[i])
    
elapsed_time = time.time() - start

print(str(float(1000000) / (elapsed_time)) + "[hash/sec]")
print(str(elapsed_time) + "[sec]")
    

