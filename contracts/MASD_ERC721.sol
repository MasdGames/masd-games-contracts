// SPDX-License-Identifier: NONE
pragma solidity 0.8.6;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

import "./utils/TokenActiveTillMixin.sol";
import "./utils/ContractURIMixin.sol";


contract MASD_ERC721 is
    ERC721,
    ERC721Enumerable,
    ERC721URIStorage,
    Ownable,
    TokenActiveTillMixin,
    ContractURIMixin
{
    string public baseURI;

    event BaseURISet(string newBaseURI);

    constructor(address ownerAddress) ERC721("MASD NFT", "MASD NFT") Ownable() {
        if (owner() != ownerAddress) {
            transferOwnership(ownerAddress);
        }
    }

    function setBaseURI(string memory uri) external onlyOwner {
        baseURI = uri;
        emit BaseURISet(uri);
    }

    function _baseURI() override(ERC721) internal view returns(string memory) {
        return baseURI;
    }

    function mint(address to, uint256 tokenId) external onlyOwner {
        _mint(to, tokenId);
    }

    function mintWithURI(address to, uint256 tokenId, string memory uri) external onlyOwner {
        _mint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }

    function mintWithURIBatch(address[] memory tos, uint256[] memory tokenIds, string[] memory uris) external onlyOwner {
        require(tokenIds.length == tos.length, "arrays mismatch");
        require(tokenIds.length == uris.length, "arrays mismatch");
        for (uint256 i=0; i<tokenIds.length; i++) {
            _mint(tos[i], tokenIds[i]);
            _setTokenURI(tokenIds[i], uris[i]);
        }
    }

    function mintWithURIAndActiveTill(address to, uint256 tokenId, string memory uri, uint256 activeTillTimestamp) external onlyOwner {
        _mint(to, tokenId);
        _setTokenURI(tokenId, uri);
        setTokenActiveTill(tokenId, activeTillTimestamp);
    }

    function mintWithURIAndActiveTillBatch(address[] memory tos, uint256[] memory tokenIds, string[] memory uris, uint256[] memory activeTillTimestamps) external onlyOwner {
        require(tokenIds.length == tos.length, "arrays mismatch");
        require(tokenIds.length == uris.length, "arrays mismatch");
        require(tokenIds.length == activeTillTimestamps.length, "arrays mismatch");
        for (uint256 i=0; i<tokenIds.length; i++) {
            _mint(tos[i], tokenIds[i]);
            _setTokenURI(tokenIds[i], uris[i]);
            setTokenActiveTill(tokenIds[i], activeTillTimestamps[i]);
        }
    }

    function burn(uint256 tokenId) external {
        require(_isApprovedOrOwner(msg.sender, tokenId), "no permission");
        _burn(tokenId);
    }

    function burnBatch(uint256[] memory tokenIds) external {
        for (uint256 i=0; i<tokenIds.length; i++) {
            require(_isApprovedOrOwner(msg.sender, tokenIds[i]), "no permission");
            _burn(tokenIds[i]);
        }
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

    function transferFromBatch(
        address[] memory froms,
        address[] memory tos,
        uint256[] memory tokenIds
    ) external {
        require(froms.length == tos.length, "arrays mismatch");
        require(froms.length == tokenIds.length, "arrays mismatch");
        for (uint256 i=0; i<froms.length; i++) {
            transferFrom(froms[i], tos[i], tokenIds[i]);
        }
    }

    /**
     * @dev See {IERC721-safeTransferFrom}.
     */
    function safeTransferFromBatch(
        address[] memory froms,
        address[] memory tos,
        uint256[] memory tokenIds,
        bytes[] memory _datas
    ) external {
        require(froms.length == tos.length, "arrays mismatch");
        require(froms.length == tokenIds.length, "arrays mismatch");
        require(froms.length == _datas.length, "arrays mismatch");
        for (uint256 i=0; i<froms.length; i++) {
            safeTransferFrom(froms[i], tos[i], tokenIds[i], _datas[i]);
        }
    }
}
