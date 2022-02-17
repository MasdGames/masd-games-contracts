from brownie import *
import pytest


@pytest.fixture
def admin(accounts):
    return accounts[0]


@pytest.fixture
def users(accounts):
    return accounts[1:]


@pytest.fixture
def user0(users):
    return users[0]


@pytest.fixture
def user1(users):
    return users[1]
    
@pytest.fixture
def user2(users):
    return users[2]    


@pytest.fixture
def masd(admin):
    contract = MASD.deploy(10 * 10**18, admin, {"from": admin})
    return contract


@pytest.fixture
def vesting(admin, masd):
    contract = MASDVesting.deploy(masd, {"from": admin})
    return contract


@pytest.fixture
def mock_vesting(admin, masd):
    contract = MockMASDVesting.deploy({"from": admin})
    return contract


@pytest.fixture
def masd_signatures(masd, admin):
    contract = MASDSignatures.deploy(masd, {"from": admin})
    return contract

