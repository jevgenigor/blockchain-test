from flask import Flask, render_template, request, jsonify
from blockchain_core import Blockchain, Transaction
from consensus import ProofOfStake
from storage import BlockchainStorage
from network import P2PNetwork
from smart_contracts import SmartContract
from custom_token import Token
from blockchain_core import Block
import time

app = Flask(__name__)

blockchain = Blockchain()
pos = ProofOfStake()
storage = BlockchainStorage("blockchain_data.json")
network = P2PNetwork("localhost", 5000, blockchain)
token = Token("MyCoin", "MYC", 1000000)

@app.route('/')
def index():
    return render_template('index.html', blockchain=blockchain)

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount', 'fee']
    if not all(k in values for k in required):
        return 'Missing values', 400

    transaction = Transaction(values['sender'], values['recipient'], values['amount'], values['fee'])
    blockchain.add_transaction(transaction)
    network.broadcast_transaction(transaction)

    return jsonify({"message": "Transaction added"}), 201

@app.route('/mine', methods=['GET'])
def mine():
    validator = pos.get_validator()
    last_block = blockchain.get_latest_block()
    new_block = Block(last_block.index + 1, blockchain.pending_transactions, int(time.time()), last_block.hash, validator)
    blockchain.add_block(new_block)
    blockchain.pending_transactions = []
    storage.save_blockchain(blockchain)
    return jsonify({"message": "New block mined"}), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': [vars(block) for block in blockchain.chain],
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)