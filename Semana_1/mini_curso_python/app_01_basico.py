print("Olá, Mundo!\n")

# Isto é um comentário. O Python não vai executar esta linha.
print("Isso será executado.\n")

# Variáveis
nome = "Maria"
idade = 30
altura = 1.65
eh_estudante = True

print(f"Nome: {nome}")
print(f"Idade: {idade}")
print(f"Altura: {altura}")
print(f"Estudante: {eh_estudante}")
print(f"Estudante: {'Sim' if eh_estudante else 'Não'}\n")

# Tipos de dados
print(f"O tipo de dado da variável nome é {type(nome)}")
print(f"O tipo de dado da variável idade é {type(idade)}")
print(f"O tipo de dado da variável altura é {type(altura)}")
print(f"O tipo de dado da variável eh_estudante é {type(eh_estudante)}\n")

# Listar os atributos e métodos de uma classe
print(dir(str), "\n")

# Cria uma lista apenas com os métodos que não começam com '__'
metodos_publicos_str = [metodo for metodo in dir(str) if not metodo.startswith('__')]

# Imprime a lista de forma mais legível
for metodo in metodos_publicos_str:
    print(metodo)
print()

# Usando um métodos da classe str
print(nome.upper())
print(nome.__add__(" da Silva"))

# Operações Matemáticas
soma = 10 + 5
subtracao = 20 - 8
multiplicacao = 7 * 6
divisao = 10 / 2

print(f"Soma: {soma}")
print(f"Subtração: {subtracao}")
print(f"Multiplicação: {multiplicacao}")
print(f"Divisão: {divisao}\n")


# Entrada do usuário (input)
nome_usuario = input("Qual é o seu nome? ")
print("Olá, " + nome_usuario + "!\n")

ano_nascimento_str = input("Em que ano você nasceu? ")
ano_nascimento = int(ano_nascimento_str) # Converte a string para inteiro

idade_aproximada = 2025 - ano_nascimento
print("Você tem aproximadamente", idade_aproximada, "anos.")

# Condicionais: if, elif e else
idade = int(input("Digite sua idade: "))

if idade >= 18:
    print("Você é maior de idade.")
else:
    print("Você é menor de idade.")


nota = float(input("Digite sua nota (0 a 10): "))

if nota >= 7.0:
    print("Aprovado!")
elif nota >= 5.0:
    print("Recuperação.")
else:
    print("Reprovado.")
print()


# Laços de Repetição
# A função range(5) gera uma sequência de números de 0 a 4.
for numero in range(5):
    print("O número agora é:", numero)
print()

for numero in range(1, 6):
    print("O número agora é:", numero)
print()

# Percorrendo uma lista de nomes
nomes = ["Ana", "Bruno", "Carlos", "Daniela"]
for nome in nomes:
    print("Olá, " + nome)
print()


# Funções
# Definindo uma função simples
def saudacao():
    print("Seja bem-vindo ao mundo das funções!")

# Chamando (executando) a função
saudacao()
saudacao()
print()

# Funções com parâmetros
def saudacao_personalizada(nome):
    print("Olá, " + nome + "!")

saudacao_personalizada("Pedro")
saudacao_personalizada("Julia")
print()

# Funções que Retornam um Valor
def somar(a, b):
    resultado_soma = a + b
    return resultado_soma

# Guardando o resultado da função em uma variável
resultado_final = somar(10, 15)
print("O resultado da soma é:", resultado_final)

# Usando o retorno diretamente
print("O resultado de 5 + 3 é:", somar(5, 3))
