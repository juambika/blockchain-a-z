# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 23:28:55 2021

@author: Juan Bautista Perán Zamora
"""
#Modulo 1 - Crear una cadena de bloques - blockchain

#Vamos a programar en Python 

#Herramientas para proceder a crear mi Blockchain

# 1 - En anaconda prompt tenemos que poner esta instrucción: pip install Flask==0.12.2
# 2 - Nos descargamos el Postman para hacer peticiciones de url para la transmisión de datos en https://getpostman.com

# 3 - Importamos las librerias necesarias
import datetime
import hashlib
import json
from flask import Flask, jsonify

#Bloque génesis - Primer bloque de la cadena Blockchain
#Proof = identificador del bloque
#Bloque genesis tiene el hash previo igual a 0 en string

#Parte 1 - Crear la Cadena de bloques
class Blockchain:
    
    def __init__(self):     #Constructor del bloque   
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):  #Creacion de un bloque
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash
               }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):  #Nos devuelve el último bloque de la cadena
        return self.chain[-1]

    #Principio de la criptografía (MUY DIFÍCIL DE RESOLVER, PERO MUY FÁCIL DE VERIFICAR)
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
    
    #Devolvemos el hash sha256 del bloque que le pasamos como argumento en base a los datos que contiene
    def hash_block(self,block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    #Esta función comprueba si la cadena de bloques que tengamos es válida
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while(block_index < len(chain)): #Mientras queden bloques de la cadena
           block = chain[block_index]
           if block['previous_hash'] != self.hash_block(previous_block):
               return False
           #Ahora obtenemos la prueba del bloque actual y la prueba del bloque previo
           previous_proof = previous_block['proof'] #El valor de la prueba previa
           proof = block['proof'] #El valor de la prueba actual
           hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
           
           #Si no se cumple el puzzle criptográfico, entonces hacemos saltar la alarmas
           if hash_operation[:4] != '0000':
               return False
           previous_block = block
           block_index += 1
        return True
            
        
#Parte 2 - Minado de un Bloque de la Cadena

#Creación de una aplicación web
app = Flask(__name__)

# Si se obtiene un error 500, actualizar flask, reiniciar spyder y ejecutar la siguiente línea
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

#Creación de una blockchain
blockchain = Blockchain()

#Minar un nuevo bloque - función de primera llamada creada con webApp creada con Flash en Python
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
   
    #Nos traemos el previous_hash del bloque previo para crear el enlace entre el nuevo bloque y el anterior
    previous_hash = blockchain.hash_block(previous_block)
    
    #Hacemos el vínculo entre el bloque actual y el previous hash
    block = blockchain.create_block(proof, previous_hash)
    
    #Como es una llamada mediante un proceso de Flash, necesitamos una respuesta del servidor para el postman
    response = {'message' : '¡Enhorabuena, has minado un nuevo bloque!', 
                'index': block['index'], #Clave del dicionario respuesta con la clave del dicionario del bloque actual
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']}
    return jsonify(response), 200  #Jeisonificamos la respuesta de Python, porque la información viene como un diccionario

#Obtenemos un diccionario con dos claves, la primera es toda la cadena y el segundo parametro es su longitud
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain' : blockchain.chain, 
                'length' : len(blockchain.chain)}
    return jsonify(response), 200

# Comprobar si la cadena de bloques es válida
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : 'Todo correcto. La cadena de bloques es válida.'}
    else:
        response = {'message' : 'Houston, tenemos un problema. La cadena de bloques no es válida.'}
    return jsonify(response), 200  

# Ejecutar la app
app.run(host = '0.0.0.0', port = 5000) #Con esta url, hacemos que sea públicamente accesible desde cualquier lado del mundo