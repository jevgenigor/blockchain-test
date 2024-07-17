import random
from blockchain_core import Blockchain, Transaction
from consensus import ProofOfStake
from network import P2PNetwork
import threading
import time

class Testnet:
    def __init__(self, num_nodes):
        self.nodes = []
        for i in range(num_nodes):
            blockchain = Blockchain()
            pos = ProofOfStake()
            network = P2PNetwork(f"127.0.0.1", 5000 + i, blockchain)
            self.nodes.append((blockchain, pos, network))

    def start(self):
        for _, _, network in self.nodes:
            thread = threading.Thread(target=network.start)
            thread.start()

    def connect_nodes(self):
        for i, (_, _, network1) in enumerate(self.nodes):
            for j, (_, _, network2) in enumerate(self.nodes):
                if i != j:
                    network1.connect_to_peer(network2.host, network2.port)

    def simulate_transactions(self, num_transactions):
        for _ in range(num_transactions):
            sender = f"wallet_{random.randint(0, len(self.nodes) - 1)}"
            recipient = f"wallet_{random.randint(0, len(self.nodes) - 1)}"
            amount = random.uniform(1, 100)
            fee = random.uniform(0.1, 1)
            transaction = Transaction(sender, recipient, amount, fee)
            node = random.choice(self.nodes)
            node[0].add_transaction(transaction)
            node[2].broadcast_transaction(transaction)

    def mine_blocks(self, num_blocks):
        for _ in range(num_blocks):
            node = random.choice(self.nodes)
            blockchain, pos, _ = node
            validator = pos.get_validator()
            blockchain.mine_block(validator)

    def run_simulation(self, duration):
        start_time = time.time()
        while time.time() - start_time < duration:
            self.simulate_transactions(10)
            self.mine_blocks(1)
            time.sleep(1)

def run_testnet():
    testnet = Testnet(5)
    testnet.start()
    testnet.connect_nodes()
    testnet.run_simulation(300)  # Run for 5 minutes

if __name__ == "__main__":
    run_testnet()