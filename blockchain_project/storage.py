import json
import os
from blockchain_core import Blockchain, Transaction, Block

class BlockchainStorage:
    def __init__(self, filename):
        self.filename = filename

    def save_blockchain(self, blockchain):
        data = {
            "chain": [self._block_to_dict(block) for block in blockchain.chain],
            "pending_transactions": [t.to_dict() for t in blockchain.pending_transactions],
            "nodes": list(blockchain.nodes)
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def load_blockchain(self):
        if not os.path.exists(self.filename):
            return None
        with open(self.filename, 'r') as f:
            data = json.load(f)
        blockchain = Blockchain()
        blockchain.chain = [self._dict_to_block(b) for b in data["chain"]]
        blockchain.pending_transactions = [Transaction(**t) for t in data["pending_transactions"]]
        blockchain.nodes = set(data["nodes"])
        return blockchain

    def _block_to_dict(self, block):
        return {
            "index": block.index,
            "transactions": [t.to_dict() for t in block.transactions],
            "timestamp": block.timestamp,
            "previous_hash": block.previous_hash,
            "validator": block.validator,
            "hash": block.hash
        }

    def _dict_to_block(self, data):
        block = Block(
            data["index"],
            [Transaction(**t) for t in data["transactions"]],
            data["timestamp"],
            data["previous_hash"],
            data["validator"]
        )
        block.hash = data["hash"]
        return block