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
var sign   = process.argv[3];

var result = 0;
// Test For Escrow
if (instr == 1) {
    // call pow Registrar
    result = 
    if (result >= 0) {
	console.log("send pow Registrar");
	// result = contract.powReg.sendTransaction(0x0120001122334455, web3.eth.blockNumber - 30, 3);
    } else {
	console.log("error code: " + result);
    }
} else if (instr == 1) {
    // call give right about ID Space
    result = contract.giveRight.call(new BigNumber("0x01100b1122334455", 16), web3.eth.blockNumber + 30, 3);
} else {
    console.log("No Instruction");
}

// show balances
// console.log(web3.eth.accounts[0] + ": " + web3.eth.getBalance(web3.eth.accounts[0]).toString());
console.log(web3.eth.accounts[1] + ": " + web3.fromWei(web3.eth.getBalance(web3.eth.accounts[1]).toString()));
console.log(web3.eth.accounts[2] + ": " + web3.fromWei(web3.eth.getBalance(web3.eth.accounts[2]).toString()));

