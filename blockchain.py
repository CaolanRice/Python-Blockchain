# initialize blockchain list
blockchain = []


def get_last_value():
     #-1 accesses the last value of the list
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

#blockchain is initialized here with value of 1 
def add_value(transaction_amount, last_transaction):
    """Append new value AND the last blockchain value to the blockchain
    
    Arguments:
        :last_transaction: Last blockchain transaction (default is [1])
        :transaction_amount: The amount that will be added to the blockchain
    """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])

def get_transaction_value():
    """Returns user input as a float to be added to the chain"""
    user_input = float(input('Enter your transaction amount: '))
    return user_input

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
    


