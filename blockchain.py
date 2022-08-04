from functools import reduce
import json

from hash_functions import hash_block
from block import Block
from transaction import Transaction
from verification import Verification


#constant, reward that user will receive when they mine a block
MINING_REWARD = 10

blockchain = []
open_transactions = []
owner = 'Caolan'

def load_data():
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt', mode='r') as file:
            # file_content = pickle.loads(file.read())
            file_content = file.readlines()
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']

            #using range selection to get the entire line except for \n
            #takes string in json format and gives back an object
            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                #using new block class to create a Block object, will return a list of objects instead of dictionaries 
                updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions

   #adding genesis block and initializing our blockchain if an IOError or IndexError is thrown
    except (IOError, IndexError):
        GENESIS_BLOCK = Block(0, '', [], 10, 0)
        blockchain = [GENESIS_BLOCK]
        open_transactions = []
    finally:
        print('Cleanup')

load_data()


def save_data():
    try:
        with open('blockchain.txt', mode='w') as file:
            #c
            saved_chain = [block.__dict__ for block in 
                [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) 
                for block_el in blockchain]]
            file.write(json.dumps(saved_chain))
            file.write('\n')
            saved_tx = [tx.__dict__ for tx in open_transactions]
            file.write(json.dumps(saved_tx))

    except IOError:
        print('File save has been unsuccessful')

        #attempted using pickle library to preserve dictionary output instead of string with json
        # save_data = {
        #     'chain': blockchain,
        #     'ot': open_transactions
        # }
        # file.write(pickle.dumps(save_data))
     

def proof_of_work():
    """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    verifier = Verification()
    #tries different proof of work numbers until it finds a valid one
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


    #return sender_balance >= transaction['amount'] because it will return a boolean anyway


def get_balance(participant):
    #nested list comprehension to go through every block in the blockchain
    #get amount for a given transcation, for all transactions in the block
    #  if the sender is the same as the participant. Since the transactions are part of the block
    # and we have a list of blocks, we wrap it with another list comprehension where we go through every block
    tx_sender = [[tx.amount for tx in block.transactions
                    if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_sender, 0)
    tx_recipient = [[tx.amount for tx in block.transactions
                    if tx.recipient == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_recipient, 0)
    #tuple to subtract the amount sent from the amount received, returning our balance. 
    return amount_received - amount_sent


def get_last_value():
     #-1 accesses the last value of the list
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

#blockchain is initialized here with value of 1 
def add_value(recipient, sender=owner, amount=1.0):
    """Append new value AND the last blockchain value to the blockchain
    
    Arguments:
        :Sender: sender of coins
        :recipient: recipient of the coins
        :Amount: amount of coins sent, default is 1
    """
    #dictionary with key value pairs 
    #creating an ordered dictionary which takes a list of tuples
    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    #foward get_balance func without () as don't want to execute the function, just forward it 
    #which passes a reference to the function onto verify_transaction, so this function can then call get balance
    #for us
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        save_data()
        return True
    return False
    

#function to mine a new block and append it to the blockchain
def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    #adding proof of work function
    proof = proof_of_work()
    #when the block is mined, the user will be rewarded by receiving coins
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    #using range selection to copy the open_transactions list
    #so that we can use this locally
    #if the mine block ever fails, then our global open_transactions won't be affected
    copy_transactions = open_transactions[:]
    copy_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copy_transactions, proof)
    # block = {
    #     'previous_hash': hashed_block,
    #     'index': len(blockchain),
    #     'transactions': copy_transactions,
    #     'proof': proof
    # }
    blockchain.append(block)
    return True


    
    


