from brownie import accounts, MASD, web3

MASD_MULTISIG = '0x928d0F89968523ac0e3b40dfC22a5B83a3932F11'


def main():
    masd_admin = accounts.load('masd')
    gas_price = '5 gwei'
    # deployed at 0xfcc92ae68facbDb6372fce8fBCaCC08b67f8A744 BSC-Main
    masd_coin = MASD.deploy(0, MASD_MULTISIG, {'from': masd_admin, 'gas_price': gas_price})

    try:
        MASD.publish_source(masd_coin)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise
