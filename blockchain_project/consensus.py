import random

class ProofOfStake:
    def __init__(self):
        self.stakers = {}
        self.total_stake = 0

    def add_staker(self, address, stake):
        if address in self.stakers:
            self.total_stake -= self.stakers[address]
        self.stakers[address] = stake
        self.total_stake += stake

    def remove_staker(self, address):
        if address in self.stakers:
            self.total_stake -= self.stakers[address]
            del self.stakers[address]

    def get_validator(self):
        if not self.stakers:
            return None
        target = random.uniform(0, self.total_stake)
        current_stake = 0
        for address, stake in self.stakers.items():
            current_stake += stake
            if current_stake >= target:
                return address
        return None

    def slash(self, address, percentage):
        if address in self.stakers:
            slash_amount = self.stakers[address] * percentage
            self.stakers[address] -= slash_amount
            self.total_stake -= slash_amount
            return slash_amount
        return 0