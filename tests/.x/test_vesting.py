import datetime

from brownie import reverts


def test_DECIMAL_FACTOR(BP, admin):
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


def test_create_vesting_params2(admin, masd, vesting, chain):
    tgePercentage = 1000  # 10%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 0
    vestingInterval = 1
    with reverts('PercentageVestingLibrary: VESTING'):
        tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
    )


def test_create_vesting_params3(admin, masd, vesting, chain):
    tgePercentage = 1000  # 10%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 1
    vestingInterval = 0
    with reverts('PercentageVestingLibrary: VESTING'):
        tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
    )


def test_create_vesting_params4(admin, masd, vesting, chain):
    tgePercentage = 1000  # 10%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 0
    vestingInterval = 0
    with reverts('PercentageVestingLibrary: CLIFF'):
        tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
    )


def test_create_vesting_params5(admin, masd, vesting, chain):
    tgePercentage = 10000  # 100%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 1
    vestingInterval = 0
    with reverts('PercentageVestingLibrary: VESTING'):
        tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
    )


def test_create_vesting_params6(admin, masd, vesting, chain):
    tgePercentage = 10000  # 100%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 0
    vestingInterval = 0
    tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
    )


def test_create_vesting_params7(admin, masd, vesting, chain):
    tgePercentage = 10000  # 100%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 1
    vestingInterval = 10
    with reverts('PercentageVestingLibrary: VESTING'):
        tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
    )


def test_create_vesting_params8(admin, masd, vesting, chain):
    tgePercentage = 10000  # 100%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 0
    vestingInterval = 2
    with reverts('PercentageVestingLibrary: VESTING'):
        tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
    )


def test_create_vesting_params_zero_tge(admin, masd, vesting, chain):
    tgePercentage = 1000  # 10%
    tge = 0
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 0
    vestingInterval = 1
    with reverts('PercentageVestingLibrary: zero tge'):
        tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
    )


def test_create_vesting_cliff(admin, masd, vesting, chain):
    tgePercentage = 10001  # 100,1%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 6 * 30 * 24 * 3600
    vestingInterval = 1
    with reverts('PercentageVestingLibrary: CLIFF'):
        tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
    )


def test_create_vesting_cliff2(admin, masd, vesting, chain):
    tgePercentage = 10001  # 100,1%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 0
    vestingInterval = 0
    with reverts('PercentageVestingLibrary: CLIFF'):
        tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
    )


def test_create_vesting_cliff3(admin, masd, vesting, chain):
    tgePercentage = 10001
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 12
    vestingInterval = 0
    with reverts('PercentageVestingLibrary: CLIFF'):
        tx = vesting.createVestingParams(
        tgePercentage,
        tge,
        cliffDuration,
        vestingDuration,
        vestingInterval,
        {"from": admin}
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
    masd.approve(vesting, amountTotal, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        amountTotal,
        vestingParamsId,
        {"from": admin}
    )
    userVestingId = tx.events['UserVestingCreated']['userVestingId']
    assert userVestingId == 0

    assert vesting.getUserVesting(userVestingId) == (
        receiver,
        amountTotal,
        0,  # amountWithdrawn
        vestingParamsId,
        0  # avaliable
    )


def test_create_user_vesting_zero_amount(admin, masd, vesting, chain, user0, user1):
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
    amountTotal = 0

    masd.mint(user0, amountTotal, {"from": admin})
    masd.approve(vesting, amountTotal, {"from": admin})
    with reverts("ZERO_AMOUNT"):
        tx = vesting.createUserVesting(
        receiver,
        amountTotal,
        vestingParamsId,
        {"from": admin}
    )


def test_create_user_vesting_zero_address(admin, masd, vesting, chain, user0, user1):
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
    receiver ='0x0000000000000000000000000000000000000000'
    amountTotal = 0

    masd.mint(user0, amountTotal, {"from": admin})
    masd.approve(vesting, amountTotal, {"from": admin})
    with reverts("ZERO_ADDRESS"):
        tx = vesting.createUserVesting(
        receiver,
        amountTotal,
        vestingParamsId,
        {"from": admin}
    )


def test_withdraw_not_receiver(admin, masd, vesting, chain, user0, user1, user2):
    tgePercentage = 1000  # 10%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 6 * 30 * 24 * 3600
    vestingInterval = 1  # 1 sec
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
    masd.approve(vesting, amountTotal, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        amountTotal,
        vestingParamsId,
        {"from": admin}
    )
    userVestingId = tx.events['UserVestingCreated']['userVestingId']
    assert userVestingId == 0
    assert vesting.getUserVesting(userVestingId) == (
        receiver,
        amountTotal,
        0,  # amountWithdrawn
        vestingParamsId,
        0  # avaliable
    )

    with reverts("NOT_RECEIVER"):
        tx = vesting.withdraw(userVestingId, {"from": user2})


def test_withdraw_user_vesting(admin, masd, vesting, chain, user0, user1):
    tgePercentage = 1000  # 10%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 6 * 30 * 24 * 3600
    vestingInterval = 1  # 1 sec
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
    masd.approve(vesting, amountTotal, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        amountTotal,
        vestingParamsId,
        {"from": admin}
    )
    userVestingId = tx.events['UserVestingCreated']['userVestingId']
    assert userVestingId == 0
    assert vesting.getUserVesting(userVestingId) == (
        receiver,
        amountTotal,
        0,  # amountWithdrawn
        vestingParamsId,
        0  # avaliable
    )

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
    assert tx.events['Withdrawn']['amount'] == 0

    chain.sleep(1)
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    last_time = tx.timestamp
    if chain.time() == tge + cliffDuration:  # the 0th second of the vesting itself
        # it's difficult to exactly test it because of the chain specific
        assert tx.events['Withdrawn']['amount'] == 0

    chain.sleep(vestingInterval * 3)
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    period = tx.timestamp - last_time
    assert tx.events['Withdrawn']['userVestingId'] == userVestingId
    assert tx.events['Withdrawn']['user'] == receiver
    assert tx.events['Withdrawn']['amount'] == amountVesting // vestingDuration * period


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
    masd.approve(vesting, amountTotal, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        amountTotal,
        vestingParamsId,
        {"from": admin}
    )
    userVestingId = tx.events['UserVestingCreated']['userVestingId']
    assert userVestingId == 0

    assert vesting.getUserVesting(userVestingId) == (
        receiver,  # receiver
        amountTotal,  # amountTotal
        0,  # amountWithdrawn
        vestingParamsId,  # vestingParamsId
        0  # available
    )

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

    chain.mine()  # necessary for view method
    assert vesting.getUserVesting(userVestingId) == (
        receiver,  # receiver
        amountTotal,  # amountTotal
        0,  # amountWithdrawn
        vestingParamsId,  # vestingParamsId
        int(tgePercentage * amountTotal // 10_000),  # available
    )
    assert vesting.getWalletInfo(receiver) == (
        amountTotal,  # amountTotal
        0,  # amountWithdrawn
        int(tgePercentage * amountTotal // 10_000),  # available
    )

    tx = vesting.withdraw(userVestingId, {"from": receiver})
    assert tx.events['Withdrawn']['userVestingId'] == userVestingId
    assert tx.events['Withdrawn']['user'] == receiver
    assert tx.events['Withdrawn']['amount'] == int(tgePercentage * amountTotal // 10_000)

    assert vesting.getUserVesting(userVestingId) == (
        receiver,  # receiver
        amountTotal,  # amountTotal
        int(tgePercentage * amountTotal // 10_000),  # amountWithdrawn
        vestingParamsId,  # vestingParamsId
        0,  # available
    )

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
    assert tx.events['Withdrawn']['amount'] == 0

    chain.sleep(cliffDuration + tge + 1 - chain.time())
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    # assert chain.time() == tge + cliffDuration + 1  # the 1th second of the vesting itself
    print(tx.events)
    assert tx.events['Withdrawn']['amount'] == 0

    chain.sleep(tge + cliffDuration + vestingInterval - chain.time())
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    # assert chain.time() == tge + cliffDuration + vestingInterval  # 0 after vestingInterval
    print(tx.events)
    assert tx.events['Withdrawn']['amount'] == amountVesting * vestingInterval // vestingDuration

    assert vesting.getUserVesting(userVestingId) == (
        receiver,  # receiver
        amountTotal,  # amountTotal
        int(tgePercentage * amountTotal // 10_000) + amountVesting * vestingInterval // vestingDuration,  # amountWithdrawn
        vestingParamsId,  # vestingParamsId
        0,  # available
    )

    chain.sleep(tge + cliffDuration + vestingInterval - chain.time() + 1)
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    # assert chain.time() == tge + cliffDuration + vestingInterval + 1  # 1 after vestingInterval
    print(tx.events)
    assert tx.events['Withdrawn']['amount'] == 0  # already withdrawn

    chain.sleep(tge + cliffDuration + 3 * vestingInterval - chain.time())
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    # assert chain.time() == tge + cliffDuration + 3*vestingInterval  # 3 vestingInterval
    assert tx.events['Withdrawn']['amount'] == amountVesting * vestingInterval // vestingDuration * (3 - 1)

    assert vesting.getUserVesting(userVestingId) == (
        receiver,  # receiver
        amountTotal,  # amountTotal
        int(tgePercentage * amountTotal // 10_000) + 3 * amountVesting * vestingInterval // vestingDuration,  # amountWithdrawn
        vestingParamsId,  # vestingParamsId
        0,  # available
    )

    chain.sleep(vestingInterval // 2)
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    assert tx.events['Withdrawn']['amount'] == 0  # no withdraw in the middle of the period
    assert vesting.getUserVesting(userVestingId) == (
        receiver,  # receiver
        amountTotal,  # amountTotal
        int(tgePercentage * amountTotal // 10_000) + 3 * amountVesting * vestingInterval // vestingDuration,  # amountWithdrawn
        vestingParamsId,  # vestingParamsId
        0,  # available
    )

    vesting_interval_amount = amountVesting * vestingInterval // vestingDuration
    vesting_intervals_end = tge + cliffDuration + (amountVesting // vesting_interval_amount) * vestingInterval
    chain.sleep(vesting_intervals_end - chain.time())
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    assert tx.events['Withdrawn']['amount'] == (amountVesting // vesting_interval_amount - 3) * vesting_interval_amount
    amountWithdrawn = int(tgePercentage * amountTotal // 10_000) + amountVesting // vesting_interval_amount * vesting_interval_amount
    assert vesting.getUserVesting(userVestingId) == (
        receiver,  # receiver
        amountTotal,  # amountTotal
        amountWithdrawn,  # amountWithdrawn
        vestingParamsId,  # vestingParamsId
        0,  # available
    )
    assert amountWithdrawn == amountTotal



def test_withdrawAll(admin, masd, vesting, chain, user0, user1, user2):
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
    masd.approve(vesting, amountTotal, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        amountTotal,
        vestingParamsId,
        {"from": admin}
    )
    userVestingId = tx.events['UserVestingCreated']['userVestingId']
    assert userVestingId == 0

    assert vesting.getUserVesting(userVestingId) == (
        receiver,  # receiver
        amountTotal,  # amountTotal
        0,  # amountWithdrawn
        vestingParamsId,  # vestingParamsId
        0  # available
    )

    tx = vesting.withdrawAll({"from": receiver})
    assert vesting.getUserVesting(userVestingId) == (
        receiver,  # receiver
        amountTotal,  # amountTotal
        0,  # amountWithdrawn
        vestingParamsId,  # vestingParamsId
        0,  # available
    )


def test_withdrawAll_2(admin, masd, vesting, chain, user0, user1, user2):
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
    masd.approve(vesting, amountTotal, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        amountTotal,
        vestingParamsId,
        {"from": admin}
    )
    userVestingId = tx.events['UserVestingCreated']['userVestingId']
    assert userVestingId == 0

    assert vesting.getUserVesting(userVestingId) == (
        receiver,  # receiver
        amountTotal,  # amountTotal
        0,  # amountWithdrawn
        vestingParamsId,  # vestingParamsId
        0  # available
    )

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

    chain.mine()  # necessary for view method
    assert vesting.getUserVesting(userVestingId) == (
        receiver,  # receiver
        amountTotal,  # amountTotal
        0,  # amountWithdrawn
        vestingParamsId,  # vestingParamsId
        int(tgePercentage * amountTotal // 10_000),  # available
    )

    tx = vesting.withdrawAll({"from": receiver})
    assert vesting.getUserVesting(userVestingId) == (
        receiver,  # receiver
        amountTotal,  # amountTotal
        int(tgePercentage * amountTotal // 10_000),  # amountWithdrawn
        vestingParamsId,  # vestingParamsId
        0,  # available
    )


def test_withdraw_user_vesting_1sec(admin, masd, vesting, chain, user0, user1):
    tgePercentage = 1000  # 10%
    tge = chain.time() + 3600
    cliffDuration = 30 * 24 * 3600  # 30 days
    vestingDuration = 100  # for easy calculations
    vestingInterval = 1  # 1 sec
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
    masd.approve(vesting, amountTotal, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        amountTotal,
        vestingParamsId,
        {"from": admin}
    )
    userVestingId = tx.events['UserVestingCreated']['userVestingId']
    assert userVestingId == 0
    assert vesting.getUserVesting(userVestingId) == (
        receiver,
        amountTotal,
        0,  # amountWithdrawn
        vestingParamsId,
        0  # avaliable
    )

    with reverts('NOT_RECEIVER'):
        tx = vesting.withdraw(userVestingId, {"from": admin})

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
    assert tx.events['Withdrawn']['amount'] == 0

    chain.sleep(1)
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    last_time = tx.timestamp
    if chain.time() == tge + cliffDuration:  # the 0th second of the vesting itself
        # it's difficult to exactly test it because of the chain specific
        assert tx.events['Withdrawn']['amount'] == 0
    w1 = tx.events['Withdrawn']['amount']

    chain.sleep(vestingInterval * 3)
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    period = tx.timestamp - last_time
    assert tx.events['Withdrawn']['userVestingId'] == userVestingId
    assert tx.events['Withdrawn']['user'] == receiver
    assert tx.events['Withdrawn']['amount'] == amountVesting // vestingDuration * period
    w2 = amountVesting // vestingDuration * period

    vesting_interval_amount = amountVesting * vestingInterval // vestingDuration
    assert vesting_interval_amount == 9 * 10**18 / 100
    vesting_intervals_end = tge + cliffDuration + (amountVesting // vesting_interval_amount)
    assert vesting_intervals_end == tge + cliffDuration + vestingDuration
    chain.sleep(vesting_intervals_end - chain.time())
    tx = vesting.withdraw(userVestingId, {"from": receiver})
    assert tx.events['Withdrawn']['amount'] == \
           (amountVesting // vesting_interval_amount) * vesting_interval_amount - w1 - w2
    amountWithdrawn = int(tgePercentage * amountTotal // 10_000) + amountVesting // vesting_interval_amount * vesting_interval_amount
    assert vesting.getUserVesting(userVestingId) == (
        receiver,  # receiver
        amountTotal,  # amountTotal
        amountWithdrawn,  # amountWithdrawn
        vestingParamsId,  # vestingParamsId
        0,  # available
    )
    assert amountWithdrawn == amountTotal


def test_withdraw_user_vesting_daily_intervals_withdrawAll_for2vestings(admin, masd, vesting, chain, user0, user1):
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

    masd.mint(admin, amountTotal, {"from": admin})
    masd.approve(vesting, amountTotal, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        amountTotal,
        vestingParamsId,
        {"from": admin}
    )
    userVestingId = tx.events['UserVestingCreated']['userVestingId']
    assert userVestingId == 0

    masd.mint(admin, amountTotal, {"from": admin})
    masd.approve(vesting, amountTotal, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        amountTotal,
        vestingParamsId,
        {"from": admin}
    )
    userVestingId = tx.events['UserVestingCreated']['userVestingId']
    assert userVestingId == 1

    chain.sleep(tge + cliffDuration + vestingInterval - chain.time())
    tx = vesting.withdrawAll({"from": receiver})
    assert tx.events['TotalWithdrawn']['amount'] == 2 * \
           ((tgePercentage * amountTotal // 10000) + amountVesting * vestingInterval // vestingDuration)


def test_create_team_vesting_withdrawAll(admin, masd, vesting, chain, user0):
    receiver = user0

    dt = datetime.datetime.fromtimestamp(chain.time())
    if (dt.month, dt.day) >= (2, 25):
        dt = dt.replace(year=dt.year+1)

    tge1 = dt.replace(month=2, day=25, hour=0, minute=0, second=0, microsecond=0).timestamp()
    tge1 = int(tge1)
    tgePercentage1 = 0
    cliffDuration1 = 0
    vestingDuration1 = 365 * 24 * 3600
    vestingInterval1 = 30 * 24 * 3600
    tx1 = vesting.createVestingParams(
        tgePercentage1,
        tge1,
        cliffDuration1,
        vestingDuration1,
        vestingInterval1,
        {"from": admin}
    )
    params1 = tx1.events['VestingParamsCreated']['vestingParamsId']


    tge2 = tge1 + 365 * 24 * 3600
    tgePercentage2 = 0
    cliffDuration2 = 0
    vestingDuration2 = 365 * 24 * 3600
    vestingInterval2 = 30 * 24 * 3600
    tx2 = vesting.createVestingParams(
        tgePercentage2,
        tge2,
        cliffDuration2,
        vestingDuration2,
        vestingInterval2,
        {"from": admin}
    )
    params2 = tx2.events['VestingParamsCreated']['vestingParamsId']

    totalAmount1 = 300_000 * 12 * 10**18
    masd.mint(admin, totalAmount1, {"from": admin})
    masd.approve(vesting, totalAmount1, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        totalAmount1,
        params1,
        {"from": admin}
    )
    userVestingId1 = tx.events['UserVestingCreated']['userVestingId']


    totalAmount2 = 950_000 * 12 * 10**18
    masd.mint(admin, totalAmount2, {"from": admin})
    masd.approve(vesting, totalAmount2, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        totalAmount2,
        params2,
        {"from": admin}
    )
    userVestingId2 = tx.events['UserVestingCreated']['userVestingId']

    assert totalAmount1 + totalAmount2 == 15 * 10**6 * 10**18

    print(f'{tge2=}')
    print(f'{vestingDuration2=}')
    chain.sleep(tge2 + vestingDuration2 - chain.time())
    balanceBefore = masd.balanceOf(receiver)
    vesting.withdrawAll({"from": receiver})
    balanceAfter = masd.balanceOf(receiver)
    assert balanceAfter - balanceBefore == 15 * 10**6 * 10**18



def test_create_team_vesting_withdrawStepByStep(admin, masd, vesting, chain, user0):
    receiver = user0

    dt = datetime.datetime.fromtimestamp(chain.time())
    if (dt.month, dt.day) >= (2, 25):
        dt = dt.replace(year=dt.year+1)

    tge1 = dt.replace(month=2, day=25, hour=0, minute=0, second=0, microsecond=0).timestamp()
    tge1 = int(tge1)
    tgePercentage1 = 0
    cliffDuration1 = 0
    vestingDuration1 = 365 * 24 * 3600
    vestingInterval1 = 30 * 24 * 3600
    tx1 = vesting.createVestingParams(
        tgePercentage1,
        tge1,
        cliffDuration1,
        vestingDuration1,
        vestingInterval1,
        {"from": admin}
    )
    params1 = tx1.events['VestingParamsCreated']['vestingParamsId']


    tge2 = tge1 + 365 * 24 * 3600
    tgePercentage2 = 0
    cliffDuration2 = 0
    vestingDuration2 = 365 * 24 * 3600
    vestingInterval2 = 30 * 24 * 3600
    tx2 = vesting.createVestingParams(
        tgePercentage2,
        tge2,
        cliffDuration2,
        vestingDuration2,
        vestingInterval2,
        {"from": admin}
    )
    params2 = tx2.events['VestingParamsCreated']['vestingParamsId']

    totalAmount1 = 300_000 * 12 * 10**18
    masd.mint(admin, totalAmount1, {"from": admin})
    masd.approve(vesting, totalAmount1, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        totalAmount1,
        params1,
        {"from": admin}
    )
    userVestingId1 = tx.events['UserVestingCreated']['userVestingId']


    totalAmount2 = 950_000 * 12 * 10**18
    masd.mint(admin, totalAmount2, {"from": admin})
    masd.approve(vesting, totalAmount2, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        totalAmount2,
        params2,
        {"from": admin}
    )
    userVestingId2 = tx.events['UserVestingCreated']['userVestingId']

    assert totalAmount1 + totalAmount2 == 15 * 10**6 * 10**18

    balanceBefore = masd.balanceOf(receiver)

    chain.sleep(tge1 - chain.time())
    delta_before = 0
    while True:
        vesting.withdrawAll({"from": receiver})
        balanceAfter = masd.balanceOf(receiver)
        balanceDelta = balanceAfter - balanceBefore
        print(f'date: {datetime.datetime.fromtimestamp(chain.time()).date()}, '
              f'tokens: {int(balanceDelta/10**18/1000)}k, '
              f'withdrawn: {int((balanceDelta-delta_before)/10**18/1000)}k')
        delta_before = balanceDelta
        if chain.time() >= tge2 + vestingDuration2:
            break
        chain.sleep(30 * 24 * 3600)
    balanceAfter = masd.balanceOf(receiver)
    assert balanceAfter - balanceBefore == 15 * 10**6 * 10**18
    assert False
