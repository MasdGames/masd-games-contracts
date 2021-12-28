from brownie import accounts, MASD, web3, Contract


def main():
    masd_coin = Contract.from_abi("MASD", "0xfcc92ae68facbDb6372fce8fBCaCC08b67f8A744", MASD.abi)
    try:
        MASD.publish_source(masd_coin)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise
