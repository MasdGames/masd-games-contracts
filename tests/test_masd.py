from brownie import *
from brownie import reverts
from web3.constants import *


def test_mint_no_minter(masd, users, admin):
    amount = 42
    with reverts(f"AccessControl: account {users[0].address.lower()} is missing role {masd.MINTER_ROLE()}"):
        tx = masd.mint(users[0], amount, {"from": users[0]})


def test_mint_small(masd, users, admin):
    amount = 42
    tx = masd.mint(users[0], amount, {"from": admin})
    assert tx.events['Transfer']['from'] == ADDRESS_ZERO
    assert tx.events['Transfer']['to'] == users[0]
    assert tx.events['Transfer']['value'] == amount


def test_mint_small_18(masd, users, admin):
    amount = 42 * 10**18
    tx = masd.mint(users[0], amount, {"from": admin})
    assert tx.events['Transfer']['from'] == ADDRESS_ZERO
    assert tx.events['Transfer']['to'] == users[0]
    assert tx.events['Transfer']['value'] == amount


def test_mint_too_high(masd, users, admin):
    amount = masd.cap() - masd.totalSupply() + 1
    with reverts('ERC20Capped: cap exceeded'):
        tx = masd.mint(users[0], amount, {"from": admin})


def test_role_member(masd, users, admin):
    assert masd.getRoleMemberCount(masd.DEFAULT_ADMIN_ROLE()) == 1
    assert masd.getRoleMember(masd.DEFAULT_ADMIN_ROLE(), 0) == admin
    assert masd.getRoleMemberCount(masd.MINTER_ROLE()) == 1
    assert masd.getRoleMember(masd.MINTER_ROLE(), 0) == admin
