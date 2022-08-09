from utility.hash_functions import hash_string_256, hash_block
from wallet import Wallet


class Verification:
    #this method is not accessing anything from the class, it only uses with the input it is given
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        #any cha
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        #checking if guest_hash begins with two 0's
        return guess_hash[0:2] == '00'

    #compare the stored hash in a given block with the recalculated hash of the previous block
    
    #accesses valid proof method of the class
    @classmethod
    def verify_blockchain(cls, blockchain):
        #loop through the blocks in the blockchain and compare every block, wrapping 
        #the list with enumerate function to get back a tuple, giving us the index of the element
        #and the element itself.
        for (index, block) in enumerate(blockchain):
        # If index is 0 then we continue, as we don't need to validate the genesis block as it's the first block.  
            if index == 0:
                continue
        #compare value stored for this key with the last block. 
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print ('Proof of work is invalid')
                return False
        return True 

    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        if check_funds:
            #checking balance of transaction SENDER
            sender_balance = get_balance(transaction.sender)
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            return Wallet.verify_transaction(transaction)    


    #needs access to the class for verify_transaction
    @classmethod
    def verify_all_transactions(cls, open_transactions, get_balance):
        #using list comprehension and all function to return all TRUE (valid) transactions
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_transactions]) 
