import time
from brownie import *


def main():
    admin = accounts.load('masd')
    assert admin == '0x20733EEbD28a47c762aeCE4c6Bcc8E771d08710E'
    gas_price = None

    erc1155 = Contract.from_abi("ERC1155", "0x52Fb465Cc0c4F65a2eb39e366d68d7B212a1CF8c", MASD_ERC1155.abi)
    tx = erc1155.mintWithURI(
        '0x7f8a8fe791484384b0674631096b8dc8553692df',  # to
        2,  # id
        1,  # amount
        "",  # data
        "https://storage.googleapis.com/masd/cheetah.json",  # uri
        {'from': admin, 'gas_price': gas_price})
    tokenId = tx.events["TransferSingle"]["id"]
    uri = erc1155.uri(tokenId)
    print(f'mint nft {tokenId}, {uri=}')
