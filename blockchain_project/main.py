import threading
from blockchain_core import Blockchain
from consensus import ProofOfStake
from storage import BlockchainStorage
from network import P2PNetwork
from smart_contracts import SmartContract
from custom_token import Token
from web_interface import app

def main():
    blockchain = Blockchain()
    pos = ProofOfStake()
    storage = BlockchainStorage("blockchain_data.json")
    network = P2PNetwork("localhost", 5000, blockchain)
    token = Token("MyCoin", "MYC", 1000000)

    # Load blockchain from storage if exists
    loaded_blockchain = storage.load_blockchain()
    if loaded_blockchain:
        blockchain = loaded_blockchain

    # Start P2P network
    network_thread = threading.Thread(target=network.start)
    network_thread.start()

    # Run web interface
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()