from brownie import accounts, MASDVesting, web3, MASD


def main():
    admin = accounts.load('brave_main')
    gas_price = '6 gwei'

    # 0x49B05cBaa9B8d25Ec792190Ef65868e9013fa19C
    masd_coin = MASD.deploy(0, admin, {'from': admin, 'gas_price': gas_price})

    # 0xb88C49D98687F4216B4948fB8aF2dFCd2ecCB361
    vesting = MASDVesting.deploy(masd_coin, {'from': admin, 'gas_price': gas_price})

    try:
        MASD.publish_source(masd_coin)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise

    try:
        MASDVesting.publish_source(vesting)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise
