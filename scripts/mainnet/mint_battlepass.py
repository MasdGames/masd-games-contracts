import time
from brownie import *


def main():
    admin = accounts.load('masd')
    gas_price = '5 gwei'

    erc721 = Contract.from_abi("ERC721", "0xBC7c836D99C77f4a92c27Ee9A31f833D917ccbC3", MASD_ERC721.abi)

    baseURI = 'https://masd.games/battlepassmetadata/'

    batch_size = 50
    total_count = 500
    assert total_count % batch_size == 0
    for start_token_id in range(1, total_count+1, batch_size):
        end_token_id = start_token_id + batch_size
        token_ids = [_ for _ in range(start_token_id, end_token_id)]
        print(f'start {token_ids[0]} ... {token_ids[-1]}')
        tx = erc721.mintBatch(
            [admin] * batch_size,  # to
            token_ids,  # id
            {'from': admin, 'gas_price': gas_price})
        for token_id in token_ids:
            assert erc721.ownerOf(token_id) == admin
            assert erc721.tokenURI(token_id) == baseURI + str(token_id)
        print(f'ok  {token_ids[0]} ... {token_ids[-1]}')
