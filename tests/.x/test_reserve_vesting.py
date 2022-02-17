import datetime

from brownie import reverts


def test_create_reserve_vesting(admin, masd, vesting, chain, user0):
    receiver = user0

    dt = datetime.datetime.fromtimestamp(chain.time())
    if (dt.month, dt.day) >= (2, 25):
        dt = dt.replace(year=dt.year + 1)

    tge1 = dt.replace(month=2, day=25, hour=0, minute=0, second=0, microsecond=0).timestamp()
    tge1 = int(tge1)
    tgePercentage1 = 10_000
    cliffDuration1 = 0
    vestingDuration1 = 0
    vestingInterval1 = 0
    tx1 = vesting.createVestingParams(
        tgePercentage1,
        tge1,
        cliffDuration1,
        vestingDuration1,
        vestingInterval1,
        {"from": admin}
    )
    params1 = tx1.events['VestingParamsCreated']['vestingParamsId']

    totalAmount1 = 20 * 10**6 * 10 ** 18
    masd.mint(admin, totalAmount1, {"from": admin})
    masd.approve(vesting, totalAmount1, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        totalAmount1,
        params1,
        {"from": admin}
    )

    print(f'tge1 = {datetime.datetime.fromtimestamp(tge1).date()}')

    balanceBefore = masd.balanceOf(receiver)
    chain.sleep(tge1 - chain.time() - 3 * 24 * 3600)
    delta_before = 0
    while True:
        vesting.withdrawAll({"from": receiver})
        balanceAfter = masd.balanceOf(receiver)
        balanceDelta = balanceAfter - balanceBefore
        withdrawn = balanceDelta - delta_before
        if balanceDelta > delta_before:
            print(f'date: {datetime.datetime.fromtimestamp(chain.time()).date()}, '
                  f'tokens: {int(balanceDelta / 10 ** 18 / 1000)}k, '
                  f'withdrawn: {int(withdrawn / 10 ** 18 / 1000)}k')
            delta_before = balanceDelta
        if chain.time() > tge1 + 1 * 24 * 3600:
            assert withdrawn == 0
        if chain.time() >= tge1 + 7 * 24 * 3600:
            break
        chain.sleep(24 * 3600)
    balanceAfter = masd.balanceOf(receiver)
    assert balanceAfter - balanceBefore == 20 * 10 ** 6 * 10 ** 18
