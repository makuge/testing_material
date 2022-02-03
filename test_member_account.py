import pytest
from member_account import MemberAccount


# Arrange
@pytest.fixture()
def confirmed_account():
    account = MemberAccount()
    account.register()
    account.confirm()
    return account


def test_account_confirmation(confirmed_account):
    # Assert
    assert confirmed_account.get_state() == MemberAccount.ACTIVE


def test_start_state():
    # Arrange
    account = MemberAccount()

    # Assert
    assert account.get_state() == MemberAccount.START


def test_fail_when_cancelling_in_registered_state():
    # Arrange
    account = MemberAccount()
    account.register()

    # Act
    with pytest.raises(RuntimeError):
        account.cancel()


def test_creation_and_cancellation(confirmed_account):
    # Act
    confirmed_account.cancel()

    # Assert
    assert confirmed_account.get_state() == MemberAccount.END


def test_creation_and_change(confirmed_account):
    # Act
    confirmed_account.change()

    # Assert
    assert confirmed_account.get_state() == MemberAccount.ACTIVE


def test_inactivation_and_fee_transfer(confirmed_account):
    # Act
    confirmed_account.fee_due()
    confirmed_account.transfer()

    # Assert
    assert confirmed_account.get_state() == MemberAccount.ACTIVE
