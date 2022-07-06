# initialize blockchain list
blockchain = []
open_transactions = []
owner = 'Caolan'

def get_last_value():
     #-1 accesses the last value of the list
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

#blockchain is initialized here with value of 1 
def add_value(sender, receiver, amount=1.0):
    """Append new value AND the last blockchain value to the blockchain
    
    Arguments:
        :sender: sender of coins
        :receiver: recipient of the coins
        :amount: amount of coins sent, default 1
    """
    transaction = {
    'sender': sender,
    'receiver': receiver, 
    'amount': amount
    }
    open_transactions.append(transaction)
    

def mine_block():
    pass

def get_transaction_value():
    """Returns user input as a float to be added to the chain"""
    tx_receiver = input('Enter the receiver of the transaction')
    tx_amount = float(input('Enter your transaction amount: '))
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
    print('2. View current blockchain')
    print('m. Alter blockchain')
    print('q. Exit program')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_value(tx_amount, get_last_value())
    elif user_choice == '2':
         print_blockchain()
    elif user_choice == 'm':
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
    


