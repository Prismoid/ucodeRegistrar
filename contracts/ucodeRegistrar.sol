pragma solidity ^0.4.21;
contract ucodeRegistrar {
  // contract owner
  address public contrOwner = msg.sender; 

  // Token & Pre-Order Hash mapping
  mapping (address => User) public user; 
  struct User {
    uint256 balance; // deposit & locked balance
    uint256 lockedBalance;
    bytes32 hash; // for pre-order
    uint64 blockHeight;
  }

  // ucode bulked mapping
  mapping(uint80 => Record) public record; // version: 4bit, TLDc: 16bit, cc: 4bit, SLDc: 56bit (IC: 48bit)
  struct Record { // CC: b'1100, ID Prefix data
    address owner;
    uint64 timestamp;
  }

  // incr and pre-order param
  uint16 public incrTLDc; // [0x1000]
  uint56 public incrSLDc;
  uint16 public preTLDc; // [0x1100]
  uint64 public preOrderN; // e.g. n = 100

  // Events
  event NewOwner(uint80 key, address owner);
  event TransferRight(uint80 key, address owner);

  // constructor 
  constructor(){
    // incr parameter
    incrTLDc = 0x1000; 
    incrSLDc = 1;
    // pre-order pram
    preTLDc  = 0x1100;
    preOrderN = 3; // for Test
  }

  // deposit function
  function deposit() payable public returns(bool){
    if (msg.value > 0
	&& (user[msg.sender].balance + msg.value) > user[msg.sender].balance) {
      user[msg.sender].balance += msg.value;
      return true;
    }
    return false;
  }
  // pay token function 
  function payExcute(address _to, uint256 _money) public returns(bool){
    if (user[msg.sender].balance >= _money
        && _money > 0
        && (user[_to].balance + _money) > user[_to].balance) {
      user[msg.sender].balance -= _money;
      user[_to].balance += _money;      
      return true;
    }
    return false;
  }
  // withdraw eth
  function withdraw(uint256 _money) public returns(bool){
    if (_money <= user[msg.sender].balance
        && _money > 0) {
      if (true == msg.sender.send(_money)) {
	user[msg.sender].balance -= _money;
	return true;
      }
    }
    return false;
  }
  // check account's balance
  function getBalance(address _addr, uint8 _type) public returns(uint256){
    if (_type == 1) {
      return user[_addr].balance;
    } else if (_type == 2) {
      return user[_addr].lockedBalance;
    } else {
      return 0;
    }
  }

  // increment reg
  function incrReg() public returns(bool) {
    // keyHead: 0x01000b, keyEnd: [0x0000000000_00_000000000000, 0xffffffffff_00_000000000000]
    uint24 keyHead = ((uint24(0xffffff) & (uint24(incrTLDc)) << 4) + uint24(0xc));
    uint80 key = (uint80(keyHead) << 56) + uint80(incrSLDc);

    if ((uint56(0xffffffffffffff) & incrSLDc) < uint56(0xffffffffffffff) // always succeeding in this function without the case of issuing all IDs
	&& !(user[msg.sender].balance < 0.01 ether)) { // check insufficient deposit
      // update database
      user[msg.sender].balance       -= 0.01 ether;
      user[msg.sender].lockedBalance += 0.01 ether;
      record[key].owner      = msg.sender;
      record[key].timestamp  = uint64(block.timestamp); // current block time
      
      // increment index and TLDc
      incrSLDc += 1;
      
      emit NewOwner(key, msg.sender);
      return true;
    }
    return false;
  }
  
  // pre-order
  function preOrderReg1(bytes32 _hash) public returns(bool){
    user[msg.sender].hash = _hash;
    user[msg.sender].blockHeight = uint64(block.number);
    return true;
  }
  function preOrderReg2(uint80 _key, uint64 _nonce) public returns(bool){
    uint8 version = uint8(_key >> 76); 
    uint16 TLDc = uint16(_key >> 60); 
    uint8 CC = uint8(_key >> 56) - ((uint8(TLDc) & 0x0f) << 4);
    uint56 SLDc = uint56(_key);
    bytes32 curHash = sha3(_key, _nonce);

    if (!(version != 0)     // version Error
	&& (TLDc == 0x1000 ||  TLDc == 0x1100) // TLDc OK
	&& !(CC != 12)     // CC Error
	&& !(record[_key].timestamp != 0)     // this SLDc's ucode isn't revoked
	&& !(user[msg.sender].hash != curHash)     // don't match hash value
	&& !(user[msg.sender].blockHeight + preOrderN  > block.number)     // check the block height
	&& !(user[msg.sender].balance < 0.01 ether)) {    // check the deposit value
      if (TLDc == 0x1000) {
	if (SLDc >= incrSLDc) { return false; }
      }
	
      // Issuing ID Space, Giving Ownership to the sender
      user[msg.sender].balance       -= 0.01 ether;
      user[msg.sender].lockedBalance += 0.01 ether;
      record[_key].owner      = msg.sender;
      record[_key].timestamp  = uint64(block.timestamp);
      NewOwner(_key, msg.sender);
      return true;
    }
    return false;
  }

  // revoke ucode
  function revokeSLD(uint80 _key) public returns(bool){
    if (!(record[_key].owner != msg.sender)     // check owner addr
	&& !(record[_key].timestamp == 0)    // check timestamp's value
	&& !(block.timestamp <= record[_key].timestamp + 1 years)) {     // if block.timestamp <= record[_key].timestamp + 90 days, this ID Space can't be revoked
      // update database
      record[_key].timestamp = 0;
      user[msg.sender].lockedBalance -= 0.01 ether;
      user[msg.sender].balance += 0.01 ether;
      return true;
    }
    return false;
  }

  function changeOwner(uint80 _key, uint64 _validTime, address _to, uint8 _v, bytes32 _r, bytes32 _s) public returns(bool){
    // how to use ecrecover: https://ethereum.stackexchange.com/questions/15364/ecrecover-from-geth-and-web3-eth-sign
    bytes memory prefix = "\x19Ethereum Signed Message:\n32";
    bytes32 prefixedHash = keccak256(prefix, sha3(_key, _validTime));
    if (!(record[_key].timestamp == 0)     // check timestamp != 0,
	&& !(record[_key].owner != msg.sender)     // check owner
	&& !(ecrecover(prefixedHash, _v, _r, _s) != _to)  // verify receiver's sign
	&& !(block.timestamp > _validTime)     // check block timestamp
	&& !(msg.sender == _to) // check sender's addr and receiver's addr
	&& !(user[_to].balance < 0.01 ether)) {     // check receiver's balance	
      // update Database
      record[_key].owner = _to;
      user[msg.sender].lockedBalance -= 0.01 ether;
      user[msg.sender].balance += 0.01 ether;
      user[_to].balance -= 0.01 ether;
      user[_to].lockedBalance += 0.01 ether;
      NewOwner(_key, _to);
      return true;
    }
    return false;
  }
  
  // check key's owner
  function getAddr(uint80 _key) public returns(address){
    // keyHead: 0x01***b, keyEnd: [0x0000000000_00_000000000000, 0xffffffffff_00_000000000000]
    return record[_key].owner;
  }
  // check owner's timestamp
  function getTimestamp(uint80 _key) public returns(uint64){
    // timestamp: e.g. 0x0011223344556677,
    // if this ID Space is not root of SLD, TTL(Time To Live)
    // if this ID Space is root of SLD, timestamp represents a time of getting this ID Space
    return record[_key].timestamp;
  }
  function getPreOrderHash(address _key) public returns(uint256){
    return uint256(user[_key].hash);
  }
  function getPreOrderBlockHeight(address _key) public returns(uint64){
    return user[_key].blockHeight;
  }
}
