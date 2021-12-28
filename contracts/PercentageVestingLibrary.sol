// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/utils/math/Math.sol";

library BP {
    uint16 constant DECIMAL_FACTOR = 10000;
}

library PercentageVestingLibrary {

    struct Data {
        // uint32 in seconds = 136 years
        uint16 tgePercentage;
        uint32 tge;
        uint32 cliffDuration;
        uint32 vestingDuration;
        uint32 vestingInterval;
    }

    function initialize(
        Data storage self,
        uint16 tgePercentage,
        uint32 tge,
        uint32 cliffDuration,
        uint32 vestingDuration,
        uint32 vestingInterval
    ) internal {
        // cliff may have zero duration to instantaneously unlock percentage of funds
        require(tgePercentage <= BP.DECIMAL_FACTOR, "PercentageVestingLibrary: CLIFF");
        if (vestingDuration == 0 || vestingInterval == 0) {
            // vesting disabled
            require(vestingDuration == 0 && vestingInterval == 0, "PercentageVestingLibrary: VESTING");
            // when vesting is disabled, cliff must unlock 100% of funds
            require(tgePercentage == BP.DECIMAL_FACTOR, "PercentageVestingLibrary: CLIFF");
        } else {
            require(vestingInterval > 0 && vestingInterval <= vestingDuration, "PercentageVestingLibrary: VESTING");
        }
        self.tgePercentage = tgePercentage;
        self.tge = tge;
        self.cliffDuration = cliffDuration;
        self.vestingDuration = vestingDuration;
        self.vestingInterval = vestingInterval;
    }

    function availableOutputAmount(Data storage self, uint max, uint output) internal view returns (uint) {
        // output = max - amount_unlocked - amount_vested
        if (block.timestamp < self.tge) {
            return 0; // no unlock or vesting yet
        }
        uint cliff = (max * self.tgePercentage) / BP.DECIMAL_FACTOR;
        uint maxVested = max - cliff;
        if (output == max) { // first claim
            if (block.timestamp < self.tge + self.cliffDuration) {
                return cliff;
            }
            return _vested(self, 0, maxVested) + cliff;
        } else {
            if (block.timestamp < self.tge + self.cliffDuration) {
                return 0;
            }
            uint vested = max - output - cliff;
            return _vested(self, vested, maxVested);
        }
    }

    function vestingDetails(Data storage self) internal view returns (uint16, uint32, uint32, uint32, uint32) {
        return (self.tgePercentage, self.tge, self.cliffDuration, self.vestingDuration, self.vestingInterval);
    }

    function _vested(
        Data storage self,
        uint vested,
        uint maxVested
    ) private view returns (uint) {
        if (self.vestingDuration == 0) {
            return maxVested;
        }
        uint vestedPerInterval = maxVested * self.vestingInterval / self.vestingDuration;
        if (vestedPerInterval == 0) {
            // when maxVested is too small or vestingDuration is too large, vesting reward is too small to even be distributed
            return 0;
        }
        uint cliffEnd = self.tge + self.cliffDuration;
        uint vestingEnd = (maxVested / vestedPerInterval) * self.vestingInterval + cliffEnd;
        // We guarantee that time is >= cliffEnd
        if (block.timestamp >= vestingEnd) {
            return maxVested - vested;
        } else {
            return Math.min(available, maxVested) - vested;

            uint lastVesting = (vested / vestedPerInterval) * self.vestingInterval + cliffEnd;
            uint available = ((block.timestamp - lastVesting) / self.vestingInterval + 1) * vestedPerInterval;
            return Math.min(available, maxVested) - vested;
        }
    }
}

