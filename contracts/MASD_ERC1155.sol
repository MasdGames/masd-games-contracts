// SPDX-License-Identifier: NONE
pragma solidity 0.8.6;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Supply.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Burnable.sol";

import "./utils/TokenActiveTillMixin.sol";
import "./utils/ContractURIMixin.sol";


contract MASD_ERC1155 is ERC1155, ERC1155Supply, ERC1155Burnable, Ownable, TokenActiveTillMixin, ContractURIMixin {
    mapping(uint256 /*tokenId*/ => /*explicit uri*/ string) _tokenURI;
    string public constant name = "MASD Assets";
    string public constant symbol = "MASD Assets";

    event DefaultTokenURISet(string uri);

    constructor(string memory uri, address ownerAddress) ERC1155(uri) Ownable() {
        if (msg.sender != ownerAddress) {
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

    function mintWithURI(
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data,
        string memory uri
    ) onlyOwner external {
        _mint(
            to,
            id,
            amount,
            data
        );
        setTokenURI(id, uri);
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

    function mintWithURIBatch(
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data,
        string[] memory uris
    ) external onlyOwner {
        require(ids.length == uris.length, "arrays mismatch");
        _mintBatch(
            to,
            ids,
            amounts,
            data
        );
        for (uint256 i = 0; i<ids.length; i++) {
            setTokenURI(ids[i], uris[i]);
        }
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

    function setDefaultTokenURI(string memory uri) external onlyOwner {
        _setURI(uri);
        emit DefaultTokenURISet(uri);
    }

    function setTokenURI(uint256 tokenId, string memory uri) public onlyOwner {
        _tokenURI[tokenId] = uri;
        emit URI(uri, tokenId);
    }

    /**
     * @dev See {IERC1155MetadataURI-uri}.
     *
     * This implementation returns the same URI for *all* token types. It relies
     * on the token type ID substitution mechanism
     * https://eips.ethereum.org/EIPS/eip-1155#metadata[defined in the EIP].
     *
     * Clients calling this function must replace the `\{id\}` substring with the
     * actual token type ID.
     */
    function uri(uint256 tokenId) public view virtual override returns (string memory) {
        string storage uri_ = _tokenURI[tokenId];
        if (bytes(uri_).length == 0) {
            return ERC1155.uri(tokenId);
        } else {
            return uri_;
        }
    }

    // just another name
    function tokenURI(uint256 tokenId) public view virtual returns (string memory) {
        return uri(tokenId);
    }
}
