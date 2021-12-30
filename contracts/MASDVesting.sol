pragma solidity 0.8.6;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import {SafeERC20} from '@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol';

import "./libraries/PercentageVestingLibrary.sol";


// @notice does not work with deflationary tokens (MASDCoin is not deflationary)
contract MASDVesting is Ownable {
    using SafeMath for uint256;
    using SafeERC20 for IERC20;
    using PercentageVestingLibrary for PercentageVestingLibrary.Data;

    struct UserVesting {
        address receiver;
        uint256 amountTotal;
        uint256 amountWithdrawn;
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

    function userTotalVestings(address user) external view returns(uint256 length) {
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

    function getUserVesting(uint256 userVestingId) external view returns(
        address receiver,
        uint256 amountTotal,
        uint256 amountWithdrawn,
        uint256 vestingParamsId,
        uint256 avaliable
    ) {
        UserVesting storage o = userVestings[userVestingId];
        require(o.receiver != address(0), "NOT_EXISTS");
        receiver = o.receiver;
        amountTotal = o.amountTotal;
        amountWithdrawn = o.amountWithdrawn;
        vestingParamsId = o.vestingParamsId;
        avaliable = vestingParams[o.vestingParamsId].availableOutputAmount(
            o.amountTotal,
            o.amountTotal-o.amountWithdrawn
        );
    }

    function getUserVestingSTUB(uint256 userVestingId) external returns(
        address receiver,
        uint256 amountTotal,
        uint256 amountWithdrawn,
        uint256 vestingParamsId,
        uint256 avaliable
    ) {
        UserVesting storage o = userVestings[userVestingId];
        require(o.receiver != address(0), "NOT_EXISTS");
        receiver = o.receiver;
        amountTotal = o.amountTotal;
        amountWithdrawn = o.amountWithdrawn;
        vestingParamsId = o.vestingParamsId;
        avaliable = vestingParams[o.vestingParamsId].availableOutputAmountSTUB(
            o.amountTotal,
            o.amountTotal-o.amountWithdrawn
        );
    }

    function createVestingParams(
        uint16 tgePercentage,
        uint32 tge,
        uint32 cliffDuration,
        uint32 vestingDuration,
        uint32 vestingInterval
    ) external {
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
        uint256 amountTotal,
        uint256 vestingParamsId
    ) external {
        require(receiver != address(0), "ZERO_ADDRESS");
        require(amountTotal > 0, "ZERO_AMOUNT");
        require(vestingParams[vestingParamsId].tge > 0, "VESTING_PARAMS_NOT_EXISTS");
        uint256 userVestingId = totalUserVestingsCount++;
        MASDCoin.safeTransferFrom(msg.sender, address(this), amountTotal);
        userVestings[userVestingId] = UserVesting({
            receiver: receiver,
            amountTotal: amountTotal,
            amountWithdrawn: 0,
            vestingParamsId: vestingParamsId
        });
        userVestingIds[receiver].push(userVestingId);
        emit UserVestingCreated({
            userVestingId: userVestingId
        });
    }

        event E(string k, uint v);


    function withdraw(uint256 userVestingId) public {
        UserVesting memory userVesting = userVestings[userVestingId];
        require(userVesting.receiver == msg.sender, "NOT_RECEIVER");
        uint256 amountToWithdraw = vestingParams[userVesting.vestingParamsId].availableOutputAmountSTUB(
            userVesting.amountTotal,
            userVesting.amountTotal-userVesting.amountWithdrawn
        );

        MASDCoin.safeTransfer(msg.sender, amountToWithdraw);
        userVestings[userVestingId].amountWithdrawn += amountToWithdraw;
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
            uint256 amountToWithdraw = vestingParams[userVesting.vestingParamsId].availableOutputAmount(
                userVesting.amountTotal,
                userVesting.amountTotal-userVesting.amountWithdrawn
            );
            if (amountToWithdraw > 0) {
                userVestings[userVestingId].amountWithdrawn += amountToWithdraw;
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
    }
}
