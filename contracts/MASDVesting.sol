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
        uint256 vestingParamId;
    }

    IERC20 public MASDCoin;
    uint256 public totalUserVestingsCount;
    uint256 public totalVestingParamsCount;
    mapping (address => uint256[]) public userVestingIds;
    mapping (uint256 /*lockId*/ => UserVesting) public userVestings;
    mapping (uint256 /*vestingId*/ => PercentageVestingLibrary.Data) public vestingParams;

    event VestingParamsCreated(
        uint256 indexed vestingParamId
    );
    event UserVestingCreated (
        uint256 indexed userVestingId
    );
    event Withdrawn(
        uint256 indexed userVestingId,
        address indexed user,
        uint256 amount
    );

    function userTotalLocks(address user) external view returns(uint256 length) {
        length = userVestingIds[user].length;
    }

    constructor(address MASDCoinAddress) Ownable() {
        require(MASDCoinAddress != address(0), "ZERO_ADDRESS");
        MASDCoin = IERC20(MASDCoinAddress);
    }

    function createVestingParams(
        uint16 tgePercentage,
        uint32 tge,
        uint32 cliffDuration,
        uint32 vestingDuration,
        uint32 vestingInterval
    ) external {
        uint256 vestingParamId = totalVestingParamsCount++;
        vestingParams[vestingParamId].initialize({
            tgePercentage: tgePercentage,
            tge: tge,
            cliffDuration: cliffDuration,
            vestingDuration: vestingDuration,
            vestingInterval: vestingInterval
        });
        emit VestingParamsCreated({
            vestingParamId: vestingParamId
        });
    }

    function createUserVesting(
        address receiver,
        uint256 amountTotal,
        uint256 vestingParamId
    ) external {
        require(receiver != address(0), "ZERO_ADDRESS");
        require(amountTotal > 0, "ZERO_AMOUNT");
        require(vestingParams[vestingParamId].tge > 0, "VESTING_PARAMS_NOT_EXISTS");
        uint256 userVestingId = totalUserVestingsCount++;
        MASDCoin.safeTransferFrom(msg.sender, address(this), amountTotal);
        userVestings[userVestingId] = UserVesting({
            receiver: receiver,
            amountTotal: amountTotal,
            amountWithdrawn: 0,
            vestingParamId: vestingParamId
        });
        emit UserVestingCreated({
            userVestingId: userVestingId
        });
    }

    function withdraw(uint256 userVestingId) external {
        UserVesting memory userVesting = userVestings[userVestingId];
        require(userVesting.receiver == msg.sender, "NOT_RECEIVER");
        uint256 amountToWithdraw = vestingParams[userVesting.vestingParamId].availableOutputAmount(
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
}
