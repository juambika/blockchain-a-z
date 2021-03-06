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
import haslib
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
    

#Parte 2 - Minado de un Bloque de la Cadena