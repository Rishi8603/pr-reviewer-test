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
