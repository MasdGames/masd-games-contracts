from brownie import *


def test_DECIMAL_FACTOR(admin):
    bp = admin.deploy(BP)
    assert bp.DECIMAL_FACTOR() == 10000


def test_create_vesting_params(admin, masd, vesting, chain):
    tgePercentage = 1000  # 10%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 6 * 30 * 24 * 3600
    vestingInterval = 1
    tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
    )
    vestingParamsId = tx.events['VestingParamsCreated']['vestingParamsId']
    assert vestingParamsId == 0
    assert vesting.getVestingParams(vestingParamsId) == (
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval
    )


def test_create_user_vesting(admin, masd, vesting, chain, user0, user1):
    tgePercentage = 1000  # 10%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 6 * 30 * 24 * 3600
    vestingInterval = 1
    tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
    )
    vestingParamsId = tx.events['VestingParamsCreated']['vestingParamsId']
    receiver = user1
    amountTotal = 10 * 10**18

    masd.mint(user0, amountTotal, {"from": admin})
    masd.approve(vesting, amountTotal, {"from": user0})
    tx = vesting.createUserVesting(
        receiver,
        amountTotal,
        vestingParamsId,
        {"from": user0}
    )
    userVestingId = tx.events['UserVestingCreated']['userVestingId']
    assert userVestingId == 0

    # todo
    # assert vesting.getUserVesting(userVestingId) == (
    #     receiver,
    #     amountTotal,
    #     0,  # amountWithdrawn
    #     vestingParamsId,
    #     0  # avaliable
    # )


# def test_withdraw_user_vesting(admin, masd, vesting, chain, user0, user1):
#     tgePercentage = 1000  # 10%
#     tge = chain.time() + 3600
#     cliffDuration = 30 * 24 * 3600  # 30 days
#     vestingDuration = 6 * 30 * 24 * 3600
#     vestingInterval = 1
#     tx = vesting.createVestingParams(
#         tgePercentage,
#         tge,
#         cliffDuration,
#         vestingDuration,
#         vestingInterval,
#         {"from": admin}
#     )
#     vestingParamsId = tx.events['VestingParamsCreated']['vestingParamsId']
#     receiver = user1
#     amountTotal = 10 * 10**18
#     amountVesting = amountTotal - int(amountTotal * tgePercentage / 10000)
#
#     masd.mint(user0, amountTotal, {"from": admin})
#     masd.approve(vesting, amountTotal, {"from": user0})
#     tx = vesting.createUserVesting(
#         receiver,
#         amountTotal,
#         vestingParamsId,
#         {"from": user0}
#     )
#     userVestingId = tx.events['UserVestingCreated']['userVestingId']
#     assert userVestingId == 0
#     assert vesting.getUserVesting(userVestingId) == (
#         receiver,
#         amountTotal,
#         0,  # amountWithdrawn
#         vestingParamsId,
#         0  # avaliable
#     )
#
#     tx = vesting.withdraw(userVestingId, {"from": receiver})
#     assert tx.events['Withdrawn']['userVestingId'] == userVestingId
#     assert tx.events['Withdrawn']['user'] == receiver
#     assert tx.events['Withdrawn']['amount'] == 0
#
#     chain.sleep(tge - chain.time() - 10)
#
#     tx = vesting.withdraw(userVestingId, {"from": receiver})
#     assert tx.events['Withdrawn']['userVestingId'] == userVestingId
#     assert tx.events['Withdrawn']['user'] == receiver
#     assert tx.events['Withdrawn']['amount'] == 0
#
#     chain.sleep(tge - chain.time())
#
#     tx = vesting.withdraw(userVestingId, {"from": receiver})
#     assert tx.events['Withdrawn']['userVestingId'] == userVestingId
#     assert tx.events['Withdrawn']['user'] == receiver
#     assert tx.events['Withdrawn']['amount'] == int(tgePercentage * amountTotal // 10_000)
#
#     chain.sleep(cliffDuration - 10)
#
#     tx = vesting.withdraw(userVestingId, {"from": receiver})
#     assert tx.events['Withdrawn']['userVestingId'] == userVestingId
#     assert tx.events['Withdrawn']['user'] == receiver
#     assert tx.events['Withdrawn']['amount'] == 0
#
#     chain.sleep(cliffDuration - (chain.time() - tge) - 1)
#
#     tx = vesting.withdraw(userVestingId, {"from": receiver})
#     assert tx.events['Withdrawn']['userVestingId'] == userVestingId
#     assert tx.events['Withdrawn']['user'] == receiver
#     assert tx.events['Withdrawn']['amount'] == 0
#
#     chain.sleep(1)
#     tx = vesting.withdraw(userVestingId, {"from": receiver})
#     assert chain.time() == tge + cliffDuration  # the 0th second of the vesting itself
#     assert tx.events['Withdrawn']['userVestingId'] == userVestingId
#     assert tx.events['Withdrawn']['user'] == receiver
#     assert tx.events['Withdrawn']['amount'] == amountVesting // vestingDuration
#
#     period = vestingInterval * 3
#     assert period == 3
#     chain.sleep(period)
#     tx = vesting.withdraw(userVestingId, {"from": receiver})
#     assert chain.time() == tge + cliffDuration + period  # the 0th second of the vesting itself
#     assert tx.events['Withdrawn']['userVestingId'] == userVestingId
#     assert tx.events['Withdrawn']['user'] == receiver
#     assert tx.events['Withdrawn']['amount'] == amountVesting // vestingDuration * period


def test_withdraw_user_vesting_daily_intervals(admin, masd, vesting, chain, user0, user1):
    tgePercentage = 1000  # 10%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 6 * 30 * 24 * 3600  # ~6 months
    vestingInterval = 24 * 3600  # 1 day
    tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
    )
    vestingParamsId = tx.events['VestingParamsCreated']['vestingParamsId']
    receiver = user1
    amountTotal = 10 * 10**18
    amountVesting = amountTotal - int(amountTotal * tgePercentage / 10000)

    masd.mint(user0, amountTotal, {"from": admin})
    masd.approve(vesting, amountTotal, {"from": user0})
    tx = vesting.createUserVesting(
        receiver,
        amountTotal,
        vestingParamsId,
        {"from": user0}
    )
    userVestingId = tx.events['UserVestingCreated']['userVestingId']
    assert userVestingId == 0

    # todo
    # assert vesting.getUserVesting(userVestingId) == (
    #     receiver,
    #     amountTotal,
    #     0,  # amountWithdrawn
    #     vestingParamsId,
    #     0  # avaliable
    # )

    tx = vesting.withdraw(userVestingId, {"from": receiver})
    assert tx.events['Withdrawn']['userVestingId'] == userVestingId
    assert tx.events['Withdrawn']['user'] == receiver
    assert tx.events['Withdrawn']['amount'] == 0

    chain.sleep(tge - chain.time() - 10)

    tx = vesting.withdraw(userVestingId, {"from": receiver})
    assert tx.events['Withdrawn']['userVestingId'] == userVestingId
    assert tx.events['Withdrawn']['user'] == receiver
    assert tx.events['Withdrawn']['amount'] == 0

    chain.sleep(tge - chain.time())

    tx = vesting.withdraw(userVestingId, {"from": receiver})
    assert tx.events['Withdrawn']['userVestingId'] == userVestingId
    assert tx.events['Withdrawn']['user'] == receiver
    assert tx.events['Withdrawn']['amount'] == int(tgePercentage * amountTotal // 10_000)

    chain.sleep(cliffDuration - 10)

    tx = vesting.withdraw(userVestingId, {"from": receiver})
    assert tx.events['Withdrawn']['userVestingId'] == userVestingId
    assert tx.events['Withdrawn']['user'] == receiver
    assert tx.events['Withdrawn']['amount'] == 0

    chain.sleep(cliffDuration - (chain.time() - tge) - 1)
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    # assert chain.time() == tge + cliffDuration - 1
    assert tx.events['Withdrawn']['userVestingId'] == userVestingId
    assert tx.events['Withdrawn']['user'] == receiver
    assert tx.events['Withdrawn']['amount'] == 0

    chain.sleep(cliffDuration + tge - chain.time())
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    # assert chain.time() == tge + cliffDuration  # the 0th second of the vesting itself
    assert tx.events['Withdrawn']['userVestingId'] == userVestingId
    assert tx.events['Withdrawn']['user'] == receiver
    assert tx.events['Withdrawn']['amount'] == 0  # amountVesting * vestingInterval // vestingDuration

    chain.sleep(cliffDuration + tge + 1 - chain.time())
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    # assert chain.time() == tge + cliffDuration + 1  # the 1th second of the vesting itself
    print(tx.events)
    assert tx.events['Withdrawn']['amount'] == 0  # already withdrawn

    chain.sleep(tge + cliffDuration + vestingInterval - chain.time())
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    # assert chain.time() == tge + cliffDuration + vestingInterval  # 0 after vestingInterval
    print(tx.events)
    assert tx.events['Withdrawn']['amount'] == amountVesting * vestingInterval // vestingDuration

    chain.sleep(tge + cliffDuration + vestingInterval - chain.time() + 1)
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    # assert chain.time() == tge + cliffDuration + vestingInterval + 1  # 1 after vestingInterval
    print(tx.events)
    assert tx.events['Withdrawn']['amount'] == 0  # already withdrawn

    chain.sleep(tge + cliffDuration + 3 * vestingInterval - chain.time())
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    assert chain.time() == tge + cliffDuration + 3*vestingInterval  # 3 vestingInterval
    assert tx.events['Withdrawn']['amount'] == amountVesting * vestingInterval // vestingDuration * (3 - 1)

    chain.sleep(vestingInterval // 2)
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    assert tx.events['Withdrawn']['userVestingId'] == userVestingId
    assert tx.events['Withdrawn']['user'] == receiver
    assert tx.events['Withdrawn']['amount'] == 0  # no withdraw in the middle of the period
