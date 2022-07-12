#adding a genesis block, the very first block that is a part of each chain
genesis_block = {
        'previous_hash': '',
        'index': 0,
        'transactions' : []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Caolan'
participants = {'Caolan'}


def hash_block(block):
    '-'.join([str(block[key]) for key in block])


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
    transaction = {
    'sender': sender,
    'receiver': receiver, 
    'amount': amount
    }
    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(receiver)
    

#function to mine a new block and append it to the blockchain
def mine_block():
    last_block = blockchain[-1]
    #list compression - join takes the list as an argument and joins it with the - character
    #can only join a list of strings, so we wrap the last_block[key] value with the string function
    hashed_block = hash_block(last_block)
    # for key in last_block:
    #     value = last_block[key]
    #     hashed_block = hashed_block + str(value)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }
    blockchain.append(block)

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
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True

    
awaiting_input = True

while awaiting_input:
    print('Select an option')
    print('1: Make a new transaction')
    print('2: Mine a new block')
    print('3: View current blockchain')
    print('4: Output Participants')
    print('m. Modify blockchain')
    print('q. Exit program')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        #tuple unpacking - assings individual elements of the tuple to a variable*****************************************
        recipient, amount = tx_data
        #adding the transaction amount to the blockchain
        add_value(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
         print_blockchain()
    elif user_choice == '4':
        print(participants)
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
else:
    print('User left') 
    
print ('Program exited!')
    


