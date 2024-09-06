from datetime import datetime
import hashlib
from pathlib import Path
import sqlite3
from uuid import uuid4

from constants.constants import BLOCK_MINING_DIFFICULTY
from constants.filepaths import DB_PATH


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float = 0.0, note: str = ""):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.now()
        self.id = f"T-{uuid4()}"
        self.note = note

    def get_transaction_id(self) -> str:
        return self.id

    def get_sender(self) -> str:
        return self.sender

    def get_receiver(self) -> str:
        return self.receiver

    def get_amount(self) -> str:
        return self.amount

    def get_timestamp(self) -> str:
        return self.timestamp

    def get_transaction_note(self) -> str:
        return self.note

    def save_transaction(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        with connection:
            cursor.execute(
                """INSERT INTO transactions(transaction_id,sender,receiver,amount,transaction_time,note) VALUES (?,?,?,?,?,?)""",
                self.id,
                self.sender,
                self.receiver,
                self.amount,
                self.timestamp,
                self.note,
            )
            connection.commit()

    def get_transaction_by_id(self, transaction_id: str):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        with connection:
            cursor.execute("""SELECT transaction_id,sender,receiver,amount,transaction_time,note FROM transactions where transaction_id =?""", transaction_id)
            transaction = cursor.fetchone()
            return {
                "transaction_id": transaction[0],
                "sender": transaction[1],
                "receiver": transaction[2],
                "amount": transaction[3],
                "transaction_time": transaction[4],
                "note": transaction[5],
            }

    def __repr__(self) -> str:
        return f"Transaction(ID={self.id}, sender={self.sender}, receiver={self.receiver}, amount={self.amount}, note={self.note}"


class Block:
    def __init__(self, previous_hash: str, transaction_id: str, nonce: int, index: int):
        self.index = index
        self.previous_hash = previous_hash
        self.transaction_id = transaction_id
        self.nonce = nonce

        self.hash = self.calculate_hash()
        # initialize

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int = 4):
        # Mine the block by finding a hash that starts with a certain number of leading zeros. The difficulty is defined by the number of zeros.
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def __repr__(self):
        # This is to print the block object
        return f"(Block(index={self.index}, hash={self.hash}, previous_hash={self.previous_hash}, transaction_id={self.transaction_id},,nonce={self.nonce})"


class Blockchain:
    def __init__(self, db_path: Path = DB_PATH, difficulty: int = BLOCK_MINING_DIFFICULTY):
        self.db_path = db_path
        self.difficulty = difficulty

    def create_chain_table(self):
        conn = sqlite3.connect(str(DB_PATH))
        with conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS blockchain (index INT, hash TEXT, prev_hash TEXT,transaction_id TEXT,nounce INT )""")

    def create_genesis_block(self):
        # Pass a Dummy Transaction
        dummy_transaction = Transaction(sender="Dummy", receiver="Dummy", amount=0.0, note="Genesis block transaction")
        dummy_transaction.save_transaction()

        genesis_block = Block(previous_hash="none", transaction_id=dummy_transaction.get_transaction_id(), nonce=0, index=0)
        genesis_block.mine_block(self.difficulty)
        self.save_block(genesis_block)

    def get_block_count(self):
        conn = sqlite3.connect(str(DB_PATH))
        with conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT count(*) FROM blockchain""")
            return cursor.fetchone()[0]

    def get_latest_block_hash(self):
        conn = sqlite3.connect(str(DB_PATH))
        with conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT index, previous_hash, nonce from blockchain WHERE index=(SELECT MAX(index) FROM blockchain)""")
            row = cursor.fetchone()
            block_string = f"{row[0]}{row[1],row[2]}"
            return hashlib.sha256(block_string.encode()).hexdigest()

    def save_block(self, block: Block):
        conn = sqlite3.connect(str(DB_PATH))
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO blockchain (index, hash, prev_hash,transaction_id ,nounce) VALUES(?,?,?,?,?)""",
                block.index,
                block.hash,
                block.previous_hash,
                block.transaction_id,
                block.nonce,
            )
            conn.commit()

    def add_block(self, block: Block):
        block.previous_hash = self.get_latest_block_hash()
        self.save_block(block)

    def is_chain_valid(self):
        conn = sqlite3.connect(str(DB_PATH))
        with conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT index, hash, prev_hash,transaction_id ,nounce from blockchain ORDER BY index ASC""")
            blocks = cursor.fetchall()
            for i in range(1, len(blocks)):
                current_block_row = blocks[i]
                previous_block_row = blocks[i - 1]
                current_block = Block(current_block_row[2], current_block_row[3], current_block_row[4], i)
                previous_block = Block(previous_block_row[2], previous_block_row[3], previous_block_row[4], i - 1)

                # Check if current block's hash is valid
                if current_block.calculate_hash() != current_block.hash:
                    return False
                # current block's previous hash = previous_block hash
                if current_block.previous_hash != previous_block.hash:
                    return False
            return True
