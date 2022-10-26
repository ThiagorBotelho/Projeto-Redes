##base postada no classroom
##mudanca: diffiehellmann
#identificadores adicionados

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import random
import cryptocode
import uuid
import os
from cryptography.fernet import Fernet
import time
import pathlib
import htmlMessage
import rsa

def HandleRequest(mClientSocket, mClientAddr, dic):
    while True:
        print("AGUARDANDO A CONEXÃO...")
        # recebendo o 'oi' do cliente1. o identificador dele ou dizendo q nao tem
        data = mClientSocket.recv(2048)
        identificadorBase = data.decode()

        if identificadorBase == "comunica":
            # se o cliente1 nao tem identificador
            identificadorCliente = uuid.uuid4()
            identificadorCliente = str(identificadorCliente)
            print(f'Conexão do cliente com o identificador {identificadorCliente}.')
            # criou o identificador e mandou
            mClientSocket.send(identificadorCliente.encode())
            resposta = mClientSocket.recv(2048) # confirmacao de q o cliente1 recebeu o id

            # inicio de DH. servidor manda as chaves publicas pro cliente1
            chavesPublicasString = "23, 9"
            mClientSocket.send(chavesPublicasString.encode())

            chavesPublicas = chavesPublicasString.split(',')
            commonPaint = int(chavesPublicas[0])
            base = int(chavesPublicas[1])
            # chave privada do servidor... nao vai guardar isso, vai guardar so o commonsecret
            bColor = random.randint(2, 64)
            bcMix = int(pow(base,bColor,commonPaint))
            bcMix = str(bcMix)
            # transporta o mix
            mClientSocket.send(bcMix.encode())
            # recebe o mix
            acMix = mClientSocket.recv(2048)
            acMix = int(acMix.decode())
            commonSecretB = int(pow(acMix,bColor,commonPaint))

            # guardando o identificador do cliente1 e o commonsecret entre eles q possibilita o DH
            dic[identificadorCliente] = commonSecretB
            chave = dic[identificadorCliente]

        else:
            # se o cliente1 tinha identificador, foi isso que ele mandou
            identificadorCliente = identificadorBase
            if dic[identificadorCliente] is not None:
                print(f'Conexão do cliente já conhecido com o identificador {identificadorCliente}.')
                # servidor entende quem é o cliente1 e pega a chave DH referente a ele
                chave = dic[identificadorCliente]

        # Pega o caminho do arquivo servidor.py no computador em que o servidor está rodando.
        caminho = pathlib.Path().absolute()
        caminho = str(caminho).replace("\\", "/")

        # Lista de arquivos para ignorar e não enviar aos clientes
        lista_ignora = ['servidor.py', 'htmlMessage.py', 'htmlMessage.cpython-310.pyc']

        # Percorre a pasta do servidor para coletar os arquivos que estão nessa pasta.
        # Envia lista de arquivos disponíveis para o cliente
        for diretorio, subpastas, arquivos in os.walk(caminho):
            for arquivo in arquivos:
                print(arquivo)
                if arquivo not in lista_ignora:
                    # Criptografa a mensagem de envio.
                    msgCriptografada = cryptocode.encrypt(arquivo, str(chave))
                    mClientSocket.send(msgCriptografada.encode())
                else:
                    pass
        time.sleep(0.5)
        msgCriptografada = cryptocode.encrypt('Lista enviada!', str(chave))
        mClientSocket.send(msgCriptografada.encode())

        # Receber o nome do cliente
        mensagem_recebida1 = mClientSocket.recv(2048)
        nome_cliente_cripto = mensagem_recebida1.decode()
        nome_cliente = cryptocode.decrypt(nome_cliente_cripto, str(chave))
        nome_cliente = nome_cliente.lower().strip()
        print(f'Nome do cliente: {nome_cliente}')

        # Receber a assinatura
        chavePublica = mClientSocket.recv(2048)
        chavePublica = chavePublica.decode()
        chavePublica1 = slice(10,-8)
        chavePublica2 = slice(-6, -1)

        chavePublica = rsa.PublicKey(int(chavePublica[chavePublica1]), int(chavePublica[chavePublica2]))

        assinatura = mClientSocket.recv(2048)
        #assinatura = assinatura.decode()
        #assinatura = cryptocode.decrypt(assinatura, str(chave))

        # Receber a mensagem (nome do arquivo)
        mensagem_recebida2 = mClientSocket.recv(2048)
        req = mensagem_recebida2.decode()
        nome_arquivo = cryptocode.decrypt(req, str(chave))
        print(f'Mensagem recebida: {nome_arquivo}')

        nome_arquivo1 = nome_arquivo.encode()
        rsa.verify(nome_arquivo1, assinatura, chavePublica)

        # RESPONDENDO

        # Tratamento de sintaxe do nome do arquivo requerido
        sintaxe = nome_arquivo.split(".")
        tipos_de_arquivo = ['html', 'htm', 'css', 'js', 'png', 'jpg', 'svg', 'pdf', 'jpeg', 'mp4', 'doc', 'zip', 'txt']

        # Verifica como o cliente escreveu o nome do arquivo
        if '.' not in nome_arquivo or sintaxe[1] not in tipos_de_arquivo:
            # ENVIO DO HTML ERRO BAD REQUEST AO CLIENTE - ERRO DE SINTAXE
            msg_erro_html = htmlMessage.BadRequest()
            msg_erro_html_cripto = cryptocode.encrypt(msg_erro_html, str(chave))
            data = msg_erro_html_cripto.encode()
            mClientSocket.send(data)

        else:
            # Tratamento de existência de arquivo solicitado
            caminho = pathlib.Path().absolute()
            caminho = str(caminho).replace("\\", "/")
            caminho_completo = caminho + "/" + nome_arquivo

            if os.path.isfile(caminho_completo):

                # Controle de acesso para o arquivo teste.txt
                lista_arquivos_permissao = ['teste.txt']
                lista_de_acesso_permitido = ['maria', 'marcos']

                if nome_arquivo in lista_arquivos_permissao:
                    # Como o arquivo requisitado ta dentro da lista de arquivos que requerem permissão, verifica agora
                    # se o cliente1 tem a permissão para acessar.
                    if nome_cliente in lista_de_acesso_permitido:

                        # ENVIO DO HTML SUCESSO AO CLIENTE
                        msg_sucesso_html = htmlMessage.sucesso()
                        msg_sucesso_html_cripto = cryptocode.encrypt(msg_sucesso_html, str(chave))
                        data = msg_sucesso_html_cripto.encode()
                        mClientSocket.send(data)

                        # geração de chave da criptografia (muda a cada envio de arquivo)
                        key = Fernet.generate_key()
                        print(f"A chave é :{key}")

                        # transforma em string para conseguir descriptografar
                        dado = key.decode()
                        # Criptografa a mensagem de envio da chave.
                        msgCriptografada = cryptocode.encrypt(dado, str(chave))
                        # envia a chave gerada ao cliente solicitante, para que ele possa descriptografar o arquivo.
                        mClientSocket.send(msgCriptografada.encode())

                        # usando a chave gerada
                        fernet = Fernet(key)

                        # abrindo o arquivo que o cliente1 solicitou para criptografar
                        with open(nome_arquivo, 'rb') as file:
                            original = file.read()

                        # criptografar o arquivo
                        encrypted = fernet.encrypt(original)

                        # abrir o arquivo no modo de gravação e gravar os dados criptografados
                        # (substituindo os dados do arquivo original)
                        with open(nome_arquivo, 'wb') as encrypted_file:
                            encrypted_file.write(encrypted)

                        # Envia o arquivo original com os dados criptografados ao cliente1
                        with open(nome_arquivo, 'rb') as file:
                            for data in file.readlines():
                                mClientSocket.send(data)
                            # Para dar tempo de o servidor mandar a 1 mensagem e depois a próxima sem misturar o envio.
                            time.sleep(0.5)
                            fim = 'Arquivo enviado!'
                            fim = fim.encode()
                            mClientSocket.send(fim)

                        # DESCRIPTOGRAFAR O ARQUIVO ORIGINAL DENTRO DA PASTA DO SERVIDOR
                        # abrindo o arquivo original que foi criptografado
                        with open(nome_arquivo, 'rb') as enc_file:
                            encrypted = enc_file.read()

                        # descriptografando o arquivo original
                        decrypted = fernet.decrypt(encrypted)

                        # abrindo o arquivo no modo de gravação e gravando os dados descriptografados
                        with open(nome_arquivo, 'wb') as dec_file:
                            dec_file.write(decrypted)

                    else:
                        # ENVIO DO HTML ERRO 403 Forbidden AO CLIENTE - NÃO AUTORIZADO
                        msg_erro_html = htmlMessage.NaoAutorizado()
                        msg_erro_html_cripto = cryptocode.encrypt(msg_erro_html, str(chave))
                        data = msg_erro_html_cripto.encode()
                        mClientSocket.send(data)

                else:
                    # ENVIO DO HTML SUCESSO AO CLIENTE
                    msg_sucesso_html = htmlMessage.sucesso()
                    msg_sucesso_html_cripto = cryptocode.encrypt(msg_sucesso_html, str(chave))
                    data = msg_sucesso_html_cripto.encode()
                    mClientSocket.send(data)

                    # geração de chave da criptografia (muda sempre)
                    key = Fernet.generate_key()

                    # transforma em string para conseguir descriptografar
                    dado = key.decode()
                    # Criptografa a mensagem de envio da chave.
                    msgCriptografada = cryptocode.encrypt(dado, str(chave))
                    # envia a chave gerada ao cliente solicitante, para que ele possa descriptografar o arquivo.
                    mClientSocket.send(msgCriptografada.encode())

                    # usando a chave gerada
                    fernet = Fernet(key)

                    # abrindo o arquivo que o cliente1 solicitou para criptografar
                    with open(nome_arquivo, 'rb') as file:
                        original = file.read()

                    # criptografar o arquivo
                    encrypted = fernet.encrypt(original)

                    # abrir o arquivo no modo de gravação e gravar os dados criptografados
                    # (substituindo os dados do arquivo original)
                    with open(nome_arquivo, 'wb') as encrypted_file:
                        encrypted_file.write(encrypted)

                    # Envia o arquivo original com os dados criptografados ao cliente1
                    with open(nome_arquivo, 'rb') as file:
                        for data in file.readlines():
                            mClientSocket.send(data)
                        # Para dar tempo de o servidor mandar a 1 mensagem e depois a próxima sem misturar o envio.
                        time.sleep(0.5)
                        fim = 'Arquivo enviado!'
                        print(fim)
                        fim = fim.encode()
                        mClientSocket.send(fim)

                    # DESCRIPTOGRAFAR O ARQUIVO ORIGINAL DENTRO DA PASTA DO SERVIDOR
                    # abrindo o arquivo original que foi criptografado
                    with open(nome_arquivo, 'rb') as enc_file:
                        encrypted = enc_file.read()

                    # descriptografando o arquivo original
                    decrypted = fernet.decrypt(encrypted)

                    # abrindo o arquivo no modo de gravação e gravando os dados descriptografados
                    with open(nome_arquivo, 'wb') as dec_file:
                        dec_file.write(decrypted)

            else:
                # ENVIO DO HTML ERRO 404 Not Found AO CLIENTE - NÃO ENCONTRADO
                msg_erro_html = htmlMessage.NaoEncontrado()
                msg_erro_html_cripto = cryptocode.encrypt(msg_erro_html, str(chave))
                data = msg_erro_html_cripto.encode()
                mClientSocket.send(data)


mSocketServer = socket(AF_INET, SOCK_STREAM)
print(f'Socket criado ...')
mSocketServer.bind(('127.0.0.1',1235))
mSocketServer.listen()

dic = {}

while True:
    clientSocket, clientAddr =  mSocketServer.accept()
    Thread(target=HandleRequest, args=(clientSocket, clientAddr, dic)).start()
    print("Saiu da função")
    # mSocketServer.close()

   