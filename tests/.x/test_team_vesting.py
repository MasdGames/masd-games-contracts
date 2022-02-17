import datetime

from brownie import reverts


def test_create_team_vesting_withdrawStepByStep_360(admin, masd, vesting, chain, user0):
    receiver = user0

    year = 360

    dt = datetime.datetime.fromtimestamp(chain.time())
    if (dt.month, dt.day) >= (2, 25):
        dt = dt.replace(year=dt.year + 1)

    tge1 = dt.replace(month=2, day=25, hour=0, minute=0, second=0, microsecond=0).timestamp()
    tge1 = int(tge1)
    tgePercentage1 = 0
    cliffDuration1 = 0
    vestingDuration1 = year * 24 * 3600
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

    tge2 = tge1 + year * 24 * 3600
    tgePercentage2 = 0
    cliffDuration2 = 0
    vestingDuration2 = year * 24 * 3600
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

    totalAmount1 = 300_000 * 12 * 10 ** 18
    print(f'totalAmount1 = {int(totalAmount1 / 10**18 / 1000)}k')
    print(f'vestedPerInterval1 = totalVestingAmount * self.vestingInterval / self.vestingDuration = '
          f'{int((totalAmount1 * vestingInterval1 // vestingDuration1) / 10**18 / 1000)}k')
    masd.mint(admin, totalAmount1, {"from": admin})
    masd.approve(vesting, totalAmount1, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        totalAmount1,
        params1,
        {"from": admin}
    )
    userVestingId1 = tx.events['UserVestingCreated']['userVestingId']

    totalAmount2 = 950_000 * 12 * 10 ** 18
    print(f'totalAmount2 = {int(totalAmount1 / 10**18 / 1000)}k')
    print(f'vestedPerInterval2 = totalVestingAmount * self.vestingInterval / self.vestingDuration = '
          f'{int((totalAmount2 * vestingInterval2 // vestingDuration2) / 10**18 / 1000)}k')


    print(f'tge1 = {datetime.datetime.fromtimestamp(tge1).date()}')
    print(f'tge2 = {datetime.datetime.fromtimestamp(tge2).date()}')


    masd.mint(admin, totalAmount2, {"from": admin})
    masd.approve(vesting, totalAmount2, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        totalAmount2,
        params2,
        {"from": admin}
    )
    userVestingId2 = tx.events['UserVestingCreated']['userVestingId']

    assert totalAmount1 + totalAmount2 == 15 * 10 ** 6 * 10 ** 18

    balanceBefore = masd.balanceOf(receiver)

    chain.sleep(tge1 - chain.time())
    delta_before = 0
    while True:
        vesting.withdrawAll({"from": receiver})
        balanceAfter = masd.balanceOf(receiver)
        balanceDelta = balanceAfter - balanceBefore
        if balanceDelta > delta_before:
            print(f'date: {datetime.datetime.fromtimestamp(chain.time()).date()}, '
                  f'tokens: {int(balanceDelta / 10 ** 18 / 1000)}k, '
                  f'withdrawn: {int((balanceDelta - delta_before) / 10 ** 18 / 1000)}k')
            delta_before = balanceDelta
        if chain.time() >= tge2 + vestingDuration2:
            break
        chain.sleep(24 * 3600 + 1)
    balanceAfter = masd.balanceOf(receiver)
    assert balanceAfter - balanceBefore == 15 * 10 ** 6 * 10 ** 18



def test_create_team_vesting_withdrawStepByStep_365(admin, masd, vesting, chain, user0):
    receiver = user0

    year = 365

    dt = datetime.datetime.fromtimestamp(chain.time())
    if (dt.month, dt.day) >= (2, 25):
        dt = dt.replace(year=dt.year + 1)

    tge1 = dt.replace(month=2, day=25, hour=0, minute=0, second=0, microsecond=0).timestamp()
    tge1 = int(tge1)
    tgePercentage1 = 0
    cliffDuration1 = 0
    vestingDuration1 = year * 24 * 3600
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

    tge2 = tge1 + year * 24 * 3600
    tgePercentage2 = 0
    cliffDuration2 = 0
    vestingDuration2 = year * 24 * 3600
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

    totalAmount1 = 300_000 * 12 * 10 ** 18
    print(f'totalAmount1 = {int(totalAmount1 / 10**18 / 1000)}k')
    print(f'vestedPerInterval1 = totalVestingAmount * self.vestingInterval / self.vestingDuration = '
          f'{int((totalAmount1 * vestingInterval1 // vestingDuration1) / 10**18 / 1000)}k')
    masd.mint(admin, totalAmount1, {"from": admin})
    masd.approve(vesting, totalAmount1, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        totalAmount1,
        params1,
        {"from": admin}
    )
    userVestingId1 = tx.events['UserVestingCreated']['userVestingId']

    totalAmount2 = 950_000 * 12 * 10 ** 18
    print(f'totalAmount2 = {int(totalAmount1 / 10**18 / 1000)}k')
    print(f'vestedPerInterval2 = totalVestingAmount * self.vestingInterval / self.vestingDuration = '
          f'{int((totalAmount2 * vestingInterval2 // vestingDuration2) / 10**18 / 1000)}k')


    print(f'tge1 = {datetime.datetime.fromtimestamp(tge1).date()}')
    print(f'tge2 = {datetime.datetime.fromtimestamp(tge2).date()}')


    masd.mint(admin, totalAmount2, {"from": admin})
    masd.approve(vesting, totalAmount2, {"from": admin})
    tx = vesting.createUserVesting(
        receiver,
        totalAmount2,
        params2,
        {"from": admin}
    )
    userVestingId2 = tx.events['UserVestingCreated']['userVestingId']

    assert totalAmount1 + totalAmount2 == 15 * 10 ** 6 * 10 ** 18

    balanceBefore = masd.balanceOf(receiver)

    chain.sleep(tge1 - chain.time())
    delta_before = 0
    while True:
        vesting.withdrawAll({"from": receiver})
        balanceAfter = masd.balanceOf(receiver)
        balanceDelta = balanceAfter - balanceBefore
        if balanceDelta > delta_before:
            print(f'date: {datetime.datetime.fromtimestamp(chain.time()).date()}, '
                  f'tokens: {int(balanceDelta / 10 ** 18 / 1000)}k, '
                  f'withdrawn: {int((balanceDelta - delta_before) / 10 ** 18 / 1000)}k')
            delta_before = balanceDelta
        if chain.time() >= tge2 + vestingDuration2:
            break
        chain.sleep(24 * 3600 + 1)
    balanceAfter = masd.balanceOf(receiver)
    assert balanceAfter - balanceBefore == 15 * 10 ** 6 * 10 ** 18
