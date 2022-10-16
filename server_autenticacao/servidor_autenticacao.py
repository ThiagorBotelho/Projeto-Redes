##base postada no classroom
##mudanca: diffiehellmann
#identificadores adicionados

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import random
import cryptocode
import uuid
import os

def HandleRequest(mClientSocket, mClientAddr, dic):
    while True:
        # recebendo o 'oi' do cliente. o identificador dele ou dizendo q nao tem
        data = mClientSocket.recv(2048)
        identificadorBase = data.decode()

        if identificadorBase == "comunica":
            # se o cliente nao tem identificador
            identificadorCliente = uuid.uuid4()
            identificadorCliente = str(identificadorCliente)
            print(f'Conexão do cliente com o identificador {identificadorCliente}.')
            # criou o identificador e mandou
            mClientSocket.send(identificadorCliente.encode())
            resposta = mClientSocket.recv(2048) # confirmacao de q o cliente recebeu o id

            # inicio de DH. servidor manda as chaves publicas pro cliente
            chavesPublicasString = "23, 9"
            mClientSocket.send(chavesPublicasString.encode())

            chavesPublicas = chavesPublicasString.split(',')
            commonPaint = int(chavesPublicas[0])
            base = int(chavesPublicas[1])
            # chave privada do servidor... nao vai guardar isso, vai guardar so o commonsecret
            bColor = random.randint(2, 64)
            bcMix = int(pow(base,bColor,commonPaint))
            bcMix = str(bcMix)
            #transporta o mix
            mClientSocket.send(bcMix.encode())
            #recebe o mix
            acMix = mClientSocket.recv(2048)
            acMix = int(acMix.decode())
            commonSecretB = int(pow(acMix,bColor,commonPaint))

            # guardando o identificador do cliente e o commonsecret entre eles q possibilita o DH
            dic[identificadorCliente] = commonSecretB
            chave = dic[identificadorCliente]

        else:
            # se o cliente tinha identificador, foi isso que ele mandou
            identificadorCliente = identificadorBase
            if dic[identificadorCliente] is not None:
                print(f'Conexão do cliente já conhecido com o identificador {identificadorCliente}.')
                # servidor entende quem é o cliente e pega a chave DH referente a ele
                chave = dic[identificadorCliente]

        # comunicacao da parte de realmente receber a mensagem
        mensangemRecebida = mClientSocket.recv(2048)
        req = mensangemRecebida.decode()
        msgDescriptografada = cryptocode.decrypt(req, str(chave))
        print(f'Mensagem recebida: {msgDescriptografada}')

        # RESPONDENDO
        # msgCriptografada = cryptocode.encrypt("Mensagem recebida com sucesso.", str(chave))
        # mClientSocket.send(msgCriptografada.encode())

        # Tratamento de sintaxe
        sintaxe = msgDescriptografada.split(".")
        tipos_de_arquivo = ['html', 'htm', 'css', 'js', 'png', 'jpg', 'svg', 'pdf', 'jpeg', 'mp4', 'doc', 'zip', 'txt']

        # Verifica como o cliente escreveu o nome do arquivo
        if '.' not in msgDescriptografada or sintaxe[1] not in tipos_de_arquivo:
            print('ERRO 400 Bad Request: Mensagem de requisição não entendida pelo servidor.')
            msgError = 'ERRO 400 Bad Request: Mensagem de requisição não entendida pelo servidor.'
            data = msgError.encode()
            mClientSocket.send(data)

        else:
            # Tratamento de existência de arquivo
            caminho = "C:/Users/thiag/PycharmProjects/pythonProject1/servidor/"
            caminhoTodo = caminho + msgDescriptografada

            if os.path.isfile(caminhoTodo):
                print('Requisição bem-sucedida, objeto requisitado será enviado.')
                msgSucess = 'Requisição bem-sucedida, objeto requisitado será enviado.'
                data = msgSucess.encode()
                mClientSocket.send(data)

                with open(msgDescriptografada, 'rb') as file:
                    for data in file.readlines():
                        dado = data.decode()
                        msgCriptografada = cryptocode.encrypt(dado, str(chave))
                        mClientSocket.send(msgCriptografada.encode())
                    print('Arquivo enviado!')
                    break

            else:
                print('ERRO 404 Not Found! Documento requisitado não localizado no servidor.')
                msgError = 'ERRO 404 Not Found! Documento requisitado não localizado no servidor.'
                data = msgError.encode()
                mClientSocket.send(data)


mSocketServer = socket(AF_INET, SOCK_STREAM)
print(f'Socket criado ...')
mSocketServer.bind(('127.0.0.1',1235))
mSocketServer.listen()

dic = {}

while True:
    clientSocket, clientAddr =  mSocketServer.accept()
    Thread(target=HandleRequest, args=(clientSocket, clientAddr, dic)).start()
    mSocketServer.close()

   