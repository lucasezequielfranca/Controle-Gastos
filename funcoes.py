from termcolor import colored as colored
import os
import colorama
colorama.init()
os.system("")

def filtrar_float(pergunta : str) -> float:
    while True:
        try:
            value = float(input(pergunta))
            if value <= 0:
                print("Valor precisa ser maior que 0.01!\n")
                continue
            break
        except:
                print(f"Valor precisa ser um numero!\n")
                continue
    return float(value)

def filtrar_int(pergunta : str) -> float:
    while True:
        try:
            value = int(input(pergunta))
            if value <= 0:
                print("Valor precisa ser maior que 0!\n")
                continue
            break
        except:
                print(f"Valor precisa ser um numero inteiro!\n")
                continue
    return int(value)

def filtrar_str(pergunta: str) -> str:
    values = list("abcdefghijklmnopqrstuvwxyz ")
    while True:
        my_string = input(pergunta).lower()
        if my_string == '':
            print("Nome nao pode ficar em branco\n")
            continue
        for item in my_string:
            if item not in values:
                my_string = my_string.replace(item, "")
        list1 : list = list(my_string)
        while list1[0] == ' ':
            list1.pop(0)
        while list1[-1] == ' ':
            list1.pop(-1)
        if len(list1) > 30:
            print("O nome nao pode ser maior que 30 caracteres\n"
                  "Removendo caracteres excedentes!")
        while len(list1) > 30:
            list1.pop(-1)
        my_string = str(''.join(list1))
        break
    return my_string

def linha():
    print('-'.center(87, '-'))
