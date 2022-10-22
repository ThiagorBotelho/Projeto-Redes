##base postada no classroom
##mudanca: diffiehellmann
#identificadores adicionados

from socket import socket, AF_INET, SOCK_STREAM
import cryptocode
import random
from cryptography.fernet import Fernet
import time


mClientSocket = socket(AF_INET, SOCK_STREAM)
mClientSocket.connect(('localhost', 1235))
identificador = "0"
chave = -1

while True:

    if identificador == "0":
        # se o cliente1 nao tiver um identificador oferecido pelo servidor

        print("O cliente1 não possui identificador.")
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

        # chave do DH definida pro cliente1. o msm processo aconteceu no servidor e ele guardou essa chave com o identificador
        chave = commonSecretA

    else:
        # o cliente1 já tem identificador pq se comunicou antes com o servidor
        print(f"Identificador do cliente1: {identificador}")
        # envia o identificador pro servidor saber quem ele é e usar a chave DH certa pra comunicação
        mClientSocket.send(identificador.encode())

    # Recebendo lista de arquivos disponíveis
    lista_arquivos = []
    while True:
        arq = mClientSocket.recv(2048)
        arquivos = arq.decode()
        arquivoDescripto = cryptocode.decrypt(arquivos, str(chave))
        if arquivoDescripto == 'Lista enviada!':
            break
        lista_arquivos.append(arquivoDescripto)

    # Digita a mensagem que será enviada posteriormente
    nome_cliente = input("Digite o nome do cliente>>")

    # Mostrar os arquivos disponíveis ao cliente:
    print("Arquivos Disponíveis:")
    for arquivo in lista_arquivos:
        print(f"-> {arquivo}")

    mensagem = input("Digite o arquivo requisitado>>")

    # criptografando o nome que foi digitado no inicio e enviando
    nome_cliente_cripto = cryptocode.encrypt(nome_cliente, str(chave))
    mClientSocket.send(nome_cliente_cripto.encode())

    # Para dar tempo de o cliente mandar a primeira mensagem e depois a próxima sem misturar o envio.
    time.sleep(0.5)

    # criptografando a mensagem que foi digitada no inicio e enviando
    msgCriptografada = cryptocode.encrypt(mensagem, str(chave))
    mClientSocket.send(msgCriptografada.encode())

    # recebendo resposta (confirmação) do servidor e descriptografando
    resp = mClientSocket.recv(2048)
    resposta = resp.decode()
    resposta_descripto = cryptocode.decrypt(resposta, str(chave))
    print('')
    print(resposta_descripto[:15])

    if resposta_descripto[:15] == 'HTTP/1.1 200 OK':
        pergunta = 1

        # Recebendo chave para descriptografar o arquivo.
        key = mClientSocket.recv(2048)
        reply = key.decode()
        msgDescriptografada = cryptocode.decrypt(reply, str(chave))
        print(f'Resposta do servidor: {msgDescriptografada}')
        KeyBytes = msgDescriptografada.encode()

        with open(mensagem, 'wb') as file:
            while 1:
                # recebendo arquivo do servidor
                data = mClientSocket.recv(2048)
                # print(f"Recebido: {data}")
                fim = data.decode()
                if fim == 'Arquivo enviado!':
                    break
                file.write(data)

        print(f'{mensagem} recebido!\n')

        # usando a chave que vai descriptografar o arquivo
        fernet = Fernet(KeyBytes)

        # abrindo o arquivo criptografado
        with open(mensagem, 'rb') as enc_file:
            encrypted = enc_file.read()

        # descriptografando o arquivo
        decrypted = fernet.decrypt(encrypted)

        # abrindo o arquivo no modo de gravação e
        # gravando os dados descriptografados
        with open(mensagem, 'wb') as dec_file:
            dec_file.write(decrypted)

        pergunta = int(input('Digite 1 para fazer outra requisição ou 0 para fechar: '))
        if pergunta == 0:
            break


    else:
        pergunta = int(input('Digite 1 para tentar outra requisição ou 0 para fechar: '))
        if pergunta == 0:
            break

print("Conexão finalizada!")
mClientSocket.close()