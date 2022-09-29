##base postada no classroom
##base postada no classroom
##base postada no classroom
##base postada no classroom
##base postada no classroom
##mudanca: diffiehellmann

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from random import randint
import cryptocode

def HandleRequest(mClientSocket, mClientAddr):
    while True:

        print('Esperando o próximo pacote ...')

        data = mClientSocket.recv(2048)

        print(f'Requisição recebida de {mClientAddr}')
        req = data.decode()
        print(f'A requisição foi:{req}')

        rep = 'Hey cliente!'
        mClientSocket.send(rep.encode())


mSocketServer = socket(AF_INET, SOCK_STREAM)
print(f'Socket criado ...')

mSocketServer.bind(('127.0.0.1',1235))

mSocketServer.listen()

#clientes = []
#dic = {}

while True:
    
    mClientSocket, mClientAddr =  mSocketServer.accept()
    print(f'O servidor aceitou a conexão do Cliente: {mClientAddr}')

    chavesPublicas = [23, 9]
    #chaveCriada = diffiehelman(chavesPublicas)
    #msgCriptografada = f"{chaveCriada}"

    commonPaint = chavesPublicas[0]
    base = chavesPublicas[1]   
    bColor = 3
    bcMix = int(pow(base,bColor,commonPaint))  
    #transporta o mix
    mClientSocket.send(bcMix.encode()) 
    #recebe o mix
    acMix = mClientSocket.recv(2048)
    acMix = acMix.decode()
    commonSecretB = int(pow(acMix,bColor,commonPaint))

    chave = commonSecretB
    mensagem = "Esta eh a minha mensagem! :)"

    msgCriptografada = cryptocode.encrypt(mensagem, chave)
    print("Sua mensagem criptografada: " + msgCriptografada)

    msgDescriptografada = cryptocode.decrypt(msgCriptografada, chave)
    print("Sua mensagem descriptografada: " + msgDescriptografada)

    mClientSocket.send(msgCriptografada.encode())

    #dic[chaveCriada] = clientAddr

    #clients.append(client)

    thread = threading.Thread(target=HandleRequest, args=[mClientSocket, mClientAddr])
    thread.start()

   