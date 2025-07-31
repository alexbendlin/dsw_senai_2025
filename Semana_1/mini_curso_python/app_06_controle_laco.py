# Exemplo de break e continue
for numero in range(1, 11):
    if numero == 3:
        continue # Pula o número 3
    
    if numero == 8:
        break # Interrompe o loop quando chega no número 8
    
    print(numero)
