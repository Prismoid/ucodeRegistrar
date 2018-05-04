# Caution!
To be determined...

## usage
To be determined...

### This memo for me
[Error: Exceeds block gas limitとなる場合の解決方法]
https://github.com/trufflesuite/truffle/issues/271

[truffle.js]
どのEthereumネットワークに接続するか、Gas Limitの設定、rpcなどなど

[デプロイしたコントラクトの呼び方]
truffle compile # ./contracts以下の.solファイルをコンパイルする
truffle migrate # ./migrates以下の指示通りにEthereumネットワークにdeployする(マイニングしている必要あり)
truffle console # コンソールモードで起動

*** console 内において ***
HelloWorld.deployed().then(function(instance) {app = instance;})

以下のようにして関数や変数の呼び出しを実行できる

app.creator.call()
app.message.call()

*** トランザクションの発行方法 ***

以下のようにする。基本的にweb3を介するだけで同じ

app.getMessage.sendTransaction({frmo: web3.eth.accounts[0]})

*** デプロイのやり直し ***
rm -rf buildを実行してからコンパイルし直す ---> うまくいかない場合多い
truffle migrate --reset --all がいい可能性が高い

