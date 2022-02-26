# Creating Cryptocurrency
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


# Building a Blockchain

class Blockchain:
    
    #The init method to create a genesis block.
    def __init__(self):
        self.chain = []
        self.transactions = [] # Pillar 1 : Transactions.
        self.create_block(proof = 1, previous_hash = '0')
        
        #Pillar 2 : The nodes in the network to provide consensus
        self.nodes = set() # Its better to have set instead of list for all the nodes connected in the network

    #Creates a new block
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions' : self.transactions}
        self.transactions =[]
        self.chain.append(block) # Will apend the new block to the chain 
        return block;
    
    #Gets the last mined block
    def get_previous_block(self):
        return self.chain[-1]

    #The make concept behind crypto mining.
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    #Returns Hash of a block 
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
   
    #Check if the chain is valid, That is all the block as the correct prevoius has value.    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
               return False
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver' : receiver,
                                  'amount' : amount
            })
        previous_block = self.get_previous_block();
        return previous_block['index'] + 1
     
    #Add new nodes to the decentralized system.
    def add_node(self, address): # if address = http://127.0.0.1:5000/
        parsed_url = urlparse(address) 
        # ParseResult(scheme='http', netloc='127.0.0.1:5000', path='/', params='', query='', fragment='')
        self.nodes.add(parsed_url.netloc)
        
    #Replace a chain when it's not according to the consensus    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        
        #We will use the get chain method to get the details of the chain, for this we will
        #use the requests package and use the get method to make a request.
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    longest_chain = chain
                    max_length = length
        if longest_chain:
            self.chain =longest_chain
            return True
        return False
# Mining out Blockchain


# Flask based webapp
app = Flask(__name__)

# Creating an address for the node on Port 5000
# UUID('{12345678-1234-5678-1234-567812345678}') 
#This will be used to give the miner some coins when he mines the block
node_address = str(uuid4()).replace('-', '')

#Creating a Blockchain
blockchain = Blockchain()

#Mining a new block
@app.route('/mine_block', methods =['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Soham', amount = 10)
    block= blockchain.create_block(proof, previous_hash)
    
    response = {'message': 'Congratulations, you just mined a block !!!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'transactions': block['transactions'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']}
    return jsonify(response), 200

#Getting the full blockchain

@app.route('/get_chain', methods =['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'lenght': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods =['GET'])
def is_valid():
    valid_chain =  'The Chain is Valid' if blockchain.is_chain_valid(blockchain.chain) else 'The Chain is not valid'
    response = {'Chain Validity' : valid_chain}
    return jsonify(response), 200

@app.route('/add_transaction', methods =['POST'])
def add_transaction():
        json = request.get_json()
        transaction_keys = ['sender', 'receiver', 'amount']
        if not all (key in json for key in transaction_keys):
            return 'Invalid or Incomplete transaction request : Please check sender, receiver and amount', 400
        index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
        response = {'message' : f'This transaction will be added to the Block {index}'}
        return jsonify(response), 201

#Part 3 : Decentralizing the network
#Connecting new nodes

@app.route('/add_nodes', methods =['POST'])
def add_nodes():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No Nodes', 400
    for node in nodes:
        blockchain.add(node)
        response = {'messgae' : 'All nodes are connected, AdhiPaisa has the follwoing nodes',
                    'total_nodes' : list(blockchain.nodes)
                    }
    return jsonify(response), 201

#Replacing the longest chain

@app.route('/replace_chain', methods =['GET'])
def replace_chain():
    is_chain_repalced = blockchain.replace_chain()
    if is_chain_repalced:
        response = {'messgae' : 'The nodes had diffrent chains so the chain had to be replaced',
                    'new_chain' : blockchain.chain
                    }
    else:
        response = {'messgae' : 'All good, The chain is the longest one',
                    'actual_chain' : blockchain.chain
                    }
    return jsonify(response), 200


app.run(host = '0.0.0.0', port = 5000)