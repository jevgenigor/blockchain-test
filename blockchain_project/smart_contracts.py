class SmartContractVM:
    def __init__(self):
        self.storage = {}

    def execute(self, code, transaction, blockchain):
        context = {
            "sender": transaction.sender,
            "recipient": transaction.recipient,
            "amount": transaction.amount,
            "data": transaction.data,
            "blockchain": blockchain,
            "storage": self.storage
        }
        exec(code, context)
        self.storage = context['storage']
        return context.get('output', None)

class SmartContract:
    def __init__(self, code):
        self.code = code
        self.vm = SmartContractVM()

    def execute(self, transaction, blockchain):
        return self.vm.execute(self.code, transaction, blockchain)