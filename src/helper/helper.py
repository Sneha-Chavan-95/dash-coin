"""File to house all the `Helper` functions"""

import sqlite3
import random
from uuid import uuid4
import hashlib
from datetime import datetime

from constants.filepaths import DB_PATH

conn = sqlite3.connect(str(DB_PATH))
with conn:
    conn.execute("""CREATE TABLE IF NOT EXISTS users (email TEXT Primary Key,name TEXT, password TEXT, active TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS tokens (email TEXT Primary Key,token TEXT UNIQUE, valid DATETIME)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS balances (email TEXT Primary Key, balance DECIMAL , block_id TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS transactions(transaction_id TEXT,sender TEXT,receiver TEXT,amount DECIMAL,transaction_time DATETIME, note TEXT) """)


# ! API helper functions
def register_new_user(email: str, name: str, password: str) -> tuple[int, dict]:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    with connection:
        cursor.execute("INSERT INTO users(email,name,password) VALUES(?,?,?)", (email, name, generate_password_salt(password)))
        connection.commit()
        cursor.execute("INSERT INTO balances(email,balance,block_id) VALUES(?,?,?)", (email, 0.0, 0))
        connection.commit()
    return (
        201,
        {
            "message": f"User with email - {email} and {name} registered successfully",
        },
    )


def authenticate_user(email: str, password: str) -> tuple[int, dict]:
    connection = sqlite3.connect(DB_PATH)
    with connection:
        cursor = connection.cursor()
        # cursor.execute('SELECT count(*) FROM users WHERE email="?" AND password ="?" AND active ="Y"', (email, generate_password_salt(password)))
        cursor.execute("SELECT count(*) FROM users WHERE email=? AND password=?", (email, generate_password_salt(password)))
    if bool(cursor.fetchone()[0]):
        return (200, {"message": f"{create_token(email)}"})


def get_user_balance(token: str) -> tuple[int, float]:
    connection = sqlite3.connect(DB_PATH)
    with connection:
        cursor = connection.cursor()
    status, content = 403, {"message": 0.0}
    try:
        email = get_email_against_token(token)

        if not email:
            raise ValueError("No user found against token - {token}")

        balance = cursor.execute("SELECT balance from balances WHERE email=?", (email,))
        status, content = 200, {"message": balance}
    except:
        return (status, content)
    return (status, content)


def get_username_against_token(token: str) -> tuple[int, float]:
    connection = sqlite3.connect(DB_PATH)
    with connection:
        cursor = connection.cursor()
    status, content = 403, {"message": ""}
    try:
        email = get_email_against_token(token)

        if not email:
            raise ValueError("No user found against token - {token}")

        username = cursor.execute("SELECT name FROM users WHERE email=?", (email,)).fetchone()[0]
        status, content = 200, {"message": username}
    except:
        return (status, content)
    return (status, content)


def get_all_users(token: str) -> tuple[int, list[str]]:
    connection = sqlite3.connect(DB_PATH)
    with connection:
        cursor = connection.cursor()
    status, content = 403, {"message": []}
    try:
        email = get_email_against_token(token)

        if not email:
            raise ValueError("No user found against token - {token}")

        users = cursor.execute("SELECT email FROM users").fetchall()[0]
        status, content = 200, {"message": users}
    except:
        return (status, content)
    return (status, content)


def send_credit_user(receiver: str, amount: float, token: str) -> tuple[int, dict]:
    sender = get_email_against_token(token)
    if sender and is_user_valid(receiver) and get_user_balance(token) >= amount:
        # Create transaction
        # Create block
        # Mine block
        return (200, {})
    return (405, {})


def add_user_balance(amount: float, token: str) -> tuple[int, float]:
    status, new_balance = 403, 0.0
    connection = sqlite3.connect(DB_PATH)
    with connection:
        cursor = connection.cursor()
        try:
            user: str = get_email_against_token(token)
            if not user:
                raise ValueError("No user found against token - {token}")
            new_balance = get_user_balance(token)[1] + amount
            cursor.execute("UPDATE balances SET balance=? WHERE email=?", (new_balance, user))
            connection.commit()
            status, new_balance = get_user_balance(token)
        except Exception:
            return (status, new_balance)
        return (status, new_balance)


def request_credit_user(sender: str, receiver: str, amount: float, token: str) -> tuple[int, dict]:
    return (200, {})


def get_all_transactions(token: str) -> tuple[int, list[dict]]:
    return (200, [{}])


# ! Session management functions


def create_token(email) -> tuple[int, dict]:
    token = str(uuid4())
    connection = sqlite3.connect(DB_PATH)
    with connection:
        cursor = connection.cursor()
        # cursor.execute("INSERT INTO tokens(email,token,valid) VALUES(?,?,?)", (email, token, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        cursor.execute("INSERT INTO tokens(email,token,valid) VALUES(?,?,?)", (email, token, datetime.now()))
        connection.commit()
    return (201, {"message": token})


def get_email_against_token(token: str) -> str:
    connection = sqlite3.connect(DB_PATH)
    with connection:
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM tokens WHERE token=?", (token,))
        email = cursor.fetchone()[0]
        return ({"message": email}) if email else (401, {"message": f"No user Found against token - {token}"})


def is_user_valid(email: str) -> bool:
    connection = sqlite3.connect(DB_PATH)
    with connection:
        cursor = connection.cursor()
        # cursor.execute('SELECT count(*) FROM users WHERE email="?" AND active="Y"', email)
        cursor.execute("SELECT count(*) FROM users WHERE email=?", (email))
    return bool(cursor.fetchone())


def generate_otp(length: int = 4) -> str:
    return f'{random.randint(0,int("9" * length)):0{length}}'


def generate_password_salt(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def notify_user(email: str, body: str) -> bool: ...


def clear_token(token: str) -> tuple[int, dict]:
    connection = sqlite3.connect(DB_PATH)
    with connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tokens WHERE token=?", (token))
        connection.commit()
    if not bool(cursor.fetchone()):
        return (200, {"message": f"Token - {token} is deleted successfully"})


# ! Database functions
