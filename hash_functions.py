import hashlib
import json

def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()

def hash_block(block):
   #using json to return our block dictionary as a string, then making a hash value from the returned string
   #hexdigest returns the hash as readable characters

   #this will give a dictionary version of the block. if copy is not called then
#    whenever you hash a block the hashable block will overwrite the previous reference for the last block
#    that it hashed. So hashes will not work well together since we would be changing old dicts of old blocks
   hashable_block = block.__dict__.copy()
   return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
