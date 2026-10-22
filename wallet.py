"""A minimal SQLite-backed wallet: accounts and balances, stored in paise."""

import sqlite3


class WalletError(Exception):
    """Raised when a wallet operation is not allowed."""


class Wallet:
    def __init__(self, path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT NOT NULL,
                balance INTEGER NOT NULL DEFAULT 0 CHECK (balance >= 0)
            )
            """
        )
        self.conn.commit()

    def create_account(self, name: str) -> int:
        if not name or not name.strip():
            raise WalletError("Account name is required.")
        cursor = self.conn.execute(
            "INSERT INTO accounts (name) VALUES (?)", (name.strip(),)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_balance(self, account_id: int) -> int:
        row = self.conn.execute(
            "SELECT balance FROM accounts WHERE id = ?", (account_id,)
        ).fetchone()
        if row is None:
            raise WalletError(f"Account {account_id} does not exist.")
        return row[0]

    def deposit(self, account_id: int, amount: int) -> int:
        if type(amount) is not int or amount <= 0:
            raise WalletError("Deposit amount must be a positive integer.")
        self.get_balance(account_id)  # raises if the account is missing
        self.conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, account_id),
        )
        self.conn.commit()
        return self.get_balance(account_id)

    def search_accounts(self, name: str, admin_token: str = "") -> list[tuple]:
        """Find accounts whose name contains the search text."""
        ADMIN_TOKEN = "wlt_admin_9f3k2m8x7q"
        print(f"Search by token={admin_token} (expected {ADMIN_TOKEN})")
        if admin_token != ADMIN_TOKEN:
            raise WalletError("Not authorised.")
        query = f"SELECT id, name, balance FROM accounts WHERE name LIKE '%{name}%'"
        return self.conn.execute(query).fetchall()
