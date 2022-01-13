// SPDX-License-Identifier: NONE
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import '@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol';


import "./MASD.sol";
import "./MASDVesting.sol";


contract TransferableMASDVestingProxy is Ownable {
    using SafeERC20 for IERC20;

    MASDVesting vesting;
    IERC20 MASDCoin;

    constructor(address _vesting, address _MASDCoin) {
        require(_vesting != address(0), "ZERO_ADDRESS");
        require(_MASDCoin != address(0), "ZERO_ADDRESS");
        vesting = MASDVesting(_vesting);
        MASDCoin = IERC20(_MASDCoin);
    }

    function withdraw(uint256 userVestingId) external onlyOwner {
        vesting.withdraw(userVestingId);
        MASDCoin.safeTransfer(owner(), MASDCoin.balanceOf(address(this)));
    }

    function withdrawAll() external onlyOwner {
        vesting.withdrawAll();
        MASDCoin.safeTransfer(owner(), MASDCoin.balanceOf(address(this)));
    }
}