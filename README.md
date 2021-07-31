# Trabalho 1 - Redes II

#### Professor Elias Duarte Júnior - UFPR

##### Realizado por Jean Guilherme Carraro da Silva e Luiz Cesar Clabond Almeida

### Instalação

É preciso utilizar a ferramenta pipenv para gerenciar os pacotes e versão do Python.

```shell
pipenv shell && pipenv install
```

\* Se não houver a possibilidade de instalação do pipenv, instalar os pacotes pip presentes no arquivo `Pipfile`

### Configuração do ambiente

Para configurar a porta e o endereço IP usados pelo servidor é preciso alterar o arquivo `.env` já inicialmente configurado. Caso cliente e servidor separados, os mesmos valores presentes no `.env` deve ser utilizado em ambos.

### Execução

###### Servidor:

```shell
./server.py
```

###### Cliente:

```shell
./client.py
```
