from member_account import MemberAccount


def test_cancellation_of_account():
    account = MemberAccount()
    account.register()
    account.confirm()
    account.cancel()
    assert account.get_state() == MemberAccount.END


def test_change_of_active_account():
    account = MemberAccount()
    account.register()
    account.confirm()
    account.change()
    assert account.get_state() == MemberAccount.ACTIVE


def test_annual_fee():
    account = MemberAccount()
    account.register()
    account.confirm()
    account.fee_due()
    account.transfer()
    assert account.get_state() == MemberAccount.ACTIVE


def test_account_suspension():
    account = MemberAccount()
    account.register()
    account.confirm()
    account.suspend()
    account.reactivate()
    assert account.get_state() == MemberAccount.ACTIVE
