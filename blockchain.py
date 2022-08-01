from functools import reduce
import json

from hash_functions import hash_string_256, hash_block
from block import Block
from transaction import Transaction


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
                converted_tx = [Transaction(tx['sender'], tx['receiver'], tx['amount']) for tx in block['transactions']]
                #using new block class to create a Block object, will return a list of objects instead of dictionaries 
                updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(tx['sender'], tx['receiver'], tx['amount'])
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
     

#function that checks whether proof is valid, proof must match guess_hash
#incrementing proof leads to an entirely new hash 
def valid_proof(transactions, last_hash, proof):
    #any cha
    guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    #checking if guest_hash begins with two 0's
    return guess_hash[0:2] == '00'

def proof_of_work():
    """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    #tries different proof of work numbers until it finds a valid one
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof

def verify_transaction(transaction):
    sender_balance = get_balance(transaction.sender)
    if sender_balance >= transaction.amount:
        return True
    else:
        return False
    #return sender_balance >= transaction['amount'] because it will return a boolean anyway


def get_balance(participant):
    #nested list comprehension to go through every block in the blockchain
    #get amount for a given transcation, for all transactions in the block
    #  if the sender is the same as the participant. Since the transactions are part of the block
    # and we have a list of blocks, we wrap it with another list comprehension where we go through every block
    tx_sender = [[tx.amount for tx in block.transactions
                    if tx.amount == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_sender, 0)
    tx_receiver = [[tx.amount for tx in block.transactions
                    if tx.receiver == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_receiver, 0)
    #tuple to subtract the amount sent from the amount received, returning our balance. 
    return amount_received - amount_sent


def get_last_value():
     #-1 accesses the last value of the list
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

#blockchain is initialized here with value of 1 
def add_value(receiver, sender=owner, amount=1.0):
    """Append new value AND the last blockchain value to the blockchain
    
    Arguments:
        :Sender: sender of coins
        :Receiver: recipient of the coins
        :Amount: amount of coins sent, default is 1
    """
    #dictionary with key value pairs 
    #creating an ordered dictionary which takes a list of tuples
    transaction = Transaction(sender, receiver, amount)
    if verify_transaction(transaction):
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

def get_transaction_value():
    """Returns user input as a float to be added to the chain"""
    tx_receiver = input('Enter the receiver of the transaction: ')
    tx_amount = float(input('Enter your transaction amount: '))
    #tuple
    return tx_receiver, tx_amount

def get_user_choice():
    user_input = input('Your choice: ')
    return user_input
    

def print_blockchain():
    # loop to print the blockchain values
    for block in blockchain:
        print ('Printing Block')
        print (block)
    else:
        print('-' * 20)

#compare the stored hash in a given block with the recalculated hash of the previous block
def verify_blockchain():
    #loop through the blocks in the blockchain and compare every block, wrapping 
    #the list with enumerate function to get back a tuple, giving us the index of the element
    #and the element itself. We can then use unpacking (index, value) to get these arguments
    #both of the values are retried.
    for (index, block) in enumerate(blockchain):
    # If index is 0 then we continue, we don't need to validate the genesis block as it's the first block.  
        if index == 0:
            continue
    #Every block has a previous hash key, so in all other cases, we compare the value stored for this key
    #with our last block  which we get from index-1. We must hash this block and then pass the previous block
    #as an argument. This is dynamically recalculating the hash of the last block and comparing it with the
    #previously stored hash. If the blockchain has been manipulated, it will yield a different result
    #than the hash of the previous block.
        # if block['previous_hash'] != hash_block(blockchain[index - 1]):
        #previous hash as shown above is an attribute of the block object, 
        # so must be accessed using block.previous hash as shown below
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print ('Proof of work is invalid')
            return False
    return True


def verify_all_transactions():
    #using list comprehension and all function to return all TRUE (valid) transactions
    return all([verify_transaction(tx) for tx in open_transactions]) 
    # is_valid = True
    # for tx in open_transactions:
    #     if verify_all_transactions(tx):
    #         is_valid = True
    #     else:
    #         is_valid = False
    # return is_valid
    
awaiting_input = True

while awaiting_input:
    print('Select an option')
    print('1: Make a new transaction')
    print('2: Mine a new block')
    print('3: View current blockchain')
    print('4: Output participants')
    print('5: Check validity of transactions')
    print('m. Modify blockchain')
    print('q. Exit program')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        #tuple unpacking - assigning individual elements of the tuple to a variable*
        recipient, amount = tx_data
        #adding the transaction amount to the blockchain
        if add_value(recipient, amount=amount):
            print('Added transaction')
        else:
            print('Transaction failed')
        print(open_transactions)
    elif user_choice == '2':
        #when user mines a new block, reset open transactions to an empty list 
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '3':
         print_blockchain()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_all_transactions():
            print('All transactions verified')
        else:
            print('Some transactions are invalid')
    elif user_choice == 'm':
        #validating the blockchain, making sure the values of previous blocks have not been modified
        if len(blockchain) >= 1:
            #adding dummy hacked values to test the validation 
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions' : [{'sender': 'Anna', 'receiver': 'Caolan', 'amount': 12}]
            }
    elif user_choice == 'q':
        awaiting_input = False
    else: 
        print('Invalid input, please select a choice from the list')
    if not verify_blockchain():
        print_blockchain()
        print('Invalid blockchain!')
        break
    print('Balance of {}: {:6.2f}'.format('Caolan', get_balance('Caolan')))
else:
    print('User left') 
    
print ('Program exited!')
    


