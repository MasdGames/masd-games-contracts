// SPDX-License-Identifier: NONE
pragma solidity 0.8.6;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import '@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol';

import "./libraries/PercentageVestingLibrary.sol";


// @notice does not work with deflationary tokens (MASDCoin is not deflationary)
contract MASDVesting is Ownable {
    using SafeMath for uint256;
    using SafeERC20 for IERC20;
    using PercentageVestingLibrary for PercentageVestingLibrary.Data;

    struct UserVesting {
        address receiver;
        uint256 totalAmount;
        uint256 withdrawnAmount;
        uint256 vestingParamsId;
    }

    IERC20 public MASDCoin;
    uint256 public totalUserVestingsCount;
    uint256 public totalVestingParamsCount;
    mapping (address => uint256[]) public userVestingIds;
    mapping (uint256 /*lockId*/ => UserVesting) public userVestings;
    mapping (uint256 /*vestingId*/ => PercentageVestingLibrary.Data) public vestingParams;

    event VestingParamsCreated(
        uint256 indexed vestingParamsId
    );
    event UserVestingCreated (
        uint256 indexed userVestingId
    );
    event Withdrawn(
        uint256 indexed userVestingId,
        address indexed user,
        uint256 amount
    );
    event TotalWithdrawn(
        address indexed user,
        uint256 amount
    );

    function userVestingsLength(address user) external view returns(uint256 length) {
        length = userVestingIds[user].length;
    }

    constructor(address MASDCoinAddress) Ownable() {
        require(MASDCoinAddress != address(0), "ZERO_ADDRESS");
        MASDCoin = IERC20(MASDCoinAddress);
    }

    function getVestingParams(uint256 vestingParamsId) external view returns(
        uint16 tgePercentage,
        uint32 tge,
        uint32 cliffDuration,
        uint32 vestingDuration,
        uint32 vestingInterval
    ) {
        return vestingParams[vestingParamsId].vestingDetails();
    }

    function getUserVesting(uint256 userVestingId) public view returns(
        address receiver,
        uint256 totalAmount,
        uint256 withdrawnAmount,
        uint256 vestingParamsId,
        uint256 avaliable
    ) {
        UserVesting storage o = userVestings[userVestingId];
        require(o.receiver != address(0), "NOT_EXISTS");

        receiver = o.receiver;
        totalAmount = o.totalAmount;
        withdrawnAmount = o.withdrawnAmount;
        vestingParamsId = o.vestingParamsId;
        avaliable = vestingParams[o.vestingParamsId].availableOutputAmount({
            totalAmount: o.totalAmount,
            withdrawnAmount: o.withdrawnAmount
        });
    }

    function getWalletInfo(address wallet) external view returns(
        uint256 totalAmount,
        uint256 alreadyWithdrawn,
        uint256 availableToWithdraw
    ) {
        uint256 totalVestingsCount = userVestingIds[wallet].length;
        for (uint256 i; i < totalVestingsCount; i++) {
            uint256 userVestingId = userVestingIds[wallet][i];
            (
                address _receiver,
                uint256 _totalAmount,
                uint256 _withdrawnAmount,
                uint256 _vestingParamsId,
                uint256 _avaliable
            ) = getUserVesting(userVestingId);
            totalAmount += _totalAmount;
            alreadyWithdrawn += _withdrawnAmount;
            availableToWithdraw += _avaliable;
        }
    }

    function createVestingParams(
        uint16 tgePercentage,
        uint32 tge,
        uint32 cliffDuration,
        uint32 vestingDuration,
        uint32 vestingInterval
    ) external onlyOwner {
        uint256 vestingParamsId = totalVestingParamsCount++;
        vestingParams[vestingParamsId].initialize({
            tgePercentage: tgePercentage,
            tge: tge,
            cliffDuration: cliffDuration,
            vestingDuration: vestingDuration,
            vestingInterval: vestingInterval
        });
        emit VestingParamsCreated({
            vestingParamsId: vestingParamsId
        });
    }

    function createUserVesting(
        address receiver,
        uint256 totalAmount,
        uint256 vestingParamsId
    ) external onlyOwner {
        require(receiver != address(0), "ZERO_ADDRESS");
        require(totalAmount > 0, "ZERO_AMOUNT");
        require(vestingParams[vestingParamsId].tge > 0, "VESTING_PARAMS_NOT_EXISTS");
        uint256 userVestingId = totalUserVestingsCount++;
        MASDCoin.safeTransferFrom(msg.sender, address(this), totalAmount);
        userVestings[userVestingId] = UserVesting({
            receiver: receiver,
            totalAmount: totalAmount,
            withdrawnAmount: 0,
            vestingParamsId: vestingParamsId
        });
        userVestingIds[receiver].push(userVestingId);
        emit UserVestingCreated({
            userVestingId: userVestingId
        });
    }

    function withdraw(uint256 userVestingId) public {
        UserVesting memory userVesting = userVestings[userVestingId];
        require(userVesting.receiver == msg.sender, "NOT_RECEIVER");
        uint256 amountToWithdraw = vestingParams[userVesting.vestingParamsId].availableOutputAmount({
            totalAmount: userVesting.totalAmount,
            withdrawnAmount: userVesting.withdrawnAmount
        });

        userVestings[userVestingId].withdrawnAmount += amountToWithdraw;
        MASDCoin.safeTransfer(msg.sender, amountToWithdraw);
        emit Withdrawn({
            userVestingId: userVestingId,
            user: msg.sender,
            amount: amountToWithdraw
        });
    }

    function withdrawAll() external {
        uint256 totalVestingsCount = userVestingIds[msg.sender].length;
        uint256 totalAmountToWithdraw;
        for (uint256 i; i < totalVestingsCount; i++) {
            uint256 userVestingId = userVestingIds[msg.sender][i];
            UserVesting storage userVesting = userVestings[userVestingId];
            uint256 amountToWithdraw = vestingParams[userVesting.vestingParamsId].availableOutputAmount({
                totalAmount: userVesting.totalAmount,
                withdrawnAmount: userVesting.withdrawnAmount
            });
            if (amountToWithdraw > 0) {
                userVestings[userVestingId].withdrawnAmount += amountToWithdraw;
                totalAmountToWithdraw += amountToWithdraw;
                emit Withdrawn({
                    userVestingId: userVestingId,
                    user: msg.sender,
                    amount: amountToWithdraw
                });
            }
        }
        if (totalAmountToWithdraw > 0) {
            MASDCoin.safeTransfer(msg.sender, totalAmountToWithdraw);
        }
        emit TotalWithdrawn({user: msg.sender, amount: totalAmountToWithdraw});
    }
}
