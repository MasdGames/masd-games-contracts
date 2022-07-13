import time
from brownie import *


def main():
    admin = accounts.load('masd')
    gas_price = '5 gwei'

    baseURI = 'https://masd.games/battlepassmetadata/'
    erc721 = MASD_ERC721.deploy(admin, baseURI, {'from': admin, 'gas_price': gas_price})
    time.sleep(3)

    assert erc721.baseURI() == baseURI
    assert erc721.owner() == admin

    try:
        MASD_ERC721.publish_source(erc721)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise

    # tx - 0x7ed3f0976555f8a484612d128a4a42591365bc8d431e92d41269636509b7661c
    # MASD_ERC721 - 0xBC7c836D99C77f4a92c27Ee9A31f833D917ccbC3
