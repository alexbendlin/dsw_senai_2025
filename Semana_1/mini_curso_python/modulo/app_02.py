# Exemplo de uso de módulos em Python
# Importando o módulo personalizado de matemática
# O módulo deve estar no mesmo diretório ou no caminho do Python
# Neste caso, o módulo se chama matematica.py e contém funções básicas de matemática
# As funções disponíveis são adicao, subtracao, multiplicacao e divisao
# Podemos importar funções específicas do módulo matematica
# Importando funções específicas do módulo matematica: subtracao e multiplicacao
from matematica import subtracao, multiplicacao

print(f'Subtração: {subtracao(5, 2)}')

print(f'Multiplicação: {multiplicacao(5, 5)}')
