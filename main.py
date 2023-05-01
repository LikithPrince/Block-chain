#https://www.tutorialspoint.com/python_blockchain/index.htm

import hashlib
import random
import string
import json
import binascii
import numpy as np
import pandas as pd
import pylab as pl
import logging
import datetime
import collections

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class Client:
    def __init__(self):
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')

# Likith = Client()
# print (Likith.identity)
class Transaction:
    def __init__(self,sender,recipient,value):
        self.sender=sender
        self.recipient=recipient
        self.value=value
        self.time=datetime.datetime.now()

    def to_dict(self):
        if self.sender=="Genesis":
            identity="Genesis"
        else:
            identity=self.sender.identity

        return collections.OrderedDict({
            "Sender":identity,
            "Recipient": self.recipient,
            "Value":self.value,
            "Time": self.time
        })
    
    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

# Dinesh = Client()
# Ramesh = Client()


# t = Transaction(Dinesh,Ramesh.identity,5.0)

# signature = t.sign_transaction()
# print (signature)

    def display_transaction(transaction):
        #for transaction in transactions:
        dict = transaction.to_dict()
        print ("Sender: " + dict['Sender'])
        print ('-----')
        print ("Recipient: " + dict['Recipient'])
        print ('-----')
        print ("Value: " + str(dict['Value']))
        print ('-----')
        print ("Time: " + str(dict['Time']))
        print ('----******----')

transactions = []

Dinesh = Client()
Ramesh = Client()
Seema = Client()
Vijay = Client()

t1 = Transaction(Dinesh,Ramesh.identity,15.0)
t1.sign_transaction()
transactions.append(t1)
t2 = Transaction(Dinesh,Seema.identity,6.0)
t2.sign_transaction()
transactions.append(t2)
t3 = Transaction(Ramesh,Vijay.identity,2.0)
t3.sign_transaction()
transactions.append(t3)
t4 = Transaction(Seema,Ramesh.identity,4.0)
t4.sign_transaction()
transactions.append(t4)
t5 = Transaction(Vijay,Seema.identity,7.0)
t5.sign_transaction()
transactions.append(t5)
t6 = Transaction(Ramesh,Seema.identity,3.0)
t6.sign_transaction()
transactions.append(t6)
t7 = Transaction(Seema,Dinesh.identity,8.0)
t7.sign_transaction()
transactions.append(t7)
t8 = Transaction(Seema,Ramesh.identity,1.0)
t8.sign_transaction()
transactions.append(t8)
t9 = Transaction(Vijay,Dinesh.identity,5.0)
t9.sign_transaction()
transactions.append(t9)
t10 = Transaction(Vijay,Ramesh.identity,3.0)
t10.sign_transaction()
transactions.append(t10)

# for transaction in transactions:
#     Transaction.display_transaction (transaction)
#     print ('--------------')

class Block:
    global last_block_hash
    def __init__(self):
        self.verified_transactions = []
        self.previous_block_hash = ""
        self.Nonce = ""
    
last_block_hash = ""

# Dinesh = Client()
t0 = Transaction ("Genesis",Dinesh.identity,500.0)

block0 = Block()
block0.previous_block_hash = None
block0.Nonce = None
block0.verified_transactions.append(t0)

digest = hash (block0)
last_block_hash = digest
TPCoins = []
TPCoins.append(block0)


def dump_blockchain (self):
    print ("Number of blocks in the chain: " + str(len (self)))
dump_blockchain(TPCoins)

# for x in range (len(TPCoins)):
#     block_temp = TPCoins[x]
#     print ("block # " + str(x))

#     for transaction in block_temp.verified_transactions:
#         Transaction.display_transaction (transaction)
#         print ('--------------')
#         print ('=====================================')

def sha256(message):
    return hashlib.sha256(message.encode('ascii')).hexdigest()

def mine(message, difficulty=1):
    assert difficulty >= 1
    prefix = '1' * difficulty
    for i in range(1000):
        digest = sha256(str(hash(message)) + str(i))
        if digest.startswith(prefix):
            print ("after " + str(i) + " iterations found nonce: "+ digest)
    return digest

# print(mine ("test message", 2))

last_transaction_index = 0

# Miner 1 adds a block
block = Block()

for i in range(3):
    temp_transaction = transactions[last_transaction_index]
# validate transaction

    block.verified_transactions.append (temp_transaction)
    last_transaction_index += 1
block.previous_block_hash = last_block_hash
block.Nonce = mine (block, 2)
digest = hash (block)
TPCoins.append (block)
last_block_hash = digest

# Miner 2 adds a block
block = Block()

for i in range(3):
    temp_transaction = transactions[last_transaction_index]
    # validate transaction
    # if valid
    block.verified_transactions.append (temp_transaction)
    last_transaction_index += 1
block.previous_block_hash = last_block_hash
block.Nonce = mine (block, 2)
digest = hash (block)
TPCoins.append (block)
last_block_hash = digest

# Miner 3 adds a block
block = Block()

for i in range(3):
    temp_transaction = transactions[last_transaction_index]
    #display_transaction (temp_transaction)
    # validate transaction
    # if valid
    block.verified_transactions.append (temp_transaction)
    last_transaction_index += 1

block.previous_block_hash = last_block_hash
block.Nonce = mine (block, 2)
digest = hash (block)
TPCoins.append (block)
last_block_hash = digest

dump_blockchain(TPCoins)

for x in range (len(TPCoins)):
    block_temp = TPCoins[x]
    print ("block # " + str(x))

    for transaction in block_temp.verified_transactions:
        Transaction.display_transaction (transaction)
        print ('--------------')
        print ('=====================================')