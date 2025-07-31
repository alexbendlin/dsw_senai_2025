# Importando e usando os módulos math e random
import math
import random

# Usando o módulo math para calcular a raiz quadrada
print(f'A raiz de 81 é: {math.sqrt(81)}')

# Usando o módulo random para escolher um item de uma lista
opcoes = ["pedra", "papel", "tesoura"]
escolha_pc = random.choice(opcoes)
print(f'Eu computador escolhi: {escolha_pc}')

# Exemplo de uso de módulos
# Módulos são arquivos Python que contêm funções, classes e variáveis reutilizáveis
# Podemos importar módulos usando a palavra-chave import
# Exemplo: import math importa o módulo math, que contém funções matemáticas
# Podemos usar funções do módulo importado usando a notação ponto
# Exemplo: math.sqrt(16) calcula a raiz quadrada de 16
# Também podemos importar módulos específicos usando from ... import ...
# Exemplo: from random import choice importa apenas a função choice do módulo random
# Podemos criar nossos próprios módulos definindo funções e classes em arquivos Python
# Exemplo: app_08_modulos.py pode conter funções que podemos importar e usar em outros arquivos
# Para usar uma função de um módulo, usamos a notação ponto: modulo.funcao()
# Exemplo: math.sqrt(25) retorna 5.0, que é a raiz quadrada de 25
# Módulos ajudam a organizar o código e a reutilizar funcionalidades
# Podemos criar módulos personalizados para agrupar funções relacionadas
# Exemplo: um módulo chamado utilidades.py pode conter funções úteis para o projeto