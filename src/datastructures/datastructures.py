# three classes "Block" "Blockchain" "Transaction"
from datetime import datetime
import hashlib
from uuid import uuid4

class Block:
    def __init__(self, previous_hash: str, transactions: str, nonce: int, index):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
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

    def _repr_(self):
    # This is to print the block object
        return (f"Block(index={self.index}, hash={self.hash}, previous_hash={self.previous_hash}”,f"nonce={self.nonce})")


class Transaction:
    def _init_(self, sender: str, receiver: str, amount: float = 0.0, note: str = ""):
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

    def _repr_(self) -> str:
        return f"Transaction(ID={self.id}, sender={self.sender}, receiver={self.receiver}, amount={self.amount}, note={self.note}"


class Blockchain:
    def _init_(self):...

    def create_chain_table(): ...
    
    def create_genesis_block(): ... 
    # Pass a Dummy Transaction
   
    def get_block_count(): ...
    
    def get_latest_block(): ...
    
    def save_block():...
    
    def add_block():...
    
    def is_chain_valid()...
