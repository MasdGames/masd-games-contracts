import time
from brownie import *


def main():
    admin = accounts.load('masd')
    assert admin == '0x20733EEbD28a47c762aeCE4c6Bcc8E771d08710E'
    gas_price = None

    # erc1155 = MASD_ERC1155.deploy("https://masd.games/erc1155/{id}", admin, {'from': admin, 'gas_price': gas_price})
    # time.sleep(3)
    # try:
    #     MASD_ERC1155.publish_source(erc1155)
    # except ValueError as exc:
    #     if 'Contract source code already verified' not in str(exc):
    #         raise

    erc1155 = Contract.from_abi("ERC1155", "0x52Fb465Cc0c4F65a2eb39e366d68d7B212a1CF8c", MASD_ERC1155.abi)

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

    erc1155.safeTransferFrom(
        admin,
        '0x20733EEbD28a47c762aeCE4c6Bcc8E771d08710E',
        tokenId,
        1000,
        "",
        {'from': admin, 'gas_price': gas_price},
    )
