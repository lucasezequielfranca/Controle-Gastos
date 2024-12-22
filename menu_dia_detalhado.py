from funcoes import *
from termcolor import colored
import sqlite3
import os.path

def execute_detalhes(cmd : str, mes : int, ano : int):
    try:
        db = sqlite3.connect(f'{mes}_{ano}_detalhes.db')
        cursor = db.cursor()
        cursor.execute(cmd)
        db.commit()
        db.close()
    except sqlite3.Error as erro:
        print(f"Erro criando db: {erro}\n")

def create_dbs(mes : int, ano : int, mes_tam : int):
    if os.path.isfile(f"./{mes}_{ano}_detalhes.db") == False:
        i = 0
        while i < mes_tam:
            execute_detalhes(f"CREATE TABLE dia{str(i + 1)}(idgg int, nome float, valor float)", mes, ano) # idgg id ganho gasto 0 ganho 1 pra gasto
            i += 1

#recupera os dados do db detalhes e retorna um dict com uma lista de dicts, dia e mes e ano especifico
def retrieve_data_detalhes(dia : int, mes : int, ano : int):
    temp_dict : list[dict[str, float]] = {}
    try:
        cur = sqlite3.connect(f'{mes}_{ano}_detalhes.db').cursor()
        query = cur.execute(f'SELECT * FROM dia{str(dia)}')
        colname = [ d[0] for d in query.description ]
        temp_dict = [ dict(zip(colname, r)) for r in query.fetchall() ]
        cur.close()
        cur.connection.close()
        return temp_dict
    except sqlite3.Error as erro:
        print(f"Erro carregando dados: {erro}\n")

#adiciona o gasto no dia mes e ano indicado
def entrada_gasto(dia : int, mes : int, ano : int):
    nome = filtrar_str("Digite o nome do gasto: ")
    valor = filtrar_float("Digite o valor do gasto: ")
    execute_detalhes(f"INSERT INTO dia{str(dia)} VALUES({1},'{nome}',{valor})", mes, ano)

def entrada_ganho(dia : int, mes : int, ano : int):
    nome = filtrar_str("Digite o nome do ganho: ")
    valor = filtrar_float("Digite o valor do ganho: ")
    execute_detalhes(f"INSERT INTO dia{str(dia)} VALUES({0},'{nome}',{valor})", mes, ano)

def print_menu_dia(dia : int, mes : int, ano : int):
        linha()
        print(f" MENU DETALHADO DO DIA {dia} ".center(87, '*'))
        linha()
        print("-----|" + f"ID".center(6) + '|' + f"Conta".center(30) + "   |   " + f"Valor".center(31) + "|-----")
        linha()
        temp_dict = retrieve_data_detalhes(dia, mes, ano)
        acum : float = 0.0
        if temp_dict == []:
            print("-----|" + f"----".center(6) + '|' + f"----------".center(30) + "   |   " + f"R$----".center(31) + "|-----")
            linha()
            print("-----|" + f"----".center(6) + '|' + f"Valor Total".center(30) + "   |   " + f"R$----".center(31) + "|-----")
            linha()
            return
        acum = 0
        for dict in temp_dict:
            id = dict['idgg']
            conta = dict['nome']
            valor = dict['valor']
            color = "white"
            colorfinal = "white"
            if id == 0:
                color = 'green'
                acum += valor
            if id == 1:
                color = 'red'
                acum -= valor
            print("-----|" + colored(f"{id}".center(6), 'blue') + '|' + colored(f"{conta}".center(30), f'{color}') + "   |   " + colored(f"R${valor:0.2f}".center(31), f"{color}") + "|-----")
        linha()
        if acum < 0:
            colorfinal = 'red'
        if acum > 0:
            colorfinal = 'green'
        print("-----|" + f"".center(6) + '|' + colored(f"Valor Total".center(30), 'blue') + "   |   " + colored(f"R${acum:0.2f}".center(31), f'{colorfinal}') + "|-----")
        linha()

def editar_entrada(dia : int, mes : int, ano : int):
    nome = filtrar_str("Digite o nome da entrada a ser editada: ")
    data = retrieve_data_detalhes(dia, mes, ano)
    for dict in data:
        if dict['nome'] == nome:
            print("Continue daqui")
            return
    print("Entrada nao encontrada!\n")

def remover_entrada(dia : int, mes : int, ano : int):
    pass

def apagar_dia(dia : int, mes : int, ano : int):
    pass


def main(dia : int, mes : int, ano : int, mes_tam : int):
    create_dbs(mes, ano, mes_tam)
    while True:
        print_menu_dia(dia, mes, ano)
        print(" 1. Adicionar gasto\n",
              "2. Adicionar ganho\n",
              "3. Editar entrada\n",
              "4. Remover entrada\n",
              "5. Apagar dia\n",
              "6. Voltar\n"
              )
        selection = input(">>")
        match selection:
            case '1':
                entrada_gasto(dia, mes, ano)
            case '2':
                entrada_ganho(dia, mes, ano)
            case '3':
                editar_entrada(dia, mes, ano)
            case '4':
                remover_entrada(dia, mes, ano)
            case '5':
                apagar_dia(dia, mes, ano)
            case '6':
                break
                
