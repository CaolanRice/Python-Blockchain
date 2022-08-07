from flask import Flask, jsonify
from flask_cors import CORS
 
from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)

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
                'block': dict_block
            }
        return jsonify(response), 201
    else:
            response = {
            'message':'Failed to mine block',
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

