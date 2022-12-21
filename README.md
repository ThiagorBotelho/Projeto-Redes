# Projeto-Redes

# Resumo:
Para a realização deste trabalho, foi feita uma proposta envolvendo dois projetos diferentes. O primeiro projeto, intitulado “Autoridade Certificadora”, descreve o desenvolvimento de um servidor de autenticação, e é nele que são exigidos todos os pontos que envolvem a confidencialidade, integridade, autenticidade e disponibilidade das mensagens e arquivos. Para isso, o primeiro passo é a implementação do algoritmo Diffie-Hellman, assim como o desenvolvimento de um protocolo de aplicação. Além desses elementos, o projeto também pede que seja suportada a conexão de mais de 4 clientes simultaneamente, e que eles tenham, cada um, o próprio identificador que servirá como um instrumento para a gerência de chaves de criptografia e conexão. 

Já o segundo projeto, chamado “Servidor Web”, solicita o desenvolvimento de um dispositivo que implementa o protocolo HTTP/1.1, principalmente o método GET. Esse servidor deverá ser capaz de retornar diversos tipos de arquivos, como html, htm, css, js, png, jpg, svg; e de diversos tamanhos, até mesmo muito grandes. Como requisitos básicos para isso, destaca-se o retorno de 4 tipos distintos de resposta às requisições no formato HTML, sendo elas o 200 OK (requisição bem-sucedida), 400 Bad Request (erro de sintaxe), 403 Forbidden (solicitação não autorizada) e 404 Not Found (arquivo não encontrado).

A atividade foi lançada no dia 23/08/2022, com entrega marcada para dois meses depois, no dia 27/10/2022. Devido à pendências com outras matérias, o projeto só começou a ser desenvolvido um mês após a postagem do mesmo, de maneira que o grupo teve por volta de 6 semanas para completar todos os requisitos propostos. 

Grupo composto por Isabelle Queiroz, Rodrigo Leal, Thiago Botelho e Vinícius Marçal

# Manual do usuário:
	O primeiro passo para o usuário é baixar as bibliotecas utilizadas no projeto, para isso, basta inserir o seguinte trecho no terminal sem as aspas “pip install -r requirements.txt”. 
	1. Abra 5 terminais, um sendo o servidor e os outros 4 sendo clientes distintos (cliente1, cliente2, cliente3 e cliente4). Faça as etapas citadas no manual anteriormente.
	2. No cliente1, digite o nome como João e no nome do arquivo escreva propositalmente errado “teste,pmg”, após a mensagem de erro 400 Bad Request, aproveite e vá para outro cliente.
	3. No cliente2, digite o nome como Roberta e no nome do arquivo escreva propositalmente um arquivo que não está na lista mostrada de arquivos disponíveis do servidor, como por exemplo, “redes.jpeg”, após a mensagem de erro 404 Not Found, aproveite e vá para outro cliente.
	4. No cliente3, digite o nome como Jean e no nome do arquivo escolha o arquivo “teste.txt”, após a mensagem de erro 403 Forbidden, aproveite e vá para outro cliente.
	5. No cliente4, digite o nome como Maria e no nome do arquivo escolha o arquivo “teste.txt”, você verá que obteve sucesso na mensagem de HTTP/1.1 200 OK, podendo inclusive apertar o número 1 e fazer outra requisição para pedir outros tipos de arquivos.

# Vídeo do projeto sendo executado:
https://drive.google.com/file/d/1s8pZfibA2skELn2NPyLjNYGlk4oTrOHu/view?usp=sharing

# Link do relatório completo:
https://docs.google.com/document/d/16iteQwgYGaHl0WauQiIWb46bu7V9Pnho/edit?usp=sharing&ouid=100718540625698193714&rtpof=true&sd=true

# Referências:

Implementation Diffie-Hellman Algorithm. Disponível em: https://www.geeksforgeeks.org/implementation-diffie-hellman-algorithm/

Diffie-Hellman key exchange. Disponível em: https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange

Python RSA Documentation, usage. Disponível em: https://stuvel.eu/python-rsa-doc/usage.html#signing-and-verification

Como listar arquivos de uma pasta no Python? Disponível em: https://wallacemaxters.com.br/blog/56/como-listar-arquivos-de-uma-pasta-no-python#:~:text=Para%20listar%20os%20arquivos%20de,walk%20.&text=Caso%20deseje%20retornar%20o%20caminho,path

Como verificar se um arquivo ou diretório existe em Python? Disponível em: https://wallacemaxters.com.br/blog/72/como-verificar-se-um-arquivo-ou-diretorio-existe-em-python#:~:text=Em%20Python%2C%20o%20m%C3%A9todo%20os,tamb%C3%A9m%20%C3%A9%20um%20arquivo%20regular

Criptografar e descriptografar arquivos usando Python. Disponível em: https://acervolima.com/criptografar-e-descriptografar-arquivos-usando-python/

Como enviar e receber arquivos com socket em Python. Disponível em: https://www.youtube.com/watch?v=j4Drn47pc3o

Socket básico. Disponível em: https://wiki.python.org.br/SocketBasico
