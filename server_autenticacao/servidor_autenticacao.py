##base postada no classroom
##base postada no classroom
##base postada no classroom
##base postada no classroom
##base postada no classroom
##mudanca: diffiehellmann

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import random
import cryptocode
import uuid

def HandleRequest(mClientSocket, mClientAddr, dic):
    while True:

        data = mClientSocket.recv(2048)
        identificadorBase = data.decode()

        if identificadorBase == "comunica":
            identificadorCliente = uuid.uuid4()
            identificadorCliente = str(identificadorCliente)
            print(f'O servidor aceitou a conexão do cliente com o identificador: {identificadorCliente}')
            dic[identificadorCliente] = mClientAddr
            mClientSocket.send(identificadorCliente.encode()) 
            resposta = mClientSocket.recv(2048)
        else:
            identificadorCliente = identificadorBase
            #identificadorCliente = identificadorCliente.decode()
            #if dic[identificadorCliente] is not None:
            print("deu certo porra")
        
        chavesPublicasString = "23, 9"
        mClientSocket.send(chavesPublicasString.encode()) 
        
        chavesPublicas = [23, 9]
        commonPaint = chavesPublicas[0]
        base = chavesPublicas[1] 
        bColor = random.randint(2, 64)
        bcMix = int(pow(base,bColor,commonPaint))  
        bcMix = str(bcMix)
        #transporta o mix
        mClientSocket.send(bcMix.encode()) 
        #recebe o mix
        acMix = mClientSocket.recv(2048)
        acMix = int(acMix.decode())
        commonSecretB = int(pow(acMix,bColor,commonPaint))

        chave = commonSecretB

        mensangemRecebida = mClientSocket.recv(2048)
        print(f'Requisição recebida de {mClientAddr}')
        req = mensangemRecebida.decode()
        msgDescriptografada = cryptocode.decrypt(req, str(chave))
        print(f'Sua mensagem descriptografada: {msgDescriptografada}')

        msgCriptografada = cryptocode.encrypt("Mensagem recebido com sucesso.", str(chave))
        print(f'Sua mensagem criptografada: {msgCriptografada}')
        mensagem = msgCriptografada
        mClientSocket.send(mensagem.encode())



mSocketServer = socket(AF_INET, SOCK_STREAM)
print(f'Socket criado ...')

mSocketServer.bind(('127.0.0.1',1235))

mSocketServer.listen()

dic = {}

while True:
    clientSocket, clientAddr =  mSocketServer.accept()
    
    Thread(target=HandleRequest, args=(clientSocket, clientAddr, dic)).start()









   