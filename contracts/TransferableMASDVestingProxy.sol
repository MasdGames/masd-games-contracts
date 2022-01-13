import "./MASD.sol";
import "./MASDVesting.sol";


contract TransferableMASDVestingProxy is Ownable {
    MASDVesting vesting;
    IERC20 MASDCoin;

    constructor(address _vesting, address _MASDCoin) {
        require(_vesting != address(0), "ZERO_ADDRESS");
        require(_MASDCoin != address(0), "ZERO_ADDRESS");
        vesting = _vesting;
        MASDCoin = _MASDCoin;
    }

    function withdraw(uint256 userVestingId) external onlyOwner {
        vesting.withdraw(userVestingId);
        MASDCoin.transfer(owner(), MASDCoin.balanceOf(address(this)));
    }

    function withdrawAll() external onlyOwner {
        vesting.withdrawAll();
        MASDCoin.transfer(owner(), MASDCoin.balanceOf(address(this)));
    }
}