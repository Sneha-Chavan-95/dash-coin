"""File to house all the `Helper` functions"""

import sqlite3
import random

db_path = ("dashcoin.db",)
conn = sqlite3.connect(db_path)
with conn:
    conn.execute("""CREATE TABLE IF NOT EXISTS users (email TEXT Primary Key,name TEXT, password TEXT, active TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS tokens (token TEXT Primary Key, email TEXT, valid DATETIME)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS balances (email TEXT Primary Key, balance DECIMAL)""")


# ! API helper functions
def get_all_users(token: str) -> tuple[int, list[str]]:
    if get_user_against_token(token):
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM users WHERE active="Y"')
        users = cursor.fetchall()[0]
        return (200, users)
    return (403, [])


def send_credit_user(receiver: str, amount: float, token: str) -> tuple[int, dict]:
    sender = get_user_against_token(token)
    if sender and is_user_valid(receiver) and get_user_balance(token) >= amount:
        # Create transaction
        # Create block
        # Mine block
        return (200, {})
    return (405, {})


def register_new_users(email: str, name: str, password: str) -> tuple[int, dict]:
    cursor = conn.cursor()
    with conn:
        cursor.execute("INSERT INTO users(email,name,password) VALUES(?,?,?)", email, name, password)
        conn.commit()
    return (201, {})


def get_user_balance(token: str) -> tuple[int, float]:
    cursor = conn.cursor()
    user: str = get_user_against_token(token)
    balance: float = cursor.execute('SELECT balance from balances WHERE user ="?"', user)
    return (200, balance)


def add_user_balance(amount: float, token: str) -> tuple[int, float]:
    cursor = conn.cursor()
    user: str = get_user_against_token(token)
    new_balance = get_user_balance(token) + amount
    cursor.execute('UPDATE balances SET balance= "?" WHERE email= "?"', new_balance, user)
    return (200, 0.0)


def request_credit_user(sender: str, receiver: str, amount: float, token: str) -> tuple[int, dict]:
    return (200, {})


def get_all_transactions(token: str) -> tuple[int, list[dict]]:
    return (200, [{}])


# ! Session management functions


def create_token() -> str: ...


def get_user_against_token(token: str) -> str:
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM tokens WHERE token="?"', token)
    email: str = cursor.fetchone()[0]
    return email if email else ""


def is_user_valid(email: str) -> bool:
    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM users WHERE email="?" AND active="Y"', email)
    return bool(cursor.fetchone())


def generate_otp(length: int = 4) -> str:
    return f'{random.randint(0,int("9" * length)):0{length}}'


def generate_password_salt(password: str) -> str: ...


def authenticate_user(email: str, password: str) -> bool: ...


def notify_user(email: str, body: str) -> bool: ...


# ! Database functions
