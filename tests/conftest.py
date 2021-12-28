from brownie import *
import pytest


@pytest.fixture
def admin(accounts):
    return accounts[0]


@pytest.fixture
def users(accounts):
    return accounts[1:]


@pytest.fixture
def masd(admin):
    contract = MASD.deploy(1 * 10**18, admin, {"from": admin})
    return contract
