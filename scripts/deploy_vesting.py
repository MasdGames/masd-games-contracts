from brownie import accounts, MASDVesting, web3, MASD

MASD_MULTISIG = '0x928d0F89968523ac0e3b40dfC22a5B83a3932F11'
MASD_ADDRESS = '0xfcc92ae68facbDb6372fce8fBCaCC08b67f8A744'


def main():
    masd_admin = accounts.load('masd')
    gas_price = '6 gwei'

    # bsc: 0x95a3C00D5d35aC0F125F9782838a086750103C21
    vesting = MASDVesting.deploy(MASD_ADDRESS, {'from': masd_admin, 'gas_price': gas_price})
    vesting.transferOwnership(MASD_MULTISIG, {'from': masd_admin, 'gas_price': gas_price})

    try:
        MASDVesting.publish_source(vesting)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise
