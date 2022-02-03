from block import Block
import json

class Blockchain:
    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = []
        self.genesis_block()

    def genesis_block(self):
        transactions = []
        genesis_block = Block(transactions, "0")
        genesis_block.generate_hash()
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        previous_hash = (self.chain[len(self.chain) - 1]).hash
        new_block = Block(transactions, previous_hash)
        new_block.generate_hash()
        # proof = proof_of_work(block) # Can add later for additional authenticity
        self.chain.append(new_block)

    def print_blocks(self):
        for i in range(len(self.chain)):
            current_block = self.chain[i]
            print("Block {} {}".format(i, current_block))
            current_block.print_contents()
    
    def update_blocks(self):
        index = len(self.chain) - 1
        current_block = self.chain[index]
        new_block = "Block {} {}".format(index, current_block)
        with open("blockchain.json", 'r+') as file:
                file_data = json.load(file)
                contents = {
                    "timestamp": current_block.update_timestamp(),
                    "transactions": current_block.update_transactions(),
                    "current hash": current_block.update_current_hash(),
                    "previous hash": current_block.update_previous_hash()
                }
                block = {new_block: contents}
                                
                file_data["blockchain"].append(block)
                file.seek(0)
                string = json.dump(file_data, file, indent = 4)


    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if (current.hash != current.generate_hash()):
                print("Current hash does not equal generated hash")
                return False
            if (current.previous_hash != previous.generate_hash()):
                print("Previous block's hash was changed")
                return False
        return True

    def proof_of_work(self, block, difficulty=2):
        proof = block.generate_hash()
        while proof[:2] != "0" * difficulty:
            block.nonce += 1
            proof = block.generate_hash()
        block.nonce = 0
        return proof