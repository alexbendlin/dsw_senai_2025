frutas = ["maçã", "banana", "laranja"]
#           0,       1,        2

print(frutas)

print(frutas[1])

frutas[1] = "Abacaxi"
print(frutas)

for fruta in frutas:
    print(fruta)

frutas.remove('laranja')
print(frutas)