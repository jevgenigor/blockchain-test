import hashlib
import time
import json
from ecdsa import SigningKey, SECP256k1, VerifyingKey
import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import random

class Transaction:
    def __init__(self, sender, recipient, amount, fee, data=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.fee = fee
        self.data = data
        self.signature = None
        self.timestamp = int(time.time())

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.fee,
            "data": self.data,
            "timestamp": self.timestamp
        }

    def calculate_hash(self):
        transaction_string = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    def sign_transaction(self, signing_key):
        transaction_hash = self.calculate_hash()
        self.signature = base64.b64encode(signing_key.sign(transaction_hash.encode())).decode()

    def is_valid(self, verifying_key):
        if not self.signature:
            return False
        transaction_hash = self.calculate_hash()
        try:
            return verifying_key.verify(base64.b64decode(self.signature), transaction_hash.encode())
        except:
            return False

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, validator):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.validator = validator
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "transactions": [t.to_dict() for t in self.transactions],
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "validator": self.validator
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.nodes = set()

    def create_genesis_block(self):
        return Block(0, [], int(time.time()), "0", "genesis")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, block):
        self.chain.append(block)

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def add_node(self, address):
        self.nodes.add(address)

    def replace_chain(self, new_chain):
        if len(new_chain) > len(self.chain) and self.is_chain_valid(new_chain):
            self.chain = new_chain

class RingSignature:
    @staticmethod
    def generate_key_pair():
        key = RSA.generate(2048)
        return key, key.publickey()

    @staticmethod
    def create_ring_signature(message, public_keys, signer_key, signer_index):
        n = len(public_keys)
        if signer_index < 0 or signer_index >= n:
            raise ValueError("Invalid signer index")

        message_bytes = message.encode('utf-8')

        v = [random.getrandbits(256) for _ in range(n)]
        x = random.getrandbits(256)

        ring = []
        for i in range(n):
            if i == signer_index:
                ring.append(x)
            else:
                ring.append(SHA256.new(str(v[i]).encode()).digest())

        h = SHA256.new(message_bytes)
        signature = pkcs1_15.new(signer_key).sign(h)

        return ring, signature

    @staticmethod
    def verify_ring_signature(message, public_keys, ring, signature):
        n = len(public_keys)
        if len(ring) != n:
            return False

        message_bytes = message.encode('utf-8')

        h = SHA256.new(message_bytes)
        try:
            pkcs1_15.new(public_keys[0]).verify(h, signature)
        except (ValueError, TypeError):
            return False

        ring_hash = SHA256.new()
        for i in range(n):
            ring_hash.update(str(ring[i]).encode())

        return ring_hash.digest() == signature

class PrivateTransaction(Transaction):
    def __init__(self, sender, recipient, amount, fee, data=None):
        super().__init__(sender, recipient, amount, fee, data)
        self.ring_signature = None

    def sign_with_ring(self, public_keys, signer_key, signer_index):
        message = self.calculate_hash()
        self.ring_signature = RingSignature.create_ring_signature(message, public_keys, signer_key, signer_index)

    def verify(self, public_keys):
        if not self.ring_signature:
            return False
        message = self.calculate_hash()
        return RingSignature.verify_ring_signature(message, public_keys, *self.ring_signature)