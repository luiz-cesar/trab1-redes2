#!/usr/bin/env python3

import socket
import os
from struct import pack, unpack

from Crypto.Util.number import getRandomNBitInteger
from Crypto.Cipher import DES
from pyjokes import get_joke
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

HOST = os.getenv("HOST")  # Standard loopback interface address (localhost)
PORT = int(os.getenv("PORT"))  # Port to listen on (non-privileged ports are > 1023)

# Função para transformar o texto em um multiplo de 8 bytes
def pad(text):
    n = len(text) % 8
    return text if n == 0 else  text + (b' ' * (8-n))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Iniciando conexao com servidor")
    s.connect((HOST, PORT))
    print("Aguardando recebimento do numero base e primo")
    # Recebimento das chaves bases
    data = s.recv(64)
    [prime_base, base] = (unpack("!II", data))
    print("Primo e base recebidos:{} (primo) e {} base".format(prime_base, base))
    # Criação da chave publica 
    my_key = getRandomNBitInteger(15)
    print("Gerado inteiro secreto:", my_key)
    print("Gerando chave publica a partir da base e primo")
    public_key = (base ** my_key) % prime_base
    print("Chave publica gerada:", public_key)
    # Envio da chave publica
    print("Enviando chave publica ao servidor")
    byte_array = pack("!I", public_key)
    s.send(byte_array)
    # Recebimento da chave publica do servidor
    print("Aguardando recebimento da chave publica do servidor")
    data = s.recv(32)
    [server_key] = unpack("!I", data)
    print("Chave publica do servidor recebida:", server_key)
    # Criacao da chave compartilhada
    print("Gerando chave compartilhada")
    shared_key = (server_key ** my_key) % prime_base
    print("Chave compartilhada gerada:", shared_key)
    # Transformando chave compartilhada em bytes    
    shared_key = shared_key.to_bytes(8, 'little')
    # Criação objeto de criptografia DES 
    cipher = DES.new(shared_key)
    print("Gerando mensagem aleatoria")
    msg = get_joke(language='es', category= 'all')
    print("Mensagem gerada:", msg)
    encrypted_msg = cipher.encrypt(pad(msg.encode('utf-8')))
    print("Mensagem criptografada:", encrypted_msg)
    print("Enviando mensagem")
    s.send(encrypted_msg)
    print("Mensagem enviada. Encerrando")
