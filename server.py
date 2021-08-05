#!/usr/bin/env python3

import socket
import os
from struct import pack, unpack

from dotenv import load_dotenv, find_dotenv
from Crypto.Util.number import getPrime, getRandomNBitInteger
from Crypto.Cipher import DES

load_dotenv(find_dotenv())

HOST = os.getenv("HOST")  # Standard loopback interface address (localhost)
PORT = int(os.getenv("PORT"))  # Port to listen on (non-privileged ports are > 1023)

# https://stackoverflow.com/questions/33913308/socket-module-how-to-send-integer

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
      print("Aguardando conexoes")
      conn, addr = s.accept()
      with conn:
          print("Conectado por", addr)
          # Geracao das chaves
          prime_base = getPrime(32)
          print("Gerado primo:", prime_base)
          base = getRandomNBitInteger(15)
          print("Gerado base:", base)
          my_key = getRandomNBitInteger(15)
          print("Gerado inteiro secreto:", my_key)
          # Envio das bases
          print("Enviando para cliente o numero primo e a base")
          byte_array = pack("!II", prime_base, base)
          conn.send(byte_array)
          # Criação da chave publica
          print("Gerando chave publica a partir da base e primo")
          public_key = (base ** my_key) % prime_base
          print("Chave publica gerada:", public_key)
          # Envio da chave publica
          print("Enviando chave publica ao cliente")
          byte_array = pack("!I", public_key)
          conn.send(byte_array)
          # Recebimento da chave publica do cliente
          print("Aguardando recebimento da chave publica do cliente")
          data = conn.recv(32)
          [client_key] = unpack("!I", data)
          print("Chave publica do cliente recebida:", client_key)
          # Criacao da chave compartilhada
          print("Gerando chave compartilhada")
          shared_key = (client_key ** my_key) % prime_base
          print("Chave compartilhada gerada:", shared_key)

          # Transformando chave compartilhada em bytes  
          shared_key = shared_key.to_bytes(8, 'little')
          # Criação objeto de criptografia DES
          cipher = DES.new(shared_key)

          print("Aguardando mensagens do cliente")
          while True:
              data = conn.recv(1024)
              if not data:
                  break
              print("Dados do cliente recebidos:", data)
              print("Descriptogradando mensagem")
              msg = cipher.decrypt(data).decode('utf-8')
              print('Mensagem descriptografada:', msg)     
