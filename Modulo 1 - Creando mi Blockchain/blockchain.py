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
        return True
            
        
        
    


#Parte 2 - Minado de un Bloque de la Cadena