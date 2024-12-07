import sqlite3

def filter_number(value : float) -> float:
    if type(value) != float and type(value) != int:
        print("Valor precisa ser um numero!")
        return
    if value <= 0:
        print("Valor precisa ser maior que 0.01!")
        return
    return float(value)

def filter_str(string : str) -> str:
    if type(string) != str:
        print("Nome precisa ser letras!")
        return
    if string == '':
        print("Nome nao pode ficar vazio!")
        return
    return string

def add_to_db(key : str, value : float) -> None:
    try:
        db = sqlite3.connect('db_gastos.db')
        cursor = db.cursor()

        
        
        cursor.execute(f"INSERT INTO gastos VALUES('{key}',{value})")
        db.commit()
        db.close()
        print("Data added to db with sucess!")
    except sqlite3.Error as erro:
        print(f"Error when adding data: {erro}")

def remove_key_from_db(key : str) -> None:
    try:
        db = sqlite3.connect('db_gastos.db')
        cursor = db.cursor()

        if type(key) != str:
            print("Key must be string!")
            return 1
        if key == '':
            print("Key cant't be empty!")
            return 1
        cursor.execute(f"DELETE from gastos WHERE conta = '{key}'")
        db.commit()
        db.close()
        print("Data removed from db with sucess!")
    except sqlite3.Error as erro:
        print(f"Error when removing data: {erro}")

def clear_db() -> None:
    try:
        db = sqlite3.connect('db_gastos.db')
        cursor = db.cursor()
        cursor.execute(f"DELETE from gastos")
        db.commit()
        db.close()
        print("Dados limpos com sucesso!")
    except sqlite3.Error as erro:
        print(f"Erro ao limpar dados: {erro}")

#updates a value from db with the new_value value, where the key name is located
def update_keyValue_db(target_key : str, new_value : float) -> None:
    temp_dict = retrieve_data_dict()
    for k, v in temp_dict.items():
        if k == target_key:
            try:
                db = sqlite3.connect('db_gastos.db')
                cursor = db.cursor()
                cursor.execute(f"UPDATE gastos SET valor = '{filter_number(new_value)}' WHERE conta = '{filter_str(target_key)}'")
                db.commit()
                db.close()
                print("Valor atualizado com sucesso!")
            except sqlite3.Error as erro:
                print(f"Erro atualizando o valor: {erro}")


#updates a key from db with the new_key value
def update_keyName_db(target_key : str, new_key : str) -> None:
    temp_dict = retrieve_data_dict()
    for k, v in temp_dict.items():
        if k == target_key:
            try:
                db = sqlite3.connect('db_gastos.db')
                cursor = db.cursor()
                cursor.execute(f"UPDATE gastos SET conta = '{filter_str(new_key)}' WHERE conta = '{filter_str(target_key)}'")
                db.commit()
                db.close()
                print("Nome atualizado com sucesso!!!")
            except sqlite3.Error as erro:
                print(f"Erro atualizando o nome: {erro}")

#retrive raw list, remeber RAW
def retrieve_data_dict():
    temp_dict : dict[str, float] = {}
    try:
        db = sqlite3.connect('db_gastos.db')
        cursor = db.cursor()
        keys = [conta[0] for conta in cursor.execute("SELECT conta FROM gastos")]
        values = [valor[0] for valor in cursor.execute("SELECT valor FROM gastos")]
        for i in range(0,len(keys)):
            temp_dict[keys[i]] = values[i]
        print("Data retrieved with sucess!")
        return temp_dict
    except sqlite3.Error as erro:
        print(f"Error when retriving data: {erro}")

remove_key_from_db('test')
update_keyName_db('aluguel', 'casa')
print(retrieve_data_dict())