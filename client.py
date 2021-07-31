#!/usr/bin/env python3

import socket
import os
from struct import pack, unpack

from Crypto.Util.number import getRandomNBitInteger
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")  # Standard loopback interface address (localhost)
PORT = int(os.getenv("PORT"))  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # Recebimento das chaves bases
    data = s.recv(64)
    [prime_base, base] = (unpack("!II", data))
    # Criação da chave publica 
    my_key = getRandomNBitInteger(20)
    public_key = (base ** my_key) % prime_base
    # Envio da chave publica
    byte_array = pack("!I", public_key)
    s.send(byte_array)
    # Recebimento da chave publica do servidor
    data = s.recv(32)
    [server_key] = unpack("!I", data)
    # Criacao da chave compartilhada
    shared_key = (server_key ** my_key) % prime_base
    print(shared_key)

