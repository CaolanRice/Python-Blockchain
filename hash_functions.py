import hashlib
import json

def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()

def hash_block(block):
   #using json to return our block dictionary as a string, then making a hash value from the returned string
   #hexdigest returns the hash as readable characters
   return hash_string_256(json.dumps(block, sort_keys=True).encode())
