from Crypto.PublicKey import RSA
# import Crypto.random
import binascii





class Wallet:
    def __init__(self):
        #set to none to prevent new keys being generated automatically when a new wallet object is created
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_key()
        self.private_key = private_key
        self.public_key = public_key
        

    def save_keys(self):
        if self.public_key != None and self.private_key != None:
            try:
                with open('wallet.txt', mode='w') as file:
                    file.write(self.public_key)
                    file.write('\n')
                    file.write(self.private_key)
            except (IOError, IndexError):
                print('Failed to save wallet!')

    
    def load_keys(self):
        try:
            with open('wallet.txt', mode='r') as file:
                keys = file.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
        except (IOError, IndexError):
            print('Failed to load wallet!')

    def generate_key(self):
        #generates a 1024 bits random private key
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        #gets a key in binary format, passes it to hexlify which converts to hexadecimal and then decodes to ascii
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), (binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')))