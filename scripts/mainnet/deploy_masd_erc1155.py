import time
from brownie import *


def main():
    admin = accounts.load('brave_main')
    gas_price = '10 gwei'

    # 0x52Fb465Cc0c4F65a2eb39e366d68d7B212a1CF8c
    erc1155 = MASD_ERC1155.deploy("https://masd.games/erc1155/{id}", admin, {'from': admin, 'gas_price': gas_price})
    time.sleep(3)

    try:
        MASD_ERC1155.publish_source(erc1155)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise

    tx = erc1155.mintWithURI(
        admin,  # to
        1,  # id
        2000,  # amount
        "",  # data
        "https://storage.googleapis.com/masd/sam.json",  # uri
        {'from': admin, 'gas_price': gas_price})
    tokenId = tx.events["TransferSingle"]["id"]
    uri = erc1155.uri(tokenId)
    print(f'mint nft {tokenId}, {uri=}')
