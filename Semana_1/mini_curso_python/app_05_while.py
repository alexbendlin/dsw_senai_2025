# Exemplos de loop while

# Exemplo 1:
numero_secreto = 9

palpite = 0

while palpite != numero_secreto:
    palpite = int(input("Digite um número de 0 a 10: "))

print("Parabéns!!! Você acertou!")

# Exemplo 2:
numero = 1
while numero <= 10:
    print(numero)
    # numero = numero + 1
    numero += 1
