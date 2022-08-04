from uuid import uuid4
from blockchain import Blockchain
from verification import Verification

class Node:
    #constructor for blockchain. Attribute of the a Node, because every node will
    #have its own local copy of the blockchain
    def __init__(self):
        #generates unique ID which will then be passed onto the blockchain as node_id
        self.id = str(uuid4())
        self.blockchain = Blockchain(self.id)
        
    def get_transaction_value(self):
        """Returns user input as a float to be added to the chain"""
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Enter your transaction amount: '))
        #tuple
        return tx_recipient, tx_amount

    def get_user_choice(self):
        user_input = input('Your choice: ')
        return user_input
    

    def print_blockchain(self):
        # loop through chain of blocks from the Blockchain object
        for block in self.blockchain.chain:
            print ('Printing Block')
            print (block)
        else:
            print('-' * 20)

    def listen_for_input(self):
        awaiting_input = True

        while awaiting_input:
            print('Select an option')
            print('1: Make a new transaction')
            print('2: Mine a new block')
            print('3: View current blockchain')
            print('4: Check validity of transactions')
            print('q. Exit program')
            #self.get_user_choice() because it's now a method of this class
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                #tuple unpacking - assigning individual elements of the tuple to a variable*
                recipient, amount = tx_data
                #adding the transaction amount to the blockchain
                if self.blockchain.add_value(recipient, self.id, amount=amount):
                    print('Added transaction')
                else:
                    print('Transaction failed')
                print(self.blockchain.open_transactions)
            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockchain()
            elif user_choice == '4':
                verifier = Verification()
                if verifier.verify_all_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
                    print('All transactions verified')
                else:
                    print('Some transactions are invalid')
            elif user_choice == 'q':
                awaiting_input = False
            else: 
                print('Invalid input, please select a choice from the list')
            verifier = Verification()
            if not verifier.verify_blockchain(self.blockchain.chain):
                self.print_blockchain()
                print('Invalid blockchain!')
                break
            print('Balance of {}: {:6.2f}'.format(self.id, self.blockchain.get_balance()))
        else:
            print('User left') 
            
        print ('Program exited!')

node = Node()
node.listen_for_input()