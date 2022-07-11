// SPDX-License-Identifier: NONE
pragma solidity 0.8.6;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import '@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol';
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import "@openzeppelin/contracts/utils/structs/EnumerableSet.sol";
import "@openzeppelin/contracts/utils/cryptography/draft-EIP712.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";


contract Payouts is Ownable, EIP712 {
    // owner must be multi-sig wallet (e.g. Gnosis)

    using SafeERC20 for IERC20;
    using EnumerableSet for EnumerableSet.AddressSet;

    IERC20 public immutable payoutToken;

    // ==== START servers ====
    EnumerableSet.AddressSet internal _servers;
    event ServerAdded(address indexed server);
    event ServerRemoved(address indexed server);
    // ==== END servers ====

    enum PayoutStatus { NONE, WAITING, CANCELLED, PROCESSED }
    struct Payout {
        address winner;
        uint256 amount;
        uint256 registeredAt;
        PayoutStatus payoutStatus;
    }
    mapping(uint256 /*payoutId*/ => Payout) public payouts;
    mapping(address /*wallet*/ => uint256[] /*payoutIds*/) public userWaitingPayoutsIds;

    event PayoutCancelled(uint256 payoutId);
    event PayoutRegistered(
        uint256 payoutId,
        address winner,
        uint256 amount,
        uint256 registeredAt
    );
    event PayoutProcessed(
        uint256 payoutId,
        address winner,
        uint256 amount
    );

    // ==== START delay section ====
    uint256 public delay;
// todo   uint256 public constant MIN_DELAY = 5 days;
    uint256 public constant MIN_DELAY = 0;
    uint256 public constant MAX_DELAY = 14 days;
    event DelaySet(uint256 value);
    // ==== END delay section ====

    bytes32 private immutable _PAYOUT_TYPEHASH =
        keccak256("Payout(address winner,uint256 amount)");

    constructor (uint256 delayValue, address payoutTokenAddress) EIP712("MASDPayouts", "1") {
        setDelay(delayValue);
        require(payoutTokenAddress != address(0), "Payouts: zero address");
        payoutToken = IERC20(payoutTokenAddress);
    }

    // ==== START delay section ====
    function setDelay(uint256 newDelay) public onlyOwner {
        require(newDelay >= MIN_DELAY, "Payouts: fail newDelay >= MIN_DELAY");
        require(newDelay <= MAX_DELAY, "Payouts: fail newDelay <= MAX_DELAY");
        delay = newDelay;
        emit DelaySet(newDelay);
    }

    function _checkDelay(uint256 timestamp) internal view returns(bool) {
        if (block.timestamp < timestamp) {
            return false;  // unexpected
        } else {
            return block.timestamp - timestamp >= delay;
        }
    }
    // ==== END delay section ====

    function claimUserPayouts() external {  // todo: some gas optimisations
        for (uint256 indexOfId; indexOfId < userWaitingPayoutsIds[msg.sender].length;) {
            uint256 payoutId = userWaitingPayoutsIds[msg.sender][indexOfId];
            Payout storage payout = payouts[payoutId];
            if (payout.payoutStatus == PayoutStatus.CANCELLED) {
                if (indexOfId < userWaitingPayoutsIds[msg.sender].length) {
                    userWaitingPayoutsIds[msg.sender][indexOfId] =
                        userWaitingPayoutsIds[msg.sender][userWaitingPayoutsIds[msg.sender].length - 1];
                    // keep the same indexOfId for the next iteration
                }  // else: the next iteration will not happen because of the pop
                userWaitingPayoutsIds[msg.sender].pop();
                continue;
            }

            require(payout.payoutStatus == PayoutStatus.WAITING, "Payouts: storage inconsistency");

            if (_checkDelay(payout.registeredAt)) {
                _unsafeProcessPayout(payoutId, payout);
                if (indexOfId < userWaitingPayoutsIds[msg.sender].length) {
                    userWaitingPayoutsIds[msg.sender][indexOfId] =
                        userWaitingPayoutsIds[msg.sender][userWaitingPayoutsIds[msg.sender].length - 1];
                    // keep the same indexOfId for the next iteration
                }  // else: the next iteration will not happen because of the pop
                userWaitingPayoutsIds[msg.sender].pop();
            } else {
                indexOfId += 1;
            }
        }
    }

    function _unsafeProcessPayout(uint256 payoutId, Payout storage payout) internal {
        payoutToken.safeTransfer(payout.winner, payout.amount);
        emit PayoutProcessed({
            payoutId: payoutId,
            winner: payout.winner,
            amount: payout.amount
        });
        payout.payoutStatus = PayoutStatus.PROCESSED;
        emit PayoutProcessed({
            payoutId: payoutId,
            winner: payout.winner,
            amount: payout.amount
        });
        // todo: save gas
    }

    // ==== START servers ====
    function addServer(address server) external onlyOwner {
        require(_servers.add(server), "already set");
    }

    function removeServer(address server) external onlyOwner {
        require(_servers.remove(server), "not in");
    }

    function getServerByIndex(uint256 index) view external returns(address) {
        return _servers.at(index);
    }

    function getServersLength() view external returns(uint256) {
        return _servers.length();
    }

    function getServers() view external returns(address[] memory) {
        uint256 length = _servers.length();
        address[] memory servers = new address[](length);
        for (uint256 index; index < length; index++){
            address server = _servers.at(index);
            servers[index] = server;
        }
        return servers;
    }

    modifier onlyServer() {
        require(_servers.contains(msg.sender), "Payouts: not server");
        _;
    }
    // ==== END servers ====

//    function registerPayout(uint256 payoutId, address winner, uint256 amount) onlyServer external {
//        uint256 index = payouts.length;
//        payouts.push(Payout({
//            amount: amount,
//            registeredAt: block.timestamp
//        }));
//        userPayoutsIndexes[winner].push(index);
//        emit PayoutRegistered({
//            payoutIndex: index,
//            winner: winner,
//            amount: amount,
//            registeredAt: block.timestamp
//        });
//    }

    function payoutDigest(uint256 payoutId, address winner, uint256 amount) view public returns(bytes32 digest) {
        bytes32 structHash = keccak256(abi.encode(
            _PAYOUT_TYPEHASH,
            payoutId,
            winner,
            amount
        ));
        digest = _hashTypedDataV4(structHash);
    }

    function registerPayoutMeta(
        uint256 payoutId,
        address winner,
        uint256 amount,
        address signer,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external {
        require(payouts[payoutId].payoutStatus == PayoutStatus.NONE, "Payouts: already exists");
// todo       require(msg.sender == winner || msg.sender == owner(), "Payouts: caller is not winner or owner");
        require(_servers.contains(signer) || signer == owner(), "Payouts: signer is not server or owner");  // todo: if server was removed future signatures are invalid
        bytes32 digest = payoutDigest(payoutId, winner, amount);
        address signerRecovered = ECDSA.recover(digest, v, r, s);
        require(signer == signerRecovered, "Payouts: invalid signerRecovered");

        payouts[payoutId] = Payout({
            winner: winner,
            amount: amount,
            registeredAt: block.timestamp,
            payoutStatus: PayoutStatus.WAITING
        });
        userWaitingPayoutsIds[winner].push(payoutId);
        emit PayoutRegistered({
            payoutId: payoutId,
            winner: winner,
            amount: amount,
            registeredAt: block.timestamp
        });
    }

    function cancelPayout(uint256 payoutId) external onlyOwner {
        // todo: onlyModerator
        // todo: decrease payout not only cancel
        payouts[payoutId].payoutStatus = PayoutStatus.CANCELLED;
        emit PayoutCancelled(payoutId);
    }
}