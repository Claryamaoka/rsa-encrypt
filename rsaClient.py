from socket import *

import random
import json

def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_random_prime(bit_length):
    while True:
        potential_prime = random.getrandbits(bit_length//2)
        if potential_prime % 2 != 0 and is_prime(potential_prime):
            return potential_prime

def coprimes(e, phi_n):
    divisores = []
    valid = 0
    for i in range(1, phi_n):
        if phi_n % i == 0:
            divisores.append(i)
    
    for x in divisores:
        if e % x == 0:
            valid += 1
    return valid == 1

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(x, phiN):
    g, d, _ = extended_gcd(x, phiN)
    if g == 1:
        return d % phiN
    else:
        return None

def rsa_encrypt(message):

    bit_length = 20  # Escolha o comprimento desejado para o número primo em bits
    p = generate_random_prime(bit_length)
    q = generate_random_prime(bit_length)
    print("Número primo aleatório p:", p)
    print("Número primo aleatório q:", q)

    #calcular N
    N = p * q
    
    #calcular função totiente de Euler
    phiN = (p-1)*(q-1)

    #selecionar e (número inteiro, positivo, menor que phiN e coprimo de phiN)
    for i in range(1, phiN):
        if coprimes(i, phiN) and i != 1:
            e = i;
            break;
    
    #calcular o inverso multiplicativo modular de e em relação a phiN para obter d
    d = mod_inverse(e, phiN)    

    # Converter a mensagem em uma lista de valores ASCII
    valores_ascii = [ord(char) for char in message]

    #elevar a mensagem a uma potência e
    valores_elevados = [valor ** e for valor in valores_ascii]

    #obter o resto da divisão por N
    valores_mod_N = [valor % N for valor in valores_elevados]

    #return valores_mod_N
    return {"chave D": d, "chave N": N, "valores": valores_mod_N}



serverName = "127.0.0.1"  # IPv4 // ::1 IPv6
serverPort = 12500
clientSocket = socket(AF_INET, SOCK_DGRAM)  # AF_INET6
print("UDP Client\n")
while True:
    message = input("Input message: ")
    if message == "exit":
        break
   
    encrypted_message = rsa_encrypt(message)  
    #print("Mensagem criptografada: ", encrypted_message)
    
    # Serializar o dicionário em uma string JSON
    json_message = json.dumps(encrypted_message)
    #print(json_message)
    clientSocket.sendto(bytes(json_message, "utf-8"), (serverName, serverPort))
    print("Message sent!")

clientSocket.close()