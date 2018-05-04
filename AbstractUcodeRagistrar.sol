pragma solidity ^0.4.21;

contract ucodeRegistrar {
  address public contrOwner;
  mapping (address => User) public user;
  mapping(uint120 => Record) public record; // version: 4bit, TLDc: 16bit, cc: 4bit, SLDc: 40bit, prefixLen: 8bit, prefix: 48bit


  // incr and pre-order param
  uint16 public incrTLDc; // [0x1000]
  uint56 public incrSLDc; // init: 1
  uint16 public preTLDc; // [0x1100]
  uint64 public preOrderN; // e.g. 100
  
  // events
  event NewOwner(uint80 key, address owner);
  event TransferRight(uint80 key, address owner);
  
  struct User {
    uint256 balance; // deposit & locked balance
    uint256 lockedBalance;
    bytes32 hash;
    uint64 blockHeight;
  }

  struct Record { // CC: b'1011, ID Prefix data
    address owner;
    uint64 timestamp;
  }
  
  // manipulating Token
  function deposit() payable public returns(bool);
  function payExcute(address _to, uint256 _money) public returns(bool);
  function withdraw(uint256 _money) public returns(bool);
  function getBalance(address _addr, uint8 _type) public returns(uint256);
  /*
  // update difficulty
  function updDiffTgt(uint32 _diff) public returns(bool);
  // manipulating ID Space
  function incrReg() public returns(int);
  function powReg(uint64 _inputKey, uint64 _blockHeight, address _sender, uint64 _nonce) public returns(int);
  function setSLDTimestamp(uint64 _sldKey, uint64 _timestamp) public returns(int);
  function revokeSLD(uint64 _sldKey) public returns(int);
  function setOwner(uint120 _key, uint64 _validTime, address _to, uint8 _v, bytes32 _r, bytes32 _s) public returns(int);
  function setSubspaceOwner(uint120 _key, uint64 _validTime, uint56 _prefix, uint64 _ttl, address _to,
                            uint8 _v, bytes32 _r, bytes32 _s) public returns(int);
  // get ID Space key's data
  function getAddr(uint120 _key) public returns(address);
  function getTimestamp(uint120 _key) public returns(uint64);

  // Logged when the owner of a node assigns a new owner to a subnode.
  event NewOwner(uint80 key, address owner);
  event TransferRight(uint80 key, address owner);
  */
}
