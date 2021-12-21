from brownie import accounts, MASDCoin, web3


def main():
    masd_admin = accounts.load('masd')
    gas_price = '5 gwei'
    masd_coin = MASDCoin.deploy({'from': masd_admin, 'gas_price': gas_price})

    try:
        MASDCoin.publish_source(masd_coin)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise
