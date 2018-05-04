// external library
var date = new Date();
const BigNumber = require("bignumber.js");
var leftPad = require('left-pad');
var web3utils = require('web3-utils');
const Web3 = require("web3");
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

// default account
var fs = require('fs');
var content = fs.readFileSync('../z001py-rpc/account.dat', 'utf8');
var defaultAccount = content.toString();
web3.eth.defaultAccount = defaultAccount;

// making a contract instance (Test)
var contract_json = require('../build/contracts/ucodeRegistrar.json');
var addr = contract_json.networks[10].address;
var abi = contract_json.abi;
var contract = web3.eth.contract(abi).at(addr);

var tgtAnt = process.argv[2]
var key = process.argv[3];
var validTime = Number(process.argv[4]) + Math.floor((date.getTime()) / 1000);
var prefix = process.argv[5];
var ttl = process.argv[6];
var flag   = 0;
if (tgtAnt === "1" && 5  == process.argv.length) {
    flag = 1;
} else if (tgtAnt === "2" && 7 == process.argv.length) {
    flag = 2;
} else {
    console.log("--- How to use ---");
    console.log("1. node InstrSign.js 1 key(80bit) validTime(64bit)");
    return false;
}   

if (flag == 1) {
    var msg = web3utils.soliditySha3({t: "uint80", v: key}, {t: "uint64", v: validTime});
    var sig = web3.eth.sign(defaultAccount, msg);
    console.log(sig)    
    var v = parseInt(sig.slice(130,132), 16); // This is only a variable of numeric type.
    var r = sig.slice(0,66);
    var s = '0x' + sig.slice(66,130);
    console.log(sig)
    console.log(v)
    console.log("--- set owner transaction's arguments ---")
    console.log("key, validTime, to, v, r, s: " + key + " " + validTime + " " + defaultAccount + " " + v + " " + r + " " + s);
    console.log("Test: " + contract.changeOwner.call(key, validTime, defaultAccount, v, r, s))
} else {
    console.log("--- How to use ---");
    console.log("1. node InstrSign.js 1 key(80bit) validTime(64bit)");
    return false;
}
