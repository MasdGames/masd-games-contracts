import time
from brownie import accounts, MockMASDNFT, MockMASDERC1155


def main():
    admin = accounts.load('brave_main')
    gas_price = None

    nft = MockMASDNFT.deploy(admin, {'from': admin, 'gas_price': gas_price})
    time.sleep(3)

    try:
        MockMASDNFT.publish_source(nft)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise

    tx = nft.mintWithTokenURI("https://masd.games/erc721/1", {'from': admin, 'gas_price': gas_price})
    print(f'mint nft {tx.events["Transfer"]["tokenId"]}')


    erc1155 = MockMASDERC1155.deploy("https://masd.games/erc1155/\{id\}", admin, {'from': admin, 'gas_price': gas_price})
    time.sleep(3)

    try:
        MockMASDERC1155.publish_source(erc1155)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise

    tx = erc1155.mint(
        admin,  # to
        1,  # id
        20,  # amount
        "",  # data
        {'from': admin, 'gas_price': gas_price})
    print(f'mint nft {tx.events["Transfer"]["tokenId"]}')
