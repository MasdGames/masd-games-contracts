pragma solidity 0.8.6;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from '@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol';


// @notice does not work with deflationary tokens (not a big deal since MASDCoin is not)
contract TimeLock {
    using SafeMath for uint256;
    using SafeERC20 for IERC20;

    struct Lock {
        address receiver;
        uint256 amountTotal;
        uint256 amountWithdrawn;
        uint256 startUnlockTimestamp;
        uint256 endUnlockTimestamp;
    }

    IERC20 public MASDCoin;
    uint256 public totalLocks;
    mapping (address => uint256[]) public receiverLockIds;
    mapping (uint256 /*lockId*/ => Lock) public locks;

    function receiverTotalLocks(address receiver) external view returns(uint256 length) {
        length = receiverLockIds[receiver].length;
    }

    event LockCreated (
        uint256 indexed lockId,
        address indexed creator,
        address indexed receiver,
        uint256 amountTotal,
        uint256 startUnlockTimestamp,
        uint256 endUnlockTimestamp
    );
    event Withdrawn(uint256 indexed lockId, uint256 amount);

    constructor(address MASDCoinAddress) {
        require(MASDCoinAddress != address(0), "ZERO_ADDRESS");
        MASDCoin = IERC20(MASDCoinAddress);
    }

    function createLock(
        address receiver,
        uint256 amountTotal,
        uint256 startUnlockTimestamp,
        uint256 endUnlockTimestamp
    ) external {
        require(receiver != address(0), "ZERO_ADDRESS");
        require(amountTotal > 0, "ZERO_AMOUNT");
        require(startUnlockTimestamp > 0, "ZERO_TIMESTAMP");
        require(endUnlockTimestamp > startUnlockTimestamp, "WRONG_TIMESTAMPS_ORDER");
        require(startUnlockTimestamp >= block.timestamp - 365*24*3600, "START_TIMESTAMP_TOO_EARLY");
        require(endUnlockTimestamp <= block.timestamp + 3*365*24*3600, "END_TIMESTAMP_TOO_LONG");
        uint256 lockId = totalLocks++;
        MASDCoin.safeTransferFrom(msg.sender, address(this), amountTotal);
        locks[lockId] = Lock({
            receiver: receiver,
            amountTotal: amountTotal,
            amountWithdrawn: 0,
            startUnlockTimestamp: startUnlockTimestamp,
            endUnlockTimestamp: endUnlockTimestamp
        });
        emit LockCreated({
            lockId: lockId,
            creator: msg.sender,
            receiver: receiver,
            amountTotal: amountTotal,
            startUnlockTimestamp: startUnlockTimestamp,
            endUnlockTimestamp: endUnlockTimestamp
        });
    }

    function withdraw(uint256 lockId) external {
        Lock memory lock = locks[lockId];
        require(lock.receiver == msg.sender, "NOT_RECEIVER");
        require(lock.startUnlockTimestamp < block.timestamp, "UNLOCK_NOT_STARTED");
        require(lock.amountWithdrawn < lock.amountTotal, "ALREADY_WITHDRAWN");
        if (block.timestamp >= lock.endUnlockTimestamp) {
            uint256 amount = lock.amountTotal - lock.amountWithdrawn;
            MASDCoin.safeTransfer(msg.sender, amount);
            locks[lockId].amountWithdrawn += amount;
            emit Withdrawn({
                lockId: lockId,
                amount: amount
            });
            return;
        }
        uint256 period = block.timestamp - lock.startUnlockTimestamp;
        uint256 amountFraction = lock.amountTotal * period / (lock.endUnlockTimestamp - lock.startUnlockTimestamp);
        uint256 amount = amountFraction - lock.amountWithdrawn;
        MASDCoin.safeTransfer(msg.sender, amount);
        locks[lockId].amountWithdrawn += amount;
        emit Withdrawn({
            lockId: lockId,
            amount: amount
        });
    }
}