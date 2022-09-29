##base postada no classroom
##base postada no classroom
##base postada no classroom
##base postada no classroom
##base postada no classroom
##mudanca: diffiehellmann

from socket import socket, AF_INET, SOCK_STREAM
import cryptocode


mClientSocket = socket(AF_INET, SOCK_STREAM)
mClientSocket.connect(('localhost', 1235))

chavesPublicas = [23, 9]

commonPaint = chavesPublicas[0]
base = chavesPublicas[1]   
aColor = 3
acMix = int(pow(base,aColor,commonPaint))  
#transporta o mix
mClientSocket.send(acMix.encode()) 
#recebe o mix
bcMix = mClientSocket.recv(2048)
bcMix = bcMix.decode()
commonSecretA = int(pow(bcMix,aColor,commonPaint))

chave = commonSecretA



while True:
    # Este loop foi criado apenas para que o cliente conseguisse enviar múltiplas solicitações
    mensagem = "Esta eh a minha mensagem! :)"
    msgCriptografada = cryptocode.encrypt(mensagem, chave)
    print("Sua mensagem criptografada: " + msgCriptografada)
    msgDescriptografada = cryptocode.decrypt(msgCriptografada, chave)
    print("Sua mensagem descriptografada: " + msgDescriptografada)
    mClientSocket.send(msgCriptografada.encode())

    #Recebendo as respostas do servidor.
    data = mClientSocket.recv(2048)
    reply = data.decode()
    print(f'Resposta recebida:{reply}')


