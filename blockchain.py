#adding a genesis block, the very first block that is a part of each chain
genesis_block = {
        'previous hash': '',
        'index': 0,
        'transactions' : []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Caolan'

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
    

def mine_block():
    last_block = blockchain[-1]
    hashed_block = ''
    for key in last_block:
        value = last_block[key]
        hashed_block = hashed_block + str(value)

    block = {
        'previous hash': hashed_block,
        'index': len(blockchain),
        'transactions' : open_transactions
    }
    blockchain.append(block)

def get_transaction_value():
    """Returns user input as a float to be added to the chain"""
    tx_receiver = input('Enter the receiver of the transaction: ')
    tx_amount = float(input('Enter your transaction amount: '))
    #tuple
    return (tx_receiver, tx_amount)

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

# get explanation for block_index variable
#function to verify that the blockchain doesn't get modified - Double check this!
def verify_blockchain():
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else: 
            is_valid = False
    return is_valid


awaiting_input = True

while awaiting_input:
    print('Select an option')
    print('1. Make a new transaction')
    print('2. Mine a new block')
    print('3. View current blockchain')
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
    elif user_choice == 'm':
        #validating the blockchain, making sure the values of previous blocks have not been modified
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        awaiting_input = False
    else: 
        print('Invalid input, please select a choice from the list')
    if not verify_blockchain():
        print_blockchain()
        print('Invalid blockchain!')
        break
    
print ('Program exited!')
    


