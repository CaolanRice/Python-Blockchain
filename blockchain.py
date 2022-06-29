from audioop import add
from webbrowser import get

# initialize blockchain list
blockchain = []

def get_last_value():
     #-1 accesses the last value of the list
    return blockchain [-1]

#blockchain is initialized here with value of 2 
def add_value(transaction_amount, last_transaction=[2]):
    """Append new value AND the last blockchain value to the blockchain
    
    Arguments:
        :last_transaction: Last blockchain transaction (default is [1])
        :transaction_amount: The amount that will be added to the blockchain
    """
    blockchain.append([last_transaction, transaction_amount])

def get_transaction_value():
    """Returns user input as a float to be added to the chain"""
    user_input = float (input('Enter your transaction amount: '))
    return user_input

def get_user_choice():
    user_input = input('Your choice: ')
    return user_input 
    

def print_blockchain():
    # loop to print the blockchain values
    for block in blockchain:
        print ('Printing Block')
        print (block)

tx_amount = get_transaction_value()
add_value(tx_amount)

while True:
    print('Select an option')
    print('1. Make a new transaction')
    print('2. View current blockchain')
    print('3. Exit program')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_value(tx_amount, get_last_value())
    elif user_choice == '2':
         print_blockchain()
    elif user_choice == '3':
        break
    else: 
        print('Invalid input, please select a choice from the list')
    print('Choice registered!')


print ('Program exited!')
    


