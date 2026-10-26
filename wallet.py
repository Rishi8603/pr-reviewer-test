"""A minimal SQLite-backed wallet: accounts and balances, stored in paise."""

import sqlite3


class WalletError(Exception):
    """Raised when a wallet operation is not allowed."""


class Wallet:
    def __init__(self, path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(path)
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT NOT NULL,
                balance INTEGER NOT NULL DEFAULT 0 CHECK (balance >= 0)
            );
            CREATE TABLE IF NOT EXISTS transactions (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL REFERENCES accounts(id),
                amount     INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS ix_transactions_account
                ON transactions (account_id, id);
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
        # One transaction: the balance and its history row change together.
        with self.conn:
            self.conn.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (amount, account_id),
            )
            self.conn.execute(
                "INSERT INTO transactions (account_id, amount) VALUES (?, ?)",
                (account_id, amount),
            )
        return self.get_balance(account_id)

    def transfer(self, from_id: int, to_id: int, amount: int) -> None:
        """Move money from one account to another."""
        if type(amount) is not int or amount <= 0:
            raise WalletError("Transfer amount must be a positive integer.")
        with self.conn:
            row = self.conn.execute(
                "SELECT balance FROM accounts WHERE id = ?",
                (from_id,),
            ).fetchone()
            if row is None:
                raise WalletError(f"Account {from_id} does not exist.")
            if row[0] < amount:
                raise WalletError("Insufficient funds.")
            self.conn.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                (amount, from_id),
            )
            cursor = self.conn.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (amount, to_id),
            )
            if cursor.rowcount == 0:
                raise WalletError(f"Account {to_id} does not exist.")

    def get_history(self, account_id: int, limit: int = 10) -> list[int]:
        """Return the most recent transaction amounts, newest first."""
        if type(limit) is not int or not 1 <= limit <= 100:
            raise WalletError("limit must be an integer between 1 and 100.")
        self.get_balance(account_id)  # raises if the account is missing
        rows = self.conn.execute(
            "SELECT amount FROM transactions WHERE account_id = ? "
            "ORDER BY id DESC LIMIT ?",
            (account_id, limit),
        ).fetchall()
        return [amount for (amount,) in rows]
