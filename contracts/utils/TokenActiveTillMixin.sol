// SPDX-License-Identifier: NONE
pragma solidity 0.8.6;

import "@openzeppelin/contracts/access/Ownable.sol";


abstract contract TokenActiveTillMixin is Ownable {
    mapping (uint256 /*tokenId*/ => uint256 /*timestamp*/) internal _activeTill;

    event TokenActiveTillSet(uint256 tokenId, uint256 timestamp);

    function activeTill(uint256 tokenId) public view returns(uint256 timestamp) {
        return _activeTill[tokenId];  // 0 means forever
    }

    // does not check existence of the token, return True for non-existant tokens.
    function isActive(uint256 tokenId) public view returns(bool) {
        return (_activeTill[tokenId] == 0) || (_activeTill[tokenId] > block.timestamp);
    }

    function setTokenActiveTill(uint256 tokenId, uint256 activeTillTimestamp) public onlyOwner {
        require(activeTillTimestamp >= block.timestamp, "invalid timestamp");
        _activeTill[tokenId] = activeTillTimestamp;
        emit TokenActiveTillSet(tokenId, activeTillTimestamp);
    }
}
