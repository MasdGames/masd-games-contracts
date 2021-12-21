from brownie import accounts, MASDCoin, web3, Contract


def main():
    masd_coin = Contract.from_abi("MASDCoin", "0x5d9C9bd03475eCf89a4e00f6d77Cc3121ff1b362", MASDCoin.abi)
    try:
        MASDCoin.publish_source(masd_coin)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise
