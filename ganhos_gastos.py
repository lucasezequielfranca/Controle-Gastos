from calendar import monthrange
from datetime import datetime
import sqlite3
import os.path

current_month : int = int(datetime.today().strftime('%m'))
current_day : int = int(datetime.today().strftime('%d'))
current_year : int = int(datetime.today().strftime('%Y'))
month_range_tupple : int = monthrange(current_year, current_month)
month_range : int = int(month_range_tupple[1])


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
        execute_detalhes("CREATE TABLE detalhes(dia_detalhado int, ganho_detalhado float, gastos_detalhado float)")

def retrieve_data_dict(my_db : str, month=current_month, year=current_year):
    temp_dict : list[dict[str, float]] = {}
    try:
        cur = sqlite3.connect(f'{month}_{year}_{my_db}.db').cursor()
        query = cur.execute(f'SELECT * FROM {my_db}')
        colname = [ d[0] for d in query.description ]
        temp_dict = [ dict(zip(colname, r)) for r in query.fetchall() ]
        cur.close()
        cur.connection.close()
        return temp_dict
    except sqlite3.Error as erro:
        print(f"Erro carregando dados: {erro}\n")




def main():
    create_dbs()

main()
def adicionar_gasto():
    nome = input("Digite o nome do gasto: ")