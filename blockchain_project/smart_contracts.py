class SmartContractVM:
    def __init__(self):
        self.storage = {}
        self.gas_limit = 1000000  # Example gas limit

    def execute(self, code, transaction, blockchain):
        context = {
            "sender": transaction.sender,
            "recipient": transaction.recipient,
            "amount": transaction.amount,
            "data": transaction.data,
            "blockchain": blockchain,
            "storage": self.storage,
            "gas_used": 0
        }

        def charge_gas(amount):
            context['gas_used'] += amount
            if context['gas_used'] > self.gas_limit:
                raise Exception("Out of gas")

        # Wrap each operation with gas charging
        wrapped_code = f"""
def charge_gas(amount):
    globals()['charge_gas'](amount)

{code}

# Charge gas for each line of code
charge_gas(1)
"""
        try:
            exec(wrapped_code, context)
        except Exception as e:
            print(f"Contract execution failed: {e}")
            return None

        self.storage = context['storage']
        return context.get('output', None), context['gas_used']

class SmartContract:
    def __init__(self, code):
        self.code = code
        self.vm = SmartContractVM()

    def execute(self, transaction, blockchain):
        return self.vm.execute(self.code, transaction, blockchain)