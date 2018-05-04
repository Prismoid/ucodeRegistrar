var ucodeRegistrar = artifacts.require("./ucodeRegistrar.sol"); // デプロイするコントラクトを入れる

module.exports = function(deployer) {
    deployer.deploy(ucodeRegistrar); // デプロイするコントラクトを入れる
};
