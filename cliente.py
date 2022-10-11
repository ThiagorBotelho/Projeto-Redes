##base postada no classroom
##base postada no classroom
##base postada no classroom
##base postada no classroom
##base postada no classroom
##mudanca: diffiehellmann




from socket import socket, AF_INET, SOCK_STREAM
import cryptocode
import random

mClientSocket = socket(AF_INET, SOCK_STREAM)
mClientSocket.connect(('localhost', 1235))

while True:
    mensagem = input("Digite>>")
    mClientSocket.send(mensagem.encode())

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

    print(f'chave: {chave}')
    
    
    msgCriptografada = cryptocode.encrypt(mensagem, str(chave))
    print(f'Sua mensagem criptografada: {msgCriptografada}')
    mensagem = msgCriptografada
    mClientSocket.send(mensagem.encode())


    data = mClientSocket.recv(2048)
    reply = data.decode()
    msgDescriptografada = cryptocode.decrypt(reply, str(chave))
    print(f'Sua mensagem descriptografada: {msgDescriptografada}')


