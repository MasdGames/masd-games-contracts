import time

from brownie import *
from brownie import reverts

from eth_account._utils.signing import sign_message_hash
from eth_utils import decode_hex
from hexbytes import HexBytes


def test_permit(masd_signatures, masd, admin, user1):
    user0 = accounts.add(private_key='b25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364')
    masd.transfer(user0, 1 * 10**18, {'from': admin})

    owner = user0.address
    spender = user1.address
    value = int(0.01 * 10**18)
    nonce = masd.nonces(user0.address)
    deadline = int(time.time()) + 365*24*3600
    offer_digest = masd_signatures.permitDigest(
        owner,
        spender,
        value,
        nonce,
        deadline
    )
    print(f'{type(offer_digest)=} {offer_digest=}')

    import eth_keys
    eth_private_key = eth_keys.keys.PrivateKey(HexBytes(user0.private_key))
    (v, r, s, eth_signature_bytes) = sign_message_hash(eth_private_key, offer_digest)

    balance_before = masd.balanceOf(user1)
    masd.permit(
        owner,
        spender,
        value,
        deadline,
        v, r, s,
        {"from": user1}
    )
    masd.transferFrom(user0, user1, value, {"from": user1})

    balance_after = masd.balanceOf(user1)
    balance_delta = balance_after - balance_before
    assert balance_delta == value
