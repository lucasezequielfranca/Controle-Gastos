from calendar import monthrange
from datetime import datetime
import sqlite3
import os.path
from termcolor import colored

current_month : int = int(datetime.today().strftime('%m'))
current_day : int = int(datetime.today().strftime('%d'))
current_year : int = int(datetime.today().strftime('%Y'))
month_range_tupple : int = monthrange(current_year, current_month)
month_range : int = int(month_range_tupple[1])



#################################
#to do:
#separar o db total para o menu principal, esse aqui ser apenas o menu de detalhes dos dias, contas fixas automaticante serem adicionadas no menu total de gastos

def filter_float(pergunta : str) -> float:
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

def filter_int(pergunta : str) -> float:
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

def filter_str(pergunta: str) -> str:
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

def execute_total(cmd : str, month=current_month, year=current_year):
    try:
        db = sqlite3.connect(f'{month}_{year}_total.db')
        cursor = db.cursor()
        cursor.execute(cmd)
        db.commit()
        db.close()
    except sqlite3.Error as erro:
        print(f"Erro criando db: {erro}\n")

def execute_detalhes(cmd : str, month=current_month, year=current_year):
    try:
        db = sqlite3.connect(f'{month}_{year}_detalhes.db')
        cursor = db.cursor()
        cursor.execute(cmd)
        db.commit()
        db.close()
    except sqlite3.Error as erro:
        print(f"Erro criando db: {erro}\n")

def create_dbs(month=current_month,year=current_year):
    if os.path.isfile(f"./{month}_{year}_total.db") == False:
        execute_total("CREATE TABLE total(dia_total int, ganho_total float, gastos_total float)")
        i : int = 0
        while i < month_range:
            execute_total(f"INSERT INTO total VALUES({i + 1}, 0.0, 0.0)")
            i += 1
    if os.path.isfile(f"./{month}_{year}_detalhes.db") == False:
        i = 0
        while i < month_range:
            execute_detalhes(f"CREATE TABLE dia{str(i + 1)}(idgg int, nome float, valor float)") # idgg id ganho gasto 0 ganho 1 pra gasto
            i += 1

#recupera dados do db total mes e ano
def retrieve_data_total(month=current_month, year=current_year):
    temp_dict : list[dict[str, float]] = {}
    try:
        cur = sqlite3.connect(f'{month}_{year}_total.db').cursor()
        query = cur.execute(f'SELECT * FROM total')
        colname = [ d[0] for d in query.description ]
        temp_dict = [ dict(zip(colname, r)) for r in query.fetchall() ]
        cur.close()
        cur.connection.close()
        return temp_dict
    except sqlite3.Error as erro:
        print(f"Erro carregando dados: {erro}\n")

#recupera os dados do db detalhes e retorna um dict com uma lista de dicts, dia e mes e ano especifico
def retrieve_data_detalhes(dia = current_day, month=current_month, year=current_year):
    temp_dict : list[dict[str, float]] = {}
    try:
        cur = sqlite3.connect(f'{month}_{year}_detalhes.db').cursor()
        query = cur.execute(f'SELECT * FROM dia{str(dia)}')
        colname = [ d[0] for d in query.description ]
        temp_dict = [ dict(zip(colname, r)) for r in query.fetchall() ]
        cur.close()
        cur.connection.close()
        return temp_dict
    except sqlite3.Error as erro:
        print(f"Erro carregando dados: {erro}\n")

#adiciona o gasto no dia mes e ano indicado
def adicionar_gasto(id = 1, dia = current_day, month = current_month, year = current_year):
    nome = filter_str("Digite o nome do gasto: ")
    valor = filter_float("Digite o valor do gasto: ")
    id = 1
    execute_detalhes(f"INSERT INTO dia{str(dia)} VALUES({id},'{nome}',{valor})", month, year)
def adicionar_ganho(id = 0, dia = current_day, month = current_month, year = current_year):
    nome = filter_str("Digite o nome do ganho: ")
    valor = filter_float("Digite o valor do ganho: ")
    id = 0
    execute_detalhes(f"INSERT INTO dia{str(dia)} VALUES({id},'{nome}',{valor})", month, year)
#
def editar_entrada(dia = current_day, month = current_month, year = current_year):
    nome = filter_str("Digite o nome da entrada a ser editada: ")
    data = retrieve_data_detalhes(dia, month, year)
    for dict in data:
        if dict['nome'] == nome:
            print("Continue daqui")
            return
    print("Entrada nao encontrada!\n")

def line():
    print('-'.center(87, '-'))

def print_menu(dia = current_day, month = current_month, year = current_year):
        line()
        print(f" MENU DETALHADO DO DIA {dia} ".center(87, '*'))
        line()
        print("-----|" + f"ID".center(6) + '|' + f"Conta".center(30) + "   |   " + f"Valor".center(31) + "|-----")
        line()
        temp_dict = retrieve_data_detalhes(dia, month, year)
        acum : float = 0.0
        if temp_dict == []:
            print("-----|" + f"----".center(6) + '|' + f"----------".center(30) + "   |   " + f"R$----".center(31) + "|-----")
            line()
            print("-----|" + f"----".center(6) + '|' + f"Valor Total".center(30) + "   |   " + f"R$----".center(31) + "|-----")
            line()
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
        line()
        if acum < 0:
            colorfinal = 'red'
        if acum > 0:
            colorfinal = 'green'
        print("-----|" + f"".center(6) + '|' + colored(f"Valor Total".center(30), 'blue') + "   |   " + colored(f"R${acum:0.2f}".center(31), f'{colorfinal}') + "|-----")
        line()

def main():
    create_dbs()
    while True:
        print_menu()
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
                adicionar_gasto()
            case '2':
                adicionar_ganho()
            case '3':
                editar_entrada()
                
    
main()

