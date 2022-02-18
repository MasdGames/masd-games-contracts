import eth_keys
from eth_account._utils.signing import sign_message_hash
from hexbytes import HexBytes
from brownie import accounts


def test_payout(admin, payouts, busd, user0, chain):
    busd.transfer(payouts, 10**6 * 10**18, {'from': admin})

    winner = user0
    server = accounts.add(private_key='b25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364')
    amount = 10 * 10**18
    payout_id = 42

    payouts.addServer(server, {"from": admin})

    digest = payouts.payoutDigest(
        payout_id,
        winner,
        amount
    )
    eth_private_key = eth_keys.keys.PrivateKey(HexBytes(server.private_key))
    (v, r, s, eth_signature_bytes) = sign_message_hash(eth_private_key, digest)

    tx = payouts.registerPayoutMeta(
        payout_id,
        winner,
        amount,
        server,
        v,
        r,
        s,
        {"from": admin}
    )
    assert 'PayoutRegistered' in tx.events

    balance_before = busd.balanceOf(winner)
    payouts.claimUserPayouts({"from": winner})
    balance_after = busd.balanceOf(winner)
    assert balance_after - balance_before == 0

    chain.sleep(payouts.delay())
    chain.mine()

    balance_before = busd.balanceOf(winner)
    payouts.claimUserPayouts({"from": winner})
    balance_after = busd.balanceOf(winner)
    assert balance_after - balance_before == amount
