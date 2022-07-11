// SPDX-License-Identifier: NONE
pragma solidity 0.8.6;

import "@openzeppelin/contracts/access/Ownable.sol";


contract ContractURIMixin is Ownable {
    string internal _contractURI;

    event ContractURISet(string newContractURI);

    function contractURI() external view returns(string memory) {
        return _contractURI;
    }

    function setContractURI(string memory newContractURI) onlyOwner external {
        _contractURI = newContractURI;
        emit ContractURISet(newContractURI);
    }
}
