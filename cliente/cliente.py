##base postada no classroom
##mudanca: diffiehellmann
#identificadores adicionados

from socket import socket, AF_INET, SOCK_STREAM
import cryptocode
import random
from cryptography.fernet import Fernet

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
        envio = "comunica"
        enviofinal = envio.encode()
        mClientSocket.send(enviofinal)
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

    # criptografando a mensagem que foi digitada no inicio e enviando
    msgCriptografada = cryptocode.encrypt(mensagem, str(chave))
    mClientSocket.send(msgCriptografada.encode())

    # recebendo resposta (confirmação) do servidor
    resp = mClientSocket.recv(2048)
    resposta = resp.decode()
    print('CÓDIGO DE RESPOSTA ABAIXO:')
    print(resposta)

    if resposta == 'Requisição bem-sucedida, objeto requisitado será enviado.':
        pergunta = 1
        break

    else:
        pergunta = int(input('Digite 1 para tentar outra requisição ou 0 para fechar: '))
        if pergunta == 0:
            break

if pergunta != 0:

    # Recebendo chave para descriptografar o arquivo.
    with open('filekey.key', 'wb') as filekey:
        key = mClientSocket.recv(2048)
        reply = key.decode()
        msgDescriptografada = cryptocode.decrypt(reply, str(chave))
        print(f'Resposta do servidor: {msgDescriptografada}')
        dataBytes = msgDescriptografada.encode()
        filekey.write(dataBytes)

    with open(mensagem, 'wb') as file:
        while 1:
            # recebendo arquivo do servidor
            data = mClientSocket.recv(2048)
            if not data:
                break
            file.write(data)

    print(f'{mensagem} recebido!\n')

    # abrindo a chave
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    # usando a chave
    fernet = Fernet(key)

    # abrindo o arquivo criptografado
    with open(mensagem, 'rb') as enc_file:
        encrypted = enc_file.read()

    # descriptografando o arquivo
    decrypted = fernet.decrypt(encrypted)

    # abrindo o arquivo no modo de gravação e
    # gravando os dados descriptografados
    with open(mensagem, 'wb') as dec_file:
        dec_file.write(decrypted)

else:
    print("Conexão finalizada!")
    mClientSocket.close()