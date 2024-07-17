import hashlib
from ecdsa import SigningKey, SECP256k1
import base58
import base64
import os

class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.address = None

    def generate_new_wallet(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.address = self.generate_address()

    def generate_address(self):
        public_key_bytes = self.public_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes).digest()
        ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()
        return base58.b58encode_check(b'\x00' + ripemd160_bpk).decode('utf-8')

    def sign_transaction(self, transaction):
        transaction_hash = transaction.calculate_hash()
        signature = self.private_key.sign(transaction_hash.encode())
        return base64.b64encode(signature).decode()

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.private_key.to_string())

    def load_from_file(self, filename):
        with open(filename, 'rb') as f:
            private_key_string = f.read()
        self.private_key = SigningKey.from_string(private_key_string, curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.address = self.generate_address()

class WalletManager:
    def __init__(self, wallet_dir):
        self.wallet_dir = wallet_dir
        self.wallets = {}
        os.makedirs(wallet_dir, exist_ok=True)

    def create_new_wallet(self, name):
        wallet = Wallet()
        wallet.generate_new_wallet()
        wallet.save_to_file(os.path.join(self.wallet_dir, f"{name}.wallet"))
        self.wallets[name] = wallet
        return wallet

    def load_wallet(self, name):
        if name not in self.wallets:
            wallet = Wallet()
            wallet.load_from_file(os.path.join(self.wallet_dir, f"{name}.wallet"))
            self.wallets[name] = wallet
        return self.wallets[name]

    def get_balance(self, name, blockchain):
        wallet = self.load_wallet(name)
        balance = 0
        for block in blockchain.chain:
            for tx in block.transactions:
                if tx.recipient == wallet.address:
                    balance += tx.amount
                if tx.sender == wallet.address:
                    balance -= tx.amount
        return balance