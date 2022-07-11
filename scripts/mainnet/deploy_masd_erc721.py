import time
from brownie import *


def main():
    admin = accounts.load('brave_main')
    gas_price = '5 gwei'

    # todo
    erc721 = MASD_ERC721.deploy(admin, {'from': admin, 'gas_price': gas_price})
    time.sleep(3)

    try:
        MASD_ERC721.publish_source(erc721)
    except ValueError as exc:
        if 'Contract source code already verified' not in str(exc):
            raise

    # image https://storage.googleapis.com/masd/masd-battle-pass.jpeg

    """
{
    "name": "MASD battle pass (30 games)",
    "description": "Owner of this NFT can participate 30 times in battle games on https://masd.games/",
    "external_url": "https://docs.masd.games/",
    "image": "https://storage.googleapis.com/masd/masd-battle-pass.jpeg",
    "attributes": [{
        "trait_type": "games_count",
        "value": 30
    }]
}
    """
    # https://storage.googleapis.com/masd/masd-battle-pass.json

    batch_size = 10
    for start_token_id in range(1, 500+1, batch_size):
        end_token_id = start_token_id + batch_size
        token_ids = [_ for _ in range(start_token_id, end_token_id)]
        tx = erc721.mintWithURIBatch(
            [admin] * batch_size,  # to
            token_ids,  # id
            ["https://storage.googleapis.com/masd/masd-battle-pass.json"] * batch_size,  # uri
            {'from': admin, 'gas_price': gas_price})
        print(f'ok {token_ids=}')
