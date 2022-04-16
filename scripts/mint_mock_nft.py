from brownie import accounts, MockMASDNFT, web3
from brownie import *


def main():
    admin = accounts.load('brave_main')
    nft = Contract.from_abi("MockMASDNFT", "0x1f458049FC6b3dabC02F49dAd32Fa98017D5d637", MockMASDNFT.abi)
    tx = nft.mintWithTokenURI('QmVgiTFc7JbbTz65RnCQrnHNMypzqZPd8tav4heykkFaWu', {"from": admin})
    token_id = tx.events['Transfer']['tokenId']
    print(f'mint {token_id=}')
