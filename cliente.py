##base postada no classroom
##mudanca: diffiehellmann
#identificadores adicionados

from socket import socket, AF_INET, SOCK_STREAM
import cryptocode
import random

mClientSocket = socket(AF_INET, SOCK_STREAM)
mClientSocket.connect(('localhost', 1235))
identificador = "0"
chave = -1

while True:
    # digita a mensagem que será enviada posteriormente
    mensagem = input("Digite>>")

    if identificador == "0":
        # se o cliente nao tiver um identificador oferecido pelo servidor

        print("O cliente não possui identificador.")
        # envia uma mensagem padrao, basicamente dizendo "nao tenho identificador"
        mClientSocket.send("comunica".encode())
        # recebe o identificador
        identificador = mClientSocket.recv(2048)
        identificador = identificador.decode()
        print(f"Identificador recebido: {identificador}")
        # diz que recebeu o identificador
        mClientSocket.send("Identificador recebido.".encode())

        # começa o DH. recebe as chaves publicas do servidor
        chavesPublicasString = mClientSocket.recv(2048)
        chavesPublicasString = chavesPublicasString.decode()
        chavesPublicas = chavesPublicasString.split(',')

        commonPaint = int(chavesPublicas[0])
        base = int(chavesPublicas[1])
        # gera sua chave privada com o random
        aColor = random.randint(2, 64)
        acMix = int(pow(base,aColor,commonPaint))  
        acMix = str(acMix)
        #recebe o mix
        bcMix = mClientSocket.recv(2048)
        bcMix = int(bcMix.decode())
        #transporta o mix
        mClientSocket.send(acMix.encode()) 
        commonSecretA = int(pow(bcMix,aColor,commonPaint))

        # chave do DH definida pro cliente. o msm processo aconteceu no servidor e ele guardou essa chave com o identificador
        chave = commonSecretA

    else:
        # o cliente já tem identificador pq se comunicou antes com o servidor
        print(f"Identificador do cliente: {identificador}")
        # envia o identificador pro servidor saber quem ele é e usar a chave DH certa pra comunicação
        mClientSocket.send(identificador.encode())

    # criptografando a mesangem que foi digitada no inicio e enviando
    msgCriptografada = cryptocode.encrypt(mensagem, str(chave))
    mClientSocket.send(msgCriptografada.encode())

    # recebendo resposta do servidor
    data = mClientSocket.recv(2048)
    reply = data.decode()
    msgDescriptografada = cryptocode.decrypt(reply, str(chave))
    print(f'Resposta do servidor: {msgDescriptografada}')


