import random

class ProofOfStake:
    def __init__(self):
        self.stakers = {}

    def add_staker(self, address, stake):
        self.stakers[address] = stake

    def remove_staker(self, address):
        if address in self.stakers:
            del self.stakers[address]

    def get_validator(self):
        total_stake = sum(self.stakers.values())
        target = random.uniform(0, total_stake)
        current_stake = 0
        for address, stake in self.stakers.items():
            current_stake += stake
            if current_stake >= target:
                return address
        return None