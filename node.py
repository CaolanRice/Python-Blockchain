import json

from pkg_resources import require
from flask import Flask, jsonify, request
from flask_cors import CORS
 
from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)

@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys() 
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'balance': blockchain.get_balance()
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Failed to save keys'
        }
        return jsonify(response), 500

@app.route('/wallet', methods=['GET'])
def load_keys():
    if  wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'balance': blockchain.get_balance()
        }
        return jsonify(response), 200
    else: 
        response = {
            'message': 'Failed to load keys'
        }
        return jsonify(response), 500
    

@app.route('/', methods=['GET'])
def get_ui():
    return 'Heylo World'

@app.route('/mine', methods=['POST'])
def mine_block():
    block = blockchain.mine_block()
    #block and transactions use block OBJECT so must be converted to dict in order to jsonify
    if block!= None:
        dict_block = block.__dict__.copy()
        #return all the transactions in the block as a dict
        dict_block['transactions'] = [
            tx.__dict__ for tx in dict_block['transactions']]
        response = {
                'message': 'New block mined successfully',
                'block': dict_block,
                'balance': blockchain.get_balance()
            }
        return jsonify(response), 201
    else:
            response = {
            'message':'Failed to mine block',
            'wallet_setup': wallet.public_key != None 
            }
            return jsonify(response), 500

@app.route('/addtx', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        response = {
            'message': 'Wallet missing'
        }
        return jsonify(response), 400
    user_data = request.get_json()
    if not user_data:
        response = {
            'message': 'Data not found'
        }
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    #if all fields NOT are part of incoming values
    if not all(field in user_data for field in required_fields):
        response = {
            'message': 'Some required data is missing'
        }
        return jsonify(response), 400
    recipient = user_data['recipient']
    amount = user_data['amount']
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    successful = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)
    if successful:
        response = {
            'message': 'Transaction completed successfully',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature,
                'balance': blockchain.get_balance()
            }
            }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Failed to add a transaction'
        }
        return jsonify(response), 500

@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            'message': 'Successfully retrieved balance',
            'Balance': balance
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Failed to load balance',
            'wallet_setup': wallet.public_key != None
        }
        return jsonify(response), 500


@app.route('/chain', methods=['GET'])
def get_blockchain():
    snapshot_chain = blockchain.chain
    #copy of snapshot chain convered to a list of dictionaries so that it can be jsonified
    dict_chain = [block.__dict__.copy() for block in snapshot_chain]
    for dict_block in dict_chain:
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
    return jsonify(dict_chain), 200
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

