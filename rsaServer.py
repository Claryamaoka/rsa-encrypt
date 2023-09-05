from socket import *

import json

def rsa_decrypt(encrypted_message, chave, N):

    #elevar a mensagem criptografada a uma potencia d
    valores_elevados = [valor ** chave for valor in encrypted_message]

    #obter o resto da divisão por N
    valores_mod_N = [valor % N for valor in valores_elevados]

    # Transformando em caracteres
    caracteres = [chr(valor) for valor in valores_mod_N]

    # Juntando os caracteres para formar a string
    string_resultante = ''.join(caracteres)
    print(string_resultante)
    return string_resultante


serverPort = 12500
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))
print("UDP server\n")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    encrypted_text = str(message, "utf-8")

    # Use json.loads() para decodificar a string JSON em um dicionario
    lista_decodificada = json.loads(encrypted_text)

    decrypted_message = rsa_decrypt(lista_decodificada["valores"], lista_decodificada["chave D"], lista_decodificada["chave N"])

    #decrypted_message = rsa_decrypt(encrypted_text, chave, N)
    print("Mensagem decriptografada:", decrypted_message)