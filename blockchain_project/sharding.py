import hashlib

class Shard:
    def __init__(self, shard_id):
        self.shard_id = shard_id
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

class ShardingManager:
    def __init__(self, num_shards):
        self.num_shards = num_shards
        self.shards = [Shard(i) for i in range(num_shards)]

    def get_shard_for_transaction(self, transaction):
        # Simple sharding based on the first character of the recipient address
        shard_id = int(hashlib.sha256(transaction.recipient.encode()).hexdigest(), 16) % self.num_shards
        return self.shards[shard_id]

    def add_transaction(self, transaction):
        shard = self.get_shard_for_transaction(transaction)
        shard.add_transaction(transaction)