from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
 
from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def get_node_ui():
    return send_from_directory('user_interface', 'blockchain_ui.html')

@app.route('/network', methods=['GET'])
def get_network_ui():
    return send_from_directory('user_interface', 'network.html')

@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys() 
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
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
        blockchain = Blockchain(wallet.public_key, port)
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

@app.route('/transaction', methods=['POST'])
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

@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions), 200

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
    
@app.route('/addnode', methods=['POST'])
def add_node(node):
    user_data = request.get_json()
    if not user_data:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400
        #user_data is a dict due to get_json() so IN checks for existence of keys in that dict
    if 'node' not in user_data:
        response = {
            'message': 'No node data found'
        }
        return jsonify(response), 400
    node = user_data['node']
    blockchain.add_peer_node(node)
    response = {
        'message': 'Node added successfully',
        'all nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200

@app.route('/removenode/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url == None:
        response = {
            'message': 'Node not found'
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_url)
    response = {
        'message': 'Node removed',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200

@app.route('/getnodes', methods=['GET'])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    response = {
        'all_nodes': nodes
    }
    return jsonify(response), 200

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)
    args = parser.parse_args()
    print(args)
    port = args.port  
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)  
    app.run(host='0.0.0.0', port=port)
    

