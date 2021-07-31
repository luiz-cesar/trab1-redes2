#!/usr/bin/env python3

import socket
import os
from struct import pack, unpack

from dotenv import load_dotenv
from Crypto.Util.number import getPrime, getRandomNBitInteger

load_dotenv()

HOST = os.getenv("HOST")  # Standard loopback interface address (localhost)
PORT = int(os.getenv("PORT"))  # Port to listen on (non-privileged ports are > 1023)

# https://stackoverflow.com/questions/33913308/socket-module-how-to-send-integer

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print("Conectado por", addr)
        # Geracao das chaves
        prime_base = getPrime(32)
        base = getRandomNBitInteger(20)
        my_key = getRandomNBitInteger(20)
        # Envio das bases
        byte_array = pack("!II", prime_base, base)
        conn.send(byte_array)
        # Criação da chave publica
        public_key = (base ** my_key) % prime_base
        # Envio da chave publica
        byte_array = pack("!I", public_key)
        conn.send(byte_array)
        # Recebimento da chave publica do cliente
        data = conn.recv(32)
        [client_key] = unpack("!I", data)
        # Criacao da chave compartilhada
        shared_key = (client_key ** my_key) % prime_base
        print(shared_key) 
        # while True:
        #     data = conn.recv(32)
        #     if not data:
        #         break
