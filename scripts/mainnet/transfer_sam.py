import time
from brownie import *


def main():
    admin = accounts.load('masd')
    assert admin == '0x20733EEbD28a47c762aeCE4c6Bcc8E771d08710E'
    gas_price = None

    erc1155 = Contract.from_abi('MASD_ERC1155', '0x52Fb465Cc0c4F65a2eb39e366d68d7B212a1CF8c', MASD_ERC1155.abi)
    tokenId = 1
    erc1155.safeTransferFrom(
        admin,
        '0x5fd077a7c6592F01A026f14abb6f9Db36aa4CD4c',
        tokenId,
        1,  # amount
        "",
        {'from': admin, 'gas_price': gas_price},
    )
