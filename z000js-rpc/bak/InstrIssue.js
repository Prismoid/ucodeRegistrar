// external library
const BigNumber = require("bignumber.js");
const Web3 = require("web3");
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
web3.eth.defaultAccount = web3.eth.accounts[1];

// making a contract instance (Test)
var contract_json = require('../build/contracts/RangedIDRegistrar.json');
var addr = contract_json.networks[1].address;
var abi = contract_json.abi;
var contract = web3.eth.contract(abi).at(addr);

var instr  = process.argv[2];
var data   = process.argv[3];
var nonce  = 3;

var result = 0;
// Test For Escrow
if (instr == 1) {
    // call incremnt Registrar
    result = contract.incrReg.call();
    if (result >= 0) {
	console.log("send incremnt Registrar");
	result = contract.incrReg.sendTransaction();
    } else {
	console.log("error code: " + result);
    }
} else if (instr == 2) {
    // call pow Registrar
    result = contract.powReg.call(new BigNumber("0x01100b" + data, 16), web3.eth.blockNumber - 30, web3.eth.accounts[1], nonce);
    if (result >= 0) {
	console.log("send pow Registrar");
	result = contract.powReg.sendTransaction("0x01100b" + data, web3.eth.blockNumber - 30, web3.eth.accounts[1], nonce);
    } else {
	console.log("error code: " + result);
    }
} else if (instr == 3) {
    // show the balances
    console.log("unlock, " + web3.eth.accounts[1] + ": " + web3.fromWei(contract.getBalance.call(web3.eth.accounts[1], 1)));
    console.log("lock,   " + web3.eth.accounts[1] + ": " + web3.fromWei(contract.getBalance.call(web3.eth.accounts[1], 2)));
    console.log("unlock, " + web3.eth.accounts[2] + ": " + web3.fromWei(contract.getBalance.call(web3.eth.accounts[2], 1)));
    console.log("lock,   " + web3.eth.accounts[2] + ": " + web3.fromWei(contract.getBalance.call(web3.eth.accounts[2], 2)));
} else {
    console.log("No Instruction");
    console.log("Increment Register: node InstrIssue.js 1");
    console.log("PoW Register: node InstrIssue.js 2 1122334455");
}

// show balances
// console.log(web3.eth.accounts[0] + ": " + web3.eth.getBalance(web3.eth.accounts[0]).toString());
console.log(web3.eth.accounts[1] + ": " + web3.fromWei(web3.eth.getBalance(web3.eth.accounts[1]).toString()));
console.log(web3.eth.accounts[2] + ": " + web3.fromWei(web3.eth.getBalance(web3.eth.accounts[2]).toString()));

