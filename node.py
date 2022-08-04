class Node:
    #constructor for blockchain. Attribute of the a Node, because every node will
    #have its own local copy of the blockchain
    def __init__(self):
        self.blockchain = []

    def listen_for_input(self):
        pass

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
        # loop to print the blockchain values
        for block in self.blockchain:
            print ('Printing Block')
            print (block)
        else:
            print('-' * 20)
    
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
                self.print_blockchain()
            elif user_choice == '4':
                verifier = Verification()
                if verifier.verify_all_transactions(open_transactions, get_balance):
                    print('All transactions verified')
                else:
                    print('Some transactions are invalid')
            elif user_choice == 'q':
                awaiting_input = False
            else: 
                print('Invalid input, please select a choice from the list')
            verifier = Verification()
            if not verifier.verify_blockchain(blockchain):
                self.print_blockchain()
                print('Invalid blockchain!')
                break
            print('Balance of {}: {:6.2f}'.format('Caolan', get_balance('Caolan')))
        else:
            print('User left') 
            
        print ('Program exited!')