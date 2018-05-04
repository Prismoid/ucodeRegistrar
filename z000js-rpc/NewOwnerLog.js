// external library
const BigNumber = require("bignumber.js");
var leftPad = require('left-pad');
const Web3 = require("web3");
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
web3.eth.defaultAccount = web3.eth.accounts[1];

// making a contract instance (Test)
var contract_json = require('../build/contracts/ucodeRegistrar.json');
var addr = contract_json.networks[10].address;
var abi = contract_json.abi;
var contract = web3.eth.contract(abi).at(addr);


var tgtAnt = process.argv[2];
var locNum = process.argv[3];
var flag   = 0;
if (tgtAnt === "Local" && locNum < web3.eth.accounts.length) {
    tgtAnt = web3.eth.accounts[locNum];
    flag = 1;
} else if (3 <= process.argv.length) {
    tgtAnt = process.argv[2];
    flag = 2;
} else {
    console.log("--- How to use ---");
    console.log("1. node NewOwnerLog.js Local i (local account number)");
    console.log("2. node NewOwnerLog.js \"0xcd669c440a31f6f54a0fa583abf76fd2badeede7\"");
    return false;
}   

var event = contract.NewOwner();
if (flag == 1) {
    console.log("--- Following ID Sapces belong to owner( " + web3.eth.accounts[locNum] + " ) ---");
} else if (flag == 2) {
    console.log("--- Following ID Sapces belong to owner( " + tgtAnt + " ) ---");
} else {
    console.log("--- How to use ---");
    console.log("1. node NewOwnerLog.js Local i (local account number)");
    console.log("2. node NewOwnerLog.js \"0xcd669c440a31f6f54a0fa583abf76fd2badeede7\"");
    return false;
}

var cnt = 0;  
contract.NewOwner({}, { fromBlock: 0, toBlock: 'latest' }).get((error, results) => {
    if (flag == 1) {
	for (var i = 0; i < results.length; i++) {
	    if (results[i].args.owner === web3.eth.accounts[locNum]) {
		var curPrefix = "0x" + leftPad(web3.toHex(results[i].args.key).slice(2).toString(16), 20, 0);
		var revokeFlag = contract.getAddr.call(curPrefix);
		if (revokeFlag === web3.eth.accounts[locNum]) { 
		    console.log((cnt + 1) + ": " + curPrefix + ", state: validated")
		} else {
		    console.log((cnt + 1) + ": " + curPrefix + ", state: revoked")
		}
		cnt += 1;
	    }
	} 
    } else if (flag == 2) {
	for (var i = 0; i < results.length; i++) {
	    if (results[i].args.owner === tgtAnt) {
		var curPrefix = "0x" + leftPad(web3.toHex(results[i].args.key).slice(2).toString(16), 20, 0);
		var revokeFlag = contract.getAddr.call(curPrefix);
		if (revokeFlag === tgtAnt) { 
		    console.log((cnt + 1) + ": " + curPrefix + ", state: validated")
		} else {
		    console.log((cnt + 1) + ": " + curPrefix + ", state: revoked")
		}
		cnt += 1;
	    }
	} 
    }
    if ((flag == 1 || flag == 2) && cnt == 0) {
	console.log("No ID Sapace is acquired by this account");
    }
});
