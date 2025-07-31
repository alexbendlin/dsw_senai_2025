try:
    idade = int(input("Informe sua idade: "))
    print(f'Sua idade daqui a 10 anos será: {idade + 10}')
except ValueError:
    # Se ocorrer um erro de conversão, exibe uma mensagem amigável
    print("Erro: Favor digitar um número válido!")
except Exception as e:
    print("Erro: Favor digitar um número!")

print("O programa continua mesmo que um erro ocorra ou não.")

# Exemplo de tratamento de erro com divisão por zero
try:
    numerador = int(input("Informe o numerador: "))
    denominador = int(input("Informe o denominador: "))
    resultado = numerador / denominador
    print(f'Resultado da divisão: {resultado}')
except ZeroDivisionError:
    print("Erro: Divisão por zero não é permitida!")
except ValueError:
    print("Erro: Favor digitar números válidos!")
except Exception as e:
    print(f"Erro inesperado: {e}")