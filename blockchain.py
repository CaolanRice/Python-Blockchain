from functools import reduce
import json

from utility.hash_functions import hash_block
from block import Block
from transaction import Transaction
from utility.verification import Verification
from wallet import Wallet

#constant, reward that user will receive when they mine a block
MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        #named chain to differentiate from the Blockchain object
        #still initializing the empty blockchain list
        genesis_block = Block(0, '', [], 10, 0)
        #first element of the chain will be the genesis block, this will be overwritten if we load_data
        #encapsulating the chain and open_transactions 
        self.chain = [genesis_block]
        self.__open_transactions = []
        self.hosting_node = hosting_node_id
        self.__peer_node = set()
        self.load_data()

    #controlling access for reading and writing.
    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    # def get_chain(self):
    #     #returning a copy, so this element gets edited, it won't edit the original chain list
    #     return self.__chain[:]


    #adds a peer node to the peer node set
    def add_peer_node(self, node):
        """Node URL should be added as an argument"""
        self.__peer_nodes.add(node)
        self.save_data()
    
    #removes a node from the peer nodes set
    def remove_peer_node(self, node):
        self.__peer_nodes.discard(node)
        self.save_data()
    
    #returns list of connected peer nodes
    def get_peer_nodes(self):
        return list(self.__peer_nodes)

    
    def get_open_transactions(self):
        return self.__open_transactions

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as file:
                file_content = file.readlines()
                #using range selection to get the entire line except for \n
                #takes string in json format and gives back an object
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction
                    (tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    #using new block class to create a Block object, will return a list of objects instead of dictionaries 
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                #storing the updated_blockchain back into the chain attribute     
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                    #storing the updated transactions in the open_transactions attribute 
                self.__open_transactions = updated_transactions
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)

   #adding genesis block and initializing our blockchain if an IOError or IndexError is thrown
        except (IOError, IndexError):
            # genesis_block = Block(0, '', [], 10, 0)
            # blockchain = [genesis_block]
            # open_transactions = []
            print('Exception Handled')
        finally:
            print('Hi')


    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as file:
                saved_chain = [block.__dict__ for block in 
                    [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) 
                    for block_el in self.__chain]]
                file.write(json.dumps(saved_chain))
                file.write('\n')
                saved_tx = [tx.__dict__ for tx in self.__open_transactions]
                file.write(json.dumps(saved_tx))
                file.write('\n')
                file.write(json.dumps(list(self.__peer_node)))

        except IOError:
            print('File save has been unsuccessful')

    def proof_of_work(self):
        """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        #tries different proof of work numbers until it finds a valid one
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof


    #return sender_balance >= transaction['amount'] because it will return a boolean anyway


    def get_balance(self):
        #nested list comprehension to go through every block in the blockchain
        #get amount for a given transcation, for all transactions in the block
        #  if the sender is the same as the participant. Since the transactions are part of the block
        # and we have a list of blocks, we wrap it with another list comprehension where we go through every block
        if self.hosting_node == None:
            return None
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions
                        if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_sender, 0)
        tx_recipient = [[tx.amount for tx in block.transactions
                        if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_recipient, 0)
        #tuple to subtract the amount sent from the amount received, returning our balance. 
        return amount_received - amount_sent


    def get_last_value(self):
        #-1 accesses the last value of the list
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

#blockchain is initialized here with value of 1 
    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """Append new value AND the last blockchain value to the blockchain
        
        Arguments:
            :Sender: sender of coins
            :recipient: recipient of the coins
            :Amount: amount of coins sent, default is 1
        """
        #dictionary with key value pairs 
        #creating an ordered dictionary which takes a list of tuples
        transaction = Transaction(sender, recipient, signature, amount)
        #foward get_balance func without () as don't want to execute the function, just forward it 
        #which passes a reference to the function onto verify_transaction, so this function can then call get balance
        #for us
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False
    

#function to mine a new block and append it to the blockchain
    def mine_block(self):
        if self.hosting_node == None:
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        #adding proof of work function
        proof = self.proof_of_work()
        #when the block is mined, the user will be rewarded by receiving coins
        reward_transaction = Transaction('MINING', self.hosting_node, '', MINING_REWARD)
        #using range selection to copy the open_transactions list
        #so that we can use this locally
        #if the mine block ever fails, then our global open_transactions won't be affected
        copy_transactions = self.__open_transactions[:]
        for tx in copy_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copy_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copy_transactions, proof)
        # block = {
        #     'previous_hash': hashed_block,
        #     'index': len(blockchain),
        #     'transactions': copy_transactions,
        #     'proof': proof
        # }
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return block


    
    


