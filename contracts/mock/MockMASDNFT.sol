// SPDX-License-Identifier: NONE
pragma solidity 0.8.6;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";


contract MockMASDNFT is ERC721, ERC721Enumerable, ERC721URIStorage, Ownable {
    uint256 internal _lastTokenId;
    mapping (uint256 /*tokenId*/ => uint256 /*timestamp*/) internal _activeTill;
    string internal _contractURI;

    event ContractURISet(string newContractURI);
    event TokenActiveTillSet(uint256 tokenId, uint256 timestamp);

    function activeTill(uint256 tokenId) external view returns(uint256 timestamp) {
        return _activeTill[tokenId];
    }

    function _setTokenActiveTill(uint256 tokenId, uint256 timestamp) internal {
        require(timestamp >= block.timestamp, "invalid timestamp");
        _activeTill[tokenId] = timestamp;
        emit TokenActiveTillSet(tokenId, timestamp);
    }

    function isActive(uint256 tokenId) external view returns(bool) {
        return _activeTill[tokenId] > block.timestamp;
    }

    constructor(address ownerAddress) ERC721("MockMASDNFT", "MockMASDNFT") Ownable() {
        if (owner() != ownerAddress) {  // openzeppelin v4.1.0 has no _transferOwnership
            require(ownerAddress != address(0), "ZERO_ADDRESS");
            transferOwnership(ownerAddress);
        }
    }

    function _baseURI() override(ERC721) internal pure returns(string memory) {
        return "ipfs://";
    }

    function mintWithTokenURI(string memory _tokenIPFSHash) onlyOwner external returns (uint256) {
        require(bytes(_tokenIPFSHash).length > 0, "EMPTY_METADATA");
        uint256 tokenId = ++_lastTokenId;  // start from 1
        address to = _msgSender();
        _mint(to, tokenId);
        _setTokenURI(tokenId, _tokenIPFSHash);
        return tokenId;
    }

    function mintWithTokenURIAndActiveTill(string memory _tokenIPFSHash, uint256 activeTillTimestamp) onlyOwner external returns (uint256) {
        require(bytes(_tokenIPFSHash).length > 0, "EMPTY_METADATA");
        uint256 tokenId = ++_lastTokenId;  // start from 1
        address to = _msgSender();
        _mint(to, tokenId);
        _setTokenURI(tokenId, _tokenIPFSHash);
        _setTokenActiveTill(tokenId, activeTillTimestamp);
        return tokenId;
    }

    function setTokenActiveTill(uint256 tokenId, uint256 activeTillTimestamp) external onlyOwner {
        require(_exists(tokenId), "not exists");
        _setTokenActiveTill(tokenId, activeTillTimestamp);
    }

    function burn(uint256 tokenId) external {
        require(ERC721.ownerOf(tokenId) == msg.sender, "NOT_OWNER");
        _burn(tokenId);
    }

     function tokenURI(uint256 tokenId)
         public
         view
         override(ERC721, ERC721URIStorage)
         returns (string memory)
     {
         return super.tokenURI(tokenId);
     }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);  // take care about multiple inheritance
    }

    function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal override(ERC721, ERC721Enumerable) {
        ERC721Enumerable._beforeTokenTransfer(from, to, tokenId);
    }

    function supportsInterface(bytes4 interfaceId) public view override(ERC721, ERC721Enumerable) returns (bool) {
        return super.supportsInterface(interfaceId);
    }

    function contractURI() external view returns(string memory) {
        return _contractURI;
    }

    function setContractURI(string memory newContractURI) onlyOwner external {
        _contractURI = newContractURI;
        emit ContractURISet(newContractURI);
    }
}
