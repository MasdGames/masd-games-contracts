from brownie import accounts, MockMASDVesting, web3


def main():
    admin = accounts.load('brave_main')
    gas_price = '5 gwei'
    # deployed at ...
    mock_vesting = MockMASDVesting.deploy({'from': admin, 'gas_price': gas_price})

    try:
        MockMASDVesting.publish_source(mock_vesting)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise
