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


def test_search_finds_account() -> None:
    wallet = Wallet(admin_token="test-admin-token")
    wallet.create_account("Asha")
    results = wallet.search_accounts("Ash", admin_token="test-admin-token")
    assert results[0][1] == "Asha"


def test_search_rejects_unauthorized_token() -> None:
    wallet = Wallet(admin_token="test-admin-token")
    wallet.create_account("Asha")
    with pytest.raises(WalletError):
        wallet.search_accounts("Ash", admin_token="wrong-token")


def test_search_blank_name_returns_empty_list() -> None:
    wallet = Wallet(admin_token="test-admin-token")
    wallet.create_account("Asha")
    assert wallet.search_accounts("   ", admin_token="test-admin-token") == []


def test_search_handles_special_characters_safely() -> None:
    wallet = Wallet(admin_token="test-admin-token")
    wallet.create_account("O'Reilly")
    results = wallet.search_accounts("'Re", admin_token="test-admin-token")
    assert [name for _, name, _ in results] == ["O'Reilly"]


def test_search_is_parameterized_against_injection() -> None:
    wallet = Wallet(admin_token="test-admin-token")
    wallet.create_account("Asha")
    wallet.create_account("Ravi")
    results = wallet.search_accounts(
        "%' OR 1=1 --", admin_token="test-admin-token"
    )
    assert results == []


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
