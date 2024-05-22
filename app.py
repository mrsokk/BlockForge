from flask import Flask, request, jsonify
from blockforge import Blockchain, Block, Transaction
import time

app = Flask(__name__)

# Initialize blockchain
blockchain = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    latest_block = blockchain.get_latest_block()
    new_block = Block(len(blockchain.chain), latest_block.hash, time.time(), [])
    blockchain.add_block(new_block)
    response = {
        'message': 'New block mined',
        'index': new_block.index,
        'hash': new_block.hash,
        'previous_hash': new_block.previous_hash,
        'nonce': new_block.nonce,
        'timestamp': new_block.timestamp
    }
    return jsonify(response), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    values = request.get_json()
    required = ['sender', 'receiver', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    transaction = Transaction(values['sender'], values['receiver'], values['amount'])
    latest_block = blockchain.get_latest_block()
    new_block = Block(len(blockchain.chain), latest_block.hash, time.time(), [transaction])
    blockchain.add_block(new_block)
    response = {'message': 'Transaction will be added to the next block'}
    return jsonify(response), 201

@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        block_data = {
            'index': block.index,
            'hash': block.hash,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce,
            'timestamp': block.timestamp,
            'transactions': [str(tx) for tx in block.transactions]
        }
        chain_data.append(block_data)
    response = {
        'chain': chain_data,
        'length': len(blockchain.chain)  # added missing closing quote
    }
    return jsonify(response), 200
