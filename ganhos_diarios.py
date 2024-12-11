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



def create_db():
    if os.path.isfile(f"./{current_month}_{current_year}.db"):
        return
    else:
        try:
            db = sqlite3.connect(f'{current_month}_{current_year}.db')
            cursor = db.cursor()
            create_table_cmd : str = f"CREATE TABLE dias(dia int, ganho float)"
            cursor.execute(create_table_cmd)
        except sqlite3.Error as erro:
            print(f"Erro criando db: {erro}\n")

create_db()