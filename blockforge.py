import hashlib
import time

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __repr__(self):
        return f"Transaction(Sender: {self.sender}, Receiver: {self.receiver}, Amount: {self.amount})"

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        transactions_str = ''.join(str(tx) for tx in self.transactions)
        value = f"{self.index}{self.previous_hash}{self.timestamp}{transactions_str}{self.nonce}"
        return hashlib.sha256(value.encode()).hexdigest()

    def __repr__(self):
        return f"Block(Index: {self.index}, Hash: {self.hash}, Nonce: {self.nonce}, Transactions: {self.transactions})"

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2  # Adjust difficulty as needed

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        self.proof_of_work(new_block)
        self.chain.append(new_block)

    def proof_of_work(self, block):
        while block.hash[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

if __name__ == "__main__":
    blockforge = Blockchain()

    tx1 = Transaction("Alice", "Bob", 10)
    tx2 = Transaction("Bob", "Charlie", 5)
    block1 = Block(1, blockforge.get_latest_block().hash, time.time(), [tx1, tx2])
    blockforge.add_block(block1)

    tx3 = Transaction("Charlie", "Dave", 2)
    block2 = Block(2, blockforge.get_latest_block().hash, time.time(), [tx3])
    blockforge.add_block(block2)

    for block in blockforge.chain:
        print(block)

    print("Is blockchain valid?", blockforge.is_chain_valid())
