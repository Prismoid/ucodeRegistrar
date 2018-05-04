/*** 外部ライブラリの読み込み ***/
// 関数呼び出し用
var BigNumber = require('bignumber.js'); // npm install bignumber, https://www.npmjs.com/package/bignumber.js
var leftPad = require('left-pad'); // npm install left-pad, https://www.npmjs.com/package/left-padのサイトとかにある
var web3utils = require('web3-utils'); // npm install web3-utils, https://www.npmjs.com/package/web3-utilsなど
// Web3のインスタンスの作成
var Web3 = require('web3');
var web3 = new Web3();
web3.setProvider(new web3.providers.HttpProvider('http://localhost:8545'));
web3.eth.defaultAccount = web3.eth.accounts[1];

// コントラクトのインスタンスを作成
var contract_json1 = require('../build/contracts/RangedIDRegistrar.json');
var addr1 = contract_json1.networks[1].address;
var abi1 = contract_json1.abi;
var test1 = web3.eth.contract(abi1).at(addr1);

var contract_json2 = require('../build/contracts/PublicResolver.json');
var addr2 = contract_json2.networks[1].address;
var abi2 = contract_json2.abi;
var test2 = web3.eth.contract(abi2).at(addr2);


var result;
result = test2.setAddr.call(addr1);
if (result) {
    console.log("Send Transaction which Sets Address");
    test2.setAddr.sendTransaction(addr1);
} else {
    console.log("Cannot Send Transaction which Sets Address");
}
