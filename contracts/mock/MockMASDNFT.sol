// SPDX-License-Identifier: NONE
pragma solidity 0.8.6;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";


contract MockMASDNFT is ERC721, ERC721Enumerable, ERC721URIStorage, Ownable {
    uint256 internal _lastTokenId;
    mapping (uint256 => address) private _tokenAuthor;
    string internal _contractURI;

    event ContractURISet(string newContractURI);

    constructor(address ownerAddress) ERC721("MockMASDNFT", "MockMASDNFT") Ownable() {
        if (owner() != ownerAddress) {  // openzeppelin v4.1.0 has no _transferOwnership
            require(ownerAddress != address(0), "ZERO_ADDRESS");
            transferOwnership(ownerAddress);
        }
    }

    function _baseURI() override(ERC721) internal pure returns(string memory) {
        return "ipfs://";
    }

    function mintWithTokenURI(string memory _tokenIPFSHash) external returns (uint256) {
        require(bytes(_tokenIPFSHash).length > 0, "EMPTY_METADATA");
        uint256 tokenId = ++_lastTokenId;  // start from 1
        address to = _msgSender();
        _mint(to, tokenId);
        _tokenAuthor[tokenId] = to;
        _setTokenURI(tokenId, _tokenIPFSHash);
        return tokenId;
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
        delete _tokenAuthor[tokenId];
    }

    function tokenAuthor(uint256 tokenId) external view returns(address) {
        require(_exists(tokenId), "NOT_EXISTS");
        return _tokenAuthor[tokenId];
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
