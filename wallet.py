from Crypto.PublicKey import RSA
import Crypto.Random
import binascii
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256


class Wallet:
    def __init__(self, node_id):
        #set to none to prevent new keys being generated automatically when a new wallet object is created
        self.private_key = None
        self.public_key = None
        self.node_id = node_id

    def create_keys(self):
        private_key, public_key = self.generate_key()
        self.private_key = private_key
        self.public_key = public_key
        

    def save_keys(self):
        if self.public_key != None and self.private_key != None:
            try:
                with open('wallet-{}.txt'.format(self.node_id), mode='w') as file:
                    file.write(self.public_key)
                    file.write('\n')
                    file.write(self.private_key)
                return True
            except (IOError, IndexError):
                print('Failed to save wallet!')
                return False

    def load_keys(self):
        try:
            with open('wallet-{}.txt'.format(self.node_id), mode='r') as file:
                keys = file.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
                return True
        except (IOError, IndexError):
            print('Failed to load wallet!')
            return False

    def generate_key(self):
        #generates a 1024 bits random private key
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        #gets a key in binary format, passes it to hexlify which converts to hexadecimal and then decodes to ascii
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), (binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')))

    #generates a signature for a transaction
    def sign_transaction(self, sender, recipient, amount):
        #turns private_key from a str back to binary
        signer = PKCS1_v1_5.new(RSA.import_key(binascii.unhexlify(self.private_key)))
        hash_sign = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(hash_sign)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):
        public_key = RSA.import_key(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        hash_verify = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))
        return verifier.verify(hash_verify, binascii.unhexlify(transaction.signature))