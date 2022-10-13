##base postada no classroom
##mudanca: diffiehellmann
#identificadores adicionados

from socket import socket, AF_INET, SOCK_STREAM
import cryptocode
import random

mClientSocket = socket(AF_INET, SOCK_STREAM)
mClientSocket.connect(('localhost', 1235))
identificador = "0"

while True:
    mensagem = input("Digite>>")

    if identificador == "0":
        print("O cliente não possui identificador.")
        mClientSocket.send("comunica".encode())
        identificador = mClientSocket.recv(2048)
        identificador = identificador.decode()
        print(f"Identificador recebido: {identificador}")
        mClientSocket.send("Identificador recebido.".encode())
    else:
        print(f"Identificador do cliente: {identificador}")
        mClientSocket.send(identificador.encode())
        
    chavesPublicasString = mClientSocket.recv(2048)
    chavesPublicasString = chavesPublicasString.decode()
    chavesPublicas = chavesPublicasString.split(',')

    commonPaint = int(chavesPublicas[0])
    base = int(chavesPublicas[1])
    aColor = random.randint(2, 64)
    acMix = int(pow(base,aColor,commonPaint))  
    acMix = str(acMix)
    #recebe o mix
    bcMix = mClientSocket.recv(2048)
    bcMix = int(bcMix.decode())
    #transporta o mix
    mClientSocket.send(acMix.encode()) 
    commonSecretA = int(pow(bcMix,aColor,commonPaint))
    chave = commonSecretA
    
    msgCriptografada = cryptocode.encrypt(mensagem, str(chave))
    mClientSocket.send(msgCriptografada.encode())


    data = mClientSocket.recv(2048)
    reply = data.decode()
    msgDescriptografada = cryptocode.decrypt(reply, str(chave))
    print(f'Resposta do servidor: {msgDescriptografada}')


