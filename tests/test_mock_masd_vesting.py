def test_simple(mock_vesting, admin):
    info = mock_vesting.getWalletInfo(admin)
    assert info == {}
