class Token:
    def __init__(self, name, symbol, total_supply):
        self.name = name
        self.symbol = symbol
        self.total_supply = total_supply
        self.balances = {}

    def transfer(self, sender, recipient, amount):
        if sender not in self.balances or self.balances[sender] < amount:
            return False
        self.balances[sender] -= amount
        self.balances[recipient] = self.balances.get(recipient, 0) + amount
        return True

    def mint(self, address, amount):
        self.balances[address] = self.balances.get(address, 0) + amount
        self.total_supply += amount

    def burn(self, address, amount):
        if address not in self.balances or self.balances[address] < amount:
            return False
        self.balances[address] -= amount
        self.total_supply -= amount
        return True