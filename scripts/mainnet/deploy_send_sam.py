import time
from brownie import *


def main():
    admin = accounts.load('masd')
    assert admin == '0x20733EEbD28a47c762aeCE4c6Bcc8E771d08710E'
    gas_price = None

    erc1155 = Contract.from_abi("ERC1155", "0x52Fb465Cc0c4F65a2eb39e366d68d7B212a1CF8c", MASD_ERC1155.abi)

    for receiver in [
        '0xa3dd3f184c69454715acb5467daff82a83a54b29',
        '0x87c0789958323d1b9c9badc8a536404801b58462',
        '0xb262a0316b265be137e8a4aadc1e75e573c10d7d',
        '0x58b2cd6aa9e0c066266e16e8444dac8ed60d6be0',
        '0x4af293d4056eff290b5cc235dbbe406d6b12f440',
    ]:
        tx = erc1155.safeTransferFrom(
            admin,
            receiver,  # to
            1,  # id
            1,  # amount
            "",  # data
            {'from': admin, 'gas_price': gas_price}
        )

