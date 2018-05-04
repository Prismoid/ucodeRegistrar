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
var value  = process.argv[3];

var result = 0;
// Test For Escrow
if (instr == 1) {
    // deposit 3 ether and issue 3 token
    console.log("deposit ether and issue token");
    contract.deposit.sendTransaction({from: web3.eth.accounts[1], to: addr, value: web3.toWei(value, "ether")});
} else if (instr == 2) {
    // send Token
    result = contract.payExcute.call(web3.eth.accounts[2], web3.toWei(value, "ether"), {from: web3.eth.accounts[1]});
    if (result) {
	console.log("send token");
	contract.payExcute.sendTransaction(web3.eth.accounts[2], web3.toWei(value, "ether"), {from: web3.eth.accounts[1]});
    }
} else if (instr == 3) {
    // withdraw ether
    result = contract.withdraw.call(web3.toWei(value, "ether"), {from: web3.eth.accounts[1]});
    if (result) {
	console.log("withdraw ether");
	result = contract.withdraw.sendTransaction(web3.toWei(value, "ether"), {from: web3.eth.accounts[1]});
    }
    console.log(result);
} else if (instr == 4) {
    // show the balances
    console.log("unlock, " + web3.eth.accounts[1] + ": " + web3.fromWei(contract.getBalance.call(web3.eth.accounts[1], 1)));
    console.log("lock,   " + web3.eth.accounts[1] + ": " + web3.fromWei(contract.getBalance.call(web3.eth.accounts[1], 2)));
    console.log("unlock, " + web3.eth.accounts[2] + ": " + web3.fromWei(contract.getBalance.call(web3.eth.accounts[2], 1)));
    console.log("lock,   " + web3.eth.accounts[2] + ": " + web3.fromWei(contract.getBalance.call(web3.eth.accounts[2], 2)));
} else {
    console.log("No Instruction, how to use");
    console.log("Deposit: node InstrDeposit.js 1 value");
    console.log("Send Token: node InstrDeposit.js 2 value");
    console.log("Withdraw: node InstrDeposit.js 3 value");
    console.log("Show balances: node InstrDeposit.js 4");
}

// show balances
// console.log(web3.eth.accounts[0] + ": " + web3.eth.getBalance(web3.eth.accounts[0]).toString());
console.log(web3.eth.accounts[1] + ": " + web3.fromWei(web3.eth.getBalance(web3.eth.accounts[1]).toString()));
console.log(web3.eth.accounts[2] + ": " + web3.fromWei(web3.eth.getBalance(web3.eth.accounts[2]).toString()));

