from audioop import add
from webbrowser import get

# initialize blockchain list
blockchain = []

def get_last_value():
     #-1 accesses the last value of the list
    return blockchain [-1]


def add_value(transaction_amount, last_transaction=[1]):
    """Append new value AND the last blockchain value to the blockchain
    
    Arguments:
        :last_transaction: Last blockchain transaction (default is [1])
        :transaction_amount: The amount that will be added to the blockchain
    """
    blockchain.append([last_transaction, transaction_amount])

def get_user_input():
    """Returns user input as a float to be added to the chain"""
    return float (input("Enter your transaction amount: "))

tx_amount = get_user_input()
add_value(tx_amount)

# keyword arguments
tx_amount = get_user_input()
add_value(last_transaction=get_last_value(), transaction_amount=tx_amount)
 
tx_amount = get_user_input()
add_value(last_transaction=get_last_value(), transaction_amount=tx_amount)
# add_value(2.4, get_last_value())

print(blockchain)