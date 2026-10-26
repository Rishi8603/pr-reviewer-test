import pytest

from wallet import Wallet, WalletError


@pytest.fixture
def wallet() -> Wallet:
    return Wallet()


def test_new_account_starts_at_zero(wallet: Wallet) -> None:
    account = wallet.create_account("Asha")
    assert wallet.get_balance(account) == 0


def test_blank_name_is_rejected(wallet: Wallet) -> None:
    with pytest.raises(WalletError):
        wallet.create_account("   ")


def test_deposit_increases_balance(wallet: Wallet) -> None:
    account = wallet.create_account("Asha")
    assert wallet.deposit(account, 500) == 500


@pytest.mark.parametrize("amount", [0, -100, 10.5, True])
def test_invalid_deposit_amounts_are_rejected(wallet: Wallet, amount: object) -> None:
    account = wallet.create_account("Asha")
    with pytest.raises(WalletError):
        wallet.deposit(account, amount)


def test_unknown_account_is_rejected(wallet: Wallet) -> None:
    with pytest.raises(WalletError):
        wallet.get_balance(999)


def test_history_lists_deposits_newest_first(wallet: Wallet) -> None:
    account = wallet.create_account("Asha")
    for amount in (100, 200, 300):
        wallet.deposit(account, amount)
    assert wallet.get_history(account) == [300, 200, 100]


def test_history_respects_limit(wallet: Wallet) -> None:
    account = wallet.create_account("Asha")
    for amount in (100, 200, 300):
        wallet.deposit(account, amount)
    assert wallet.get_history(account, limit=2) == [300, 200]


def test_history_is_empty_for_new_account(wallet: Wallet) -> None:
    account = wallet.create_account("Asha")
    assert wallet.get_history(account) == []


def test_history_is_per_account(wallet: Wallet) -> None:
    asha = wallet.create_account("Asha")
    ravi = wallet.create_account("Ravi")
    wallet.deposit(asha, 100)
    assert wallet.get_history(ravi) == []


@pytest.mark.parametrize("limit", [0, 101, -1, 2.5])
def test_history_rejects_bad_limit(wallet: Wallet, limit: object) -> None:
    account = wallet.create_account("Asha")
    with pytest.raises(WalletError):
        wallet.get_history(account, limit=limit)


def test_history_rejects_unknown_account(wallet: Wallet) -> None:
    with pytest.raises(WalletError):
        wallet.get_history(999)


def test_transfer_moves_funds_between_accounts(wallet: Wallet) -> None:
    asha = wallet.create_account("Asha")
    ravi = wallet.create_account("Ravi")
    wallet.deposit(asha, 500)

    wallet.transfer(asha, ravi, 200)

    assert wallet.get_balance(asha) == 300
    assert wallet.get_balance(ravi) == 200


@pytest.mark.parametrize("amount", [0, -100, 10.5, True])
def test_transfer_rejects_invalid_amounts(wallet: Wallet, amount: object) -> None:
    asha = wallet.create_account("Asha")
    ravi = wallet.create_account("Ravi")
    wallet.deposit(asha, 500)

    with pytest.raises(WalletError):
        wallet.transfer(asha, ravi, amount)


def test_transfer_rolls_back_when_destination_missing(wallet: Wallet) -> None:
    asha = wallet.create_account("Asha")
    wallet.deposit(asha, 500)

    with pytest.raises(WalletError):
        wallet.transfer(asha, 999, 200)

    assert wallet.get_balance(asha) == 500
