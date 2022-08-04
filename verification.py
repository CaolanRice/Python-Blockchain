from hash_functions import hash_string_256, hash_block


class Verification:
#function that checks whether proof is valid, proof must match guess_hash
#incrementing proof leads to an entirely new hash 
    def valid_proof(self, transactions, last_hash, proof):
        #any cha
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        #checking if guest_hash begins with two 0's
        return guess_hash[0:2] == '00'

    #compare the stored hash in a given block with the recalculated hash of the previous block
    def verify_blockchain(self, blockchain):
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
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print ('Proof of work is invalid')
                return False
        return True 

    def verify_transaction(self, transaction, get_balance):
        sender_balance = get_balance(transaction.sender)
        if sender_balance >= transaction.amount:
            return True
        else:
            return False

    #get_balance arg
    def verify_all_transactions(self, open_transactions, get_balance):
        #using list comprehension and all function to return all TRUE (valid) transactions
        return all([self.verify_transaction(tx, get_balance) for tx in open_transactions]) 
