pragma solidity 0.8.6;
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";


contract MASDCoin is IERC20 {
    using SafeMath for uint256;

    string public constant name = "MASD";
    string public constant symbol = "MASD";
    uint256 public constant decimals = 18;
    uint256 public constant override totalSupply = (100 * 1000 * 1000) * 10**18;

    mapping(address => uint256) internal balances;
    mapping(address => mapping(address => uint256)) internal allowed;

    constructor() {
        balances[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }

    function transfer(address to, uint256 amount) override external returns (bool) {
        require(to != address(0), "ZERO_ADDRESS");
        balances[msg.sender] = balances[msg.sender].sub(amount, "BALANCE_NOT_ENOUGH");
        balances[to] = balances[to].add(amount);
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    function balanceOf(address owner) override external view returns (uint256) {
        return balances[owner];
    }

    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) override external returns (bool) {
        require(to != address(0), "ZERO_ADDRESS");
        balances[from] = balances[from].sub(amount, "BALANCE_NOT_ENOUGH");
        balances[to] = balances[to].add(amount);
        allowed[from][msg.sender] = allowed[from][msg.sender].sub(amount, "ALLOWANCE_NOT_ENOUGH");
        emit Transfer(from, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) override external returns (bool) {
        allowed[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function allowance(address owner, address spender) override external view returns (uint256) {
        return allowed[owner][spender];
    }
}
