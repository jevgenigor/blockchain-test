import socket
import threading
import json
import random
from blockchain_core import Transaction

class P2PNetwork:
    def __init__(self, host, port, blockchain):
        self.host = host
        self.port = port
        self.blockchain = blockchain
        self.peers = set()
        self.known_nodes = set()  # List of known node addresses

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"Node listening on {self.host}:{self.port}")
        
        # Start peer discovery
        discovery_thread = threading.Thread(target=self.discover_peers)
        discovery_thread.start()

        while True:
            client, address = server.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def handle_client(self, client_socket):
        request = client_socket.recv(1024).decode()
        if request == "get_chain":
            response = json.dumps(self.blockchain.chain, default=lambda o: o.__dict__)
            client_socket.send(response.encode())
        elif request.startswith("new_transaction:"):
            transaction_data = json.loads(request.split(":", 1)[1])
            transaction = Transaction(**transaction_data)
            self.blockchain.add_transaction(transaction)
        elif request == "get_peers":
            response = json.dumps(list(self.peers))
            client_socket.send(response.encode())
        client_socket.close()

    def broadcast_transaction(self, transaction):
        for peer in self.peers:
            try:
                host, port = peer.split(':')
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, int(port)))
                    s.send(f"new_transaction:{json.dumps(transaction.to_dict())}".encode())
            except Exception as e:
                print(f"Failed to send transaction to {peer}: {e}")

    def connect_to_peer(self, host, port):
        peer = f"{host}:{port}"
        if peer not in self.peers:
            self.peers.add(peer)
            self.blockchain.add_node(peer)

    def discover_peers(self):
        while True:
            if self.known_nodes:
                node = random.choice(list(self.known_nodes))
                try:
                    host, port = node.split(':')
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((host, int(port)))
                        s.send("get_peers".encode())
                        response = s.recv(1024).decode()
                        new_peers = json.loads(response)
                        for peer in new_peers:
                            self.connect_to_peer(*peer.split(':'))
                except Exception as e:
                    print(f"Failed to discover peers from {node}: {e}")
            threading.Timer(60, self.discover_peers).start()  # Run discovery every 60 seconds