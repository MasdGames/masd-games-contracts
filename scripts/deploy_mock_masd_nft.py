from brownie import accounts, MockMASDNFT, web3


def main():
    admin = accounts.load('brave_main')
    gas_price = '5 gwei'
    # deployed at 0xB1AdB7510331173b3c76b37B9a3Dd1d94Ec7d7a1
    contract = MockMASDNFT.deploy(admin, {'from': admin, 'gas_price': gas_price})

    try:
        MockMASDNFT.publish_source(contract)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise
