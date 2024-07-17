from blockchain_core import Transaction
import time

class Proposal:
    def __init__(self, proposer, description, options):
        self.proposer = proposer
        self.description = description
        self.options = options
        self.votes = {option: 0 for option in options}
        self.start_time = time.time()
        self.end_time = self.start_time + 7 * 24 * 60 * 60  # 1 week voting period

    def vote(self, voter, option):
        if option not in self.options:
            raise ValueError("Invalid voting option")
        if time.time() > self.end_time:
            raise ValueError("Voting period has ended")
        self.votes[option] += 1

    def get_result(self):
        if time.time() < self.end_time:
            return None
        return max(self.votes, key=self.votes.get)

class DAO:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.proposals = []
        self.members = set()

    def add_member(self, address):
        self.members.add(address)

    def remove_member(self, address):
        self.members.remove(address)

    def create_proposal(self, proposer, description, options):
        if proposer not in self.members:
            raise ValueError("Only members can create proposals")
        proposal = Proposal(proposer, description, options)
        self.proposals.append(proposal)
        return len(self.proposals) - 1  # Return proposal ID

    def vote(self, voter, proposal_id, option):
        if voter not in self.members:
            raise ValueError("Only members can vote")
        if proposal_id < 0 or proposal_id >= len(self.proposals):
            raise ValueError("Invalid proposal ID")
        self.proposals[proposal_id].vote(voter, option)

    def execute_proposal(self, proposal_id):
        if proposal_id < 0 or proposal_id >= len(self.proposals):
            raise ValueError("Invalid proposal ID")
        proposal = self.proposals[proposal_id]
        result = proposal.get_result()
        if result is None:
            raise ValueError("Voting period has not ended yet")
        
        # Execute the proposal based on the result
        # This is a placeholder and should be implemented based on your specific needs
        print(f"Executing proposal {proposal_id}: {result}")

    def get_proposal_status(self, proposal_id):
        if proposal_id < 0 or proposal_id >= len(self.proposals):
            raise ValueError("Invalid proposal ID")
        proposal = self.proposals[proposal_id]
        return {
            "description": proposal.description,
            "options": proposal.options,
            "votes": proposal.votes,
            "end_time": proposal.end_time,
            "result": proposal.get_result()
        }
