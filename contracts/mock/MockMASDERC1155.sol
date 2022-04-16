// SPDX-License-Identifier: NONE
pragma solidity 0.8.6;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Supply.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Burnable.sol";


contract MockMASDERC1155 is ERC1155, ERC1155Supply, ERC1155Burnable, Ownable {
    string internal _contractURI;

    string public constant name = "MockMASDERC1155";
    string public constant symbol = "MockMASDERC1155";

    event ContractURISet(string newContractURI);

    constructor(string memory uri, address ownerAddress) ERC1155(uri) Ownable() {
        if (owner() != ownerAddress) {  // openzeppelin v4.1.0 has no _transferOwnership
            require(ownerAddress != address(0), "ZERO_ADDRESS");
            transferOwnership(ownerAddress);
        }
    }

    function mint(
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) onlyOwner external {
        _mint(
            to,
            id,
            amount,
            data
        );
    }

    function mintBatch(
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) external onlyOwner {
        _mintBatch(
            to,
            ids,
            amounts,
            data
        );
    }

    function contractURI() external view returns(string memory) {
        return _contractURI;
    }

    function setContractURI(string memory newContractURI) onlyOwner external {
        _contractURI = newContractURI;
        emit ContractURISet(newContractURI);
    }

    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) internal override(ERC1155, ERC1155Supply) {
        ERC1155Supply._beforeTokenTransfer(
            operator,
            from,
            to,
            ids,
            amounts,
            data
        );
    }
}
