import datetime
import hashlib  # create de hash
import json  # create json
from flask import Flask, jsonify

# Parte 1 - Criação do Blockchain


class Blockchain:
    def __init__(self):
        # O Blockchain é uma cadeia de blocos
        # O primeiro (genesis) não tem um hash anterior
        # O proof dele deve ser 1
        self.chain = []
        self.create_block(data='genesis', previous_hash='0')

    def create_block(self, data, previous_hash):
        # Aqui eu crio meus blocos, e defino os seus parâmetros
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'nonce': 0,
                 'data': data,
                 'previous_hash': previous_hash
                 }
        nonce = self.proof_of_work(block)
        block.update(nonce=nonce)
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        nonce = 0
        check_nonce = False
        while check_nonce is False:
            block.update(nonce=nonce)
            hash_operation = self.hash(block)
            if hash_operation[:4] == '0000':
                check_nonce = True
            else:
                nonce += 1
        return nonce

    # Essa função tranforma o bloco em arquivo json e gera hash deste arquivo
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()


app = Flask(__name__)
# instanciando o blockchain(Criando o objeto em memória)
blockchain = Blockchain()


# Mineração do bloco


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block('block data', previous_hash)
    response = {'message': 'Parabéns, você minerou um bloco!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'nonce': block['nonce'],
                'data': block['data'],
                'previous_hash': block['previous_hash']
                },
    return jsonify(response), 200

# Criar função que retorne todo o blockchain


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5000)
