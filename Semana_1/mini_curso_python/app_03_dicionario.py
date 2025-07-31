pessoa = {
    "nome": "Carlos",
    "idade": 32,
    "cidade": "Jaraguá do Sul"
}

print(f"Nome: {pessoa["nome"]}")

# Adicionando uma nova chave e valor ao dicionário
pessoa['profissao'] = 'Mecânico'
print(pessoa)


#  *** Não mencionado em aula ***

# Removendo a chave "cidade" (Não mencionei em aula)
del pessoa["cidade"]
print(pessoa)

# Verificando se uma chave existe no dicionário
if "idade" in pessoa:
    print(f"Idade: {pessoa['idade']}")

# Iterando sobre as chaves e valores do dicionário
for chave, valor in pessoa.items():
    print(f"{chave}: {valor}")

# Limpando o dicionário
pessoa.clear()
print(pessoa)

# Verificando se o dicionário está vazio
if not pessoa:
    print("O dicionário está vazio.")

# Exemplo de dicionário em Python
# Dicionário é uma coleção de pares chave-valor
# As chaves devem ser únicas e imutáveis (strings, números, tuplas)
# Os valores podem ser de qualquer tipo (strings, números, listas, outros dicionários, etc.)
# Dicionários são mutáveis, ou seja, podem ser alterados após a sua criação
# Dicionários são definidos usando chaves {} e os pares chave-valor são separados por vírgulas
# Exemplo: pessoa = {"nome": "João", "idade": 30, "cidade": "São Paulo"}
# Acessando valores em um dicionário
# Para acessar um valor, usamos a chave entre colchetes: pessoa["nome"]
# Também podemos usar o método get: pessoa.get("nome")
# Adicionando novos pares chave-valor
# Para adicionar um novo par chave-valor, basta atribuir um valor a uma nova chave
# Exemplo: pessoa["profissao"] = "Engenheiro"
# Removendo pares chave-valor
# Para remover um par chave-valor, usamos o comando del: del pessoa["cidade"]
# Também podemos usar o método pop: pessoa.pop("cidade")
# Verificando se uma chave existe
# Podemos verificar se uma chave existe no dicionário usando o operador in
# Exemplo: if "idade" in pessoa: print(pessoa["idade"])
# Iterando sobre chaves e valores
# Podemos iterar sobre as chaves e valores de um dicionário usando um loop for
# Exemplo: for chave, valor in pessoa.items(): print(f"{chave}: {valor}")
# Limpando o dicionário
# Para remover todos os pares chave-valor, usamos o método clear: pessoa.clear()
# Verificando se o dicionário está vazio
# Podemos verificar se o dicionário está vazio usando a função bool
# Exemplo: if not pessoa: print("O dicionário está vazio.")