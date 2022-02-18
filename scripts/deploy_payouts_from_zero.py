from brownie import accounts, MockBUSD, Payouts, web3


def main():
    admin = accounts.load('brave_main')
    # bsc-test 0x37bFa1452BE9676992027Ac4172a7d1141335B5b
    busd = MockBUSD.deploy(100 * 1_000_000 * 10**18, admin, {'from': admin})

    try:
        MockBUSD.publish_source(busd)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise

    delayValue = 10 * 60
    payouts = Payouts.deploy(delayValue, busd, {"from": admin})

    # bsc-test 0xfd6DbA20FF27f0a0F6086CaD15f8488D0BC2779f
    try:
        Payouts.publish_source(payouts)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise
