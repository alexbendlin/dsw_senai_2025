# Exemplo prático de lista
frutas = ["maçã", "banana", "laranja"]
# Índice [     0,        1,         2]

print("Lista original:", frutas)

print("Elemento no índice 1:", frutas[1])

frutas[1] = "Abacaxi"
print("Lista após alteração:", frutas)

print("Elementos da lista:")
for fruta in frutas:
    print(fruta)

# Removendo um elemento da lista
frutas.remove('laranja')
print("Lista após remoção:", frutas)


#  *** Não mencionado em aula ***

# Adicionando um novo elemento à lista
frutas.append("uva")
print("Lista após adição:", frutas)

# Verificando se um elemento existe na lista
if "maçã" in frutas:
    print("A maçã está na lista.")

# Verificando o tamanho da lista
print("Tamanho da lista:", len(frutas))

# Ordenando a lista
frutas.sort()
print("Lista ordenada:", frutas)

# Invertendo a lista
frutas.reverse()
print("Lista invertida:", frutas)

# Limpando a lista
frutas.clear()
print("Lista após limpeza:", frutas)

# Verificando se a lista está vazia
if not frutas:
    print("A lista está vazia.")

# Exemplo de lista em Python
# Lista é uma coleção ordenada e mutável de elementos
# As listas são definidas usando colchetes []
# Exemplo: frutas = ["maçã", "banana", "laranja"]
# Acessando elementos de uma lista
# Podemos acessar elementos de uma lista usando o índice, que começa em 0
# Exemplo: frutas[0] retorna "maçã"
# Modificando elementos de uma lista
# Podemos modificar um elemento de uma lista atribuindo um novo valor ao índice
# Exemplo: frutas[1] = "Abacaxi" altera o segundo elemento para "Abacaxi"
# Iterando sobre uma lista
# Podemos percorrer todos os elementos de uma lista usando um loop for
# Exemplo: for fruta in frutas: print(fruta)
# Removendo elementos de uma lista
# Podemos remover um elemento específico usando o método remove
# Exemplo: frutas.remove("laranja") remove "laranja" da lista
# Também podemos usar o método pop para remover o último elemento ou um elemento específico
# Exemplo: frutas.pop() remove o último elemento
# Adicionando elementos a uma lista
# Podemos adicionar um novo elemento ao final da lista usando o método append
# Exemplo: frutas.append("uva") adiciona "uva" ao final da lista
# Verificando se um elemento existe
# Podemos verificar se um elemento está na lista usando o operador in
# Exemplo: if "maçã" in frutas: print("A maçã está na lista.")
# Verificando o tamanho da lista
# Podemos obter o número de elementos na lista usando a função len
# Exemplo: len(frutas) retorna o número de elementos na lista
# Ordenando uma lista
# Podemos ordenar os elementos de uma lista usando o método sort
# Exemplo: frutas.sort() ordena a lista em ordem alfabética
# Invertendo uma lista
# Podemos inverter a ordem dos elementos de uma lista usando o método reverse
# Exemplo: frutas.reverse() inverte a ordem dos elementos
# Limpando uma lista
# Podemos remover todos os elementos de uma lista usando o método clear
# Exemplo: frutas.clear() remove todos os elementos da lista
# Verificando se a lista está vazia
# Podemos verificar se a lista está vazia usando a função bool
# Exemplo: if not frutas: print("A lista está vazia.") 
