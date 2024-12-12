from calendar import monthrange
from datetime import datetime
import sqlite3
import os.path

current_month : int = int(datetime.today().strftime('%m'))
current_day : int = int(datetime.today().strftime('%d'))
current_year : int = int(datetime.today().strftime('%Y'))
month_range_tupple : int = monthrange(current_year, current_month)
month_range : int = int(month_range_tupple[1])
print(month_range)


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
data_total = retrieve_data_dict("total")
for day in data_total:
    if day['dia_total'] == current_day:
        for k,v in day.items():
            print(f"{k},{v}")