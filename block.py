import datetime
from hashlib import sha256

class Block:
    def __init__(self, transactions, previous_hash):
        self.time_stamp = datetime.datetime.now()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.generate_hash()

    def generate_hash(self):
        block_header = str(self.time_stamp) + str(self.transactions) +str(self.previous_hash) + str(self.nonce)
        block_hash = sha256(block_header.encode())
        return block_hash.hexdigest()

    def print_contents(self):
        print("timestamp:", self.time_stamp)
        print("transactions:", self.transactions)
        print("current hash:", self.generate_hash())
        print("previous hash:", self.previous_hash)
        print("")

    def update_timestamp(self):
        timestamp = str(self.time_stamp)
        return timestamp
    
    def update_transactions(self):
        transactions = str(self.transactions)
        return transactions

    def update_current_hash(self):
        current_hash = str(self.generate_hash())
        return current_hash
    
    def update_previous_hash(self):
        previous_hash = str(self.previous_hash)
        return previous_hash

    def update_space(self):
        space = ""
        return space
