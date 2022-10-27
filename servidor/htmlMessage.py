from datetime import datetime
from pytz import timezone


def sucesso():
    now = datetime.now()
    # Fuso horario para ser independente do computador
    fuso_horario = timezone('America/Sao_Paulo')
    now_brasil = now.astimezone(fuso_horario)
    data_texto = now_brasil.strftime('%A, %d %B %Y, %H:%M:%S')

    #header
    resposta = ''
    resposta += 'HTTP/1.1 200 OK\r\n'
    resposta += f'Date: {data_texto}\r\n'
    resposta += 'Server: CIn UFPE/0.0.0.1 (Ubuntu)\r\n'
    # resposta += f'Content-Length: '
    resposta += 'Content-Type: text/html\r\n'
    resposta += '\r\n'

    # mensagem
    html = ''
    html += '<html>\r\n'
    html += '   <head>\r\n'
    html += '       <title> Sucesso!! </title>\r\n'
    html += '       <meta charset="UTF-8">\r\n'
    html += '   </head>\r\n'
    html += '   <body>\r\n'
    html += '       <h1> Requisição bem-sucedida, objeto requisitado será enviado! </h1>\r\n'
    html += '   </body>\r\n'
    html += '</html>\r\n'

    resposta += html
    return resposta

def NaoEncontrado():
    now = datetime.now()
    # Fuso horario para ser independente do computador
    fuso_horario = timezone('America/Sao_Paulo')
    now_brasil = now.astimezone(fuso_horario)
    data_texto = now_brasil.strftime('%A, %d %B %Y, %H:%M:%S')

    resposta = ''
    resposta += 'HTTP/1.1 404 Not Found\r\n'
    resposta += f'Date: {data_texto}\r\n'
    resposta += 'Server: CIn UFPE/0.0.0.1 (Ubuntu)\r\n'
    # resposta += f'Content-Length: '
    resposta += 'Content-Type: text/html\r\n'
    resposta += '\r\n'

    html = ''
    html += '<html>\r\n'
    html += '   <head>\r\n'
    html += '       <title> ERROR Not Found </title>\r\n'
    html += '       <meta charset="UTF-8">\r\n'
    html += '   </head>\r\n'
    html += '   <body>\r\n'
    html += '       <h1> Essa requisição não foi encontrada no servidor </h1>\r\n'
    html += '   </body>\r\n'
    html += '</html>\r\n'

    resposta += html
    return resposta

def NaoAutorizado():
    now = datetime.now()
    # Fuso horario para ser independente do computador
    fuso_horario = timezone('America/Sao_Paulo')
    now_brasil = now.astimezone(fuso_horario)
    data_texto = now_brasil.strftime('%A, %d %B %Y, %H:%M:%S')

    resposta = ''
    resposta += 'HTTP/1.1 403 Forbidden\r\n'
    resposta += f'Date: {data_texto}\r\n'
    resposta += 'Server: CIn UFPE/0.0.0.1 (Ubuntu)\r\n'
    # resposta += f'Content-Length: '
    resposta += 'Content-Type: text/html\r\n'
    resposta += '\r\n'

    html = ''
    html += '<html>\r\n'
    html += '   <head>\r\n'
    html += '       <title> ERROR Forbidden </title>\r\n'
    html += '       <meta charset="UTF-8">\r\n'
    html += '   </head>\r\n'
    html += '   <body>\r\n'
    html += '       <h1> O cliente não tem direitos de acesso ao conteúdo requisitado! </h1>\r\n'
    html += '   </body>\r\n'
    html += '</html>\r\n'

    resposta += html
    return resposta

def BadRequest():
    now = datetime.now()
    # Fuso horario para ser independente do computador
    fuso_horario = timezone('America/Sao_Paulo')
    now_brasil = now.astimezone(fuso_horario)
    data_texto = now_brasil.strftime('%A, %d %B %Y, %H:%M:%S')

    resposta = ''
    resposta += 'HTTP/1.1 400 Bad Request\r\n'
    resposta += f'Date: {data_texto}\r\n'
    resposta += 'Server: CIn UFPE/0.0.0.1 (Ubuntu)\r\n'
    # resposta += f'Content-Length: '
    resposta += 'Content-Type: text/html\r\n'
    resposta += '\r\n'

    html = ''
    html += '<html>\r\n'
    html += '   <head>\r\n'
    html += '       <title> ERROR Bad Request </title>\r\n'
    html += '       <meta charset="UTF-8">\r\n'
    html += '   </head>\r\n'
    html += '   <body>\r\n'
    html += '       <h1> Mensagem de requisição não entendida pelo servidor! </h1>\r\n'
    html += '   </body>\r\n'
    html += '</html>\r\n'

    resposta += html
    return resposta