#!/bin/bash

./server.py.txt &> saida_servidor.txt &

FILE="saida_cliente.txt"

: > "$FILE"
for i in {1..5}
do
    echo -e "Iteração $i\n" >> "$FILE"
    ./client.py.txt >> "$FILE"
    echo -e "--------------------------------------------------------------------------------------------------\n" >> "$FILE"
done 

echo -e "-------------------------------TESTE SIMULANDO CHAVE ERRADA-------------------------------\n" >> "$FILE"
echo -e "Iteração 6\n" >> "$FILE"
./client.py.txt falsa >> "$FILE"
echo -e "--------------------------------------------------------------------------------------------------\n" >> "$FILE"
